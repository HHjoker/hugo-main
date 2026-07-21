#!/usr/bin/env python3
"""Generate a page-bundle podcast MP3 with MiMo-V2.5-TTS.

The API key is read only from MIMO_API_KEY. It is never accepted as a command
line argument, which keeps it out of shell history and process listings.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1"
DEFAULT_MODEL = "mimo-v2.5-tts"
DEFAULT_VOICE = "苏打"
DEFAULT_STYLE = (
    "请使用自然、清晰、有洞察力的中文播客主持人口吻朗读。语速适中，"
    "不要播音腔，不要夸张表演；段落之间自然停顿，重点句稍微放慢。"
)


def verified_ssl_context() -> ssl.SSLContext:
    """Use certifi when the framework Python cannot locate macOS CA roots."""
    try:
        import certifi
    except ImportError:
        return ssl.create_default_context()
    return ssl.create_default_context(cafile=certifi.where())


def load_api_key() -> str | None:
    api_key = os.getenv("MIMO_API_KEY")
    if api_key:
        return api_key
    env_file = Path(
        os.getenv(
            "MIMO_ENV_FILE",
            str(Path.home() / "Documents" / "Codex" / ".secrets" / "hh-blog-mimo.env"),
        )
    )
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            key, separator, value = line.partition("=")
            if separator and key.strip() == "MIMO_API_KEY":
                value = value.strip().strip("\"'")
                if value:
                    return value
    if sys.platform == "darwin" and shutil.which("security"):
        result = subprocess.run(
            [
                "security", "find-generic-password", "-a", os.getenv("USER", ""),
                "-s", "hh-blog-mimo-tts", "-w",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    return None


def markdown_to_speech_text(markdown: str) -> str:
    markdown = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", markdown, count=1, flags=re.S)
    markdown = re.sub(r"```.*?```", "", markdown, flags=re.S)
    markdown = re.sub(r"`([^`]+)`", r"\1", markdown)
    markdown = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", markdown)
    markdown = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", markdown)
    markdown = re.sub(r"^#{1,6}\s*", "", markdown, flags=re.M)
    markdown = re.sub(r"^\s*[-*+]\s+", "", markdown, flags=re.M)
    markdown = re.sub(r"^\s*\d+[.)]\s+", "", markdown, flags=re.M)
    markdown = re.sub(r"^\s*>\s?", "", markdown, flags=re.M)
    markdown = re.sub(r"[*_~]", "", markdown)
    markdown = re.sub(r"^\s*[-|: ]{3,}\s*$", "", markdown, flags=re.M)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip()


def split_text(text: str, limit: int) -> list[str]:
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]
    chunks: list[str] = []
    current = ""

    def append_piece(piece: str) -> None:
        nonlocal current
        candidate = f"{current}\n\n{piece}".strip() if current else piece
        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = piece

    for paragraph in paragraphs:
        if len(paragraph) <= limit:
            append_piece(paragraph)
            continue
        sentences = [s for s in re.split(r"(?<=[。！？!?；;])", paragraph) if s]
        for sentence in sentences:
            if len(sentence) <= limit:
                append_piece(sentence)
            else:
                for start in range(0, len(sentence), limit):
                    append_piece(sentence[start : start + limit])
    if current:
        chunks.append(current)
    return chunks


def request_audio(
    *, base_url: str, api_key: str, model: str, voice: str, style: str,
    text: str, timeout: int, retries: int
) -> bytes:
    payload = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "user", "content": style},
                {"role": "assistant", "content": text},
            ],
            "audio": {"format": "wav", "voice": voice},
        },
        ensure_ascii=False,
    ).encode("utf-8")
    url = f"{base_url.rstrip('/')}/chat/completions"
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        request = urllib.request.Request(
            url,
            data=payload,
            method="POST",
            headers={
                "api-key": api_key,
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(
                request, timeout=timeout, context=verified_ssl_context()
            ) as response:
                result = json.load(response)
            audio_data = result["choices"][0]["message"]["audio"]["data"]
            return base64.b64decode(audio_data)
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError) as error:
            last_error = error
            if isinstance(error, urllib.error.HTTPError):
                detail = error.read().decode("utf-8", errors="replace")[:500]
                print(f"MiMo API HTTP {error.code}: {detail}", file=sys.stderr)
            if attempt < retries:
                time.sleep(min(2 ** attempt, 10))
    raise RuntimeError(f"MiMo TTS failed after {retries} attempts: {last_error}")


def encode_mp3(wav_files: list[Path], output: Path, bitrate: str) -> None:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required but was not found in PATH")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8", delete=False) as playlist:
        playlist_path = Path(playlist.name)
        for wav_file in wav_files:
            escaped = str(wav_file).replace("'", "'\\''")
            playlist.write(f"file '{escaped}'\n")
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "concat", "-safe", "0", "-i", str(playlist_path),
                "-ac", "1", "-ar", "24000", "-codec:a", "libmp3lame",
                "-b:a", bitrate, str(output),
            ],
            check=True,
        )
    finally:
        playlist_path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path, help="Hugo Markdown article")
    parser.add_argument("--output", type=Path, help="Defaults to podcast.mp3 beside the article")
    parser.add_argument("--base-url", default=os.getenv("MIMO_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--model", default=os.getenv("MIMO_TTS_MODEL", DEFAULT_MODEL))
    parser.add_argument("--voice", default=os.getenv("MIMO_TTS_VOICE", DEFAULT_VOICE))
    parser.add_argument("--style", default=os.getenv("MIMO_TTS_STYLE", DEFAULT_STYLE))
    parser.add_argument("--chunk-size", type=int, default=1600)
    parser.add_argument("--bitrate", default="48k")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    article = args.article.resolve()
    if not article.is_file():
        raise SystemExit(f"Article does not exist: {article}")
    output = (args.output or article.with_name("podcast.mp3")).resolve()
    speech_text = markdown_to_speech_text(article.read_text(encoding="utf-8"))
    chunks = split_text(speech_text, args.chunk_size)
    if not chunks:
        raise SystemExit("No speakable article text was found")
    print(f"Prepared {len(chunks)} chunks, {len(speech_text)} characters -> {output}")
    if args.dry_run:
        return 0

    api_key = load_api_key()
    if not api_key:
        raise SystemExit(
            "MiMo API key not found. Set MIMO_API_KEY or add the macOS Keychain "
            "item hh-blog-mimo-tts."
        )

    with tempfile.TemporaryDirectory(prefix="mimo-podcast-") as temp_dir:
        wav_files: list[Path] = []
        for index, chunk in enumerate(chunks, start=1):
            print(f"Generating chunk {index}/{len(chunks)} ({len(chunk)} characters)")
            audio = request_audio(
                base_url=args.base_url,
                api_key=api_key,
                model=args.model,
                voice=args.voice,
                style=args.style,
                text=chunk,
                timeout=args.timeout,
                retries=args.retries,
            )
            wav_path = Path(temp_dir) / f"chunk-{index:03d}.wav"
            wav_path.write_bytes(audio)
            wav_files.append(wav_path)
        encode_mp3(wav_files, output, args.bitrate)
    print(f"Created {output} ({output.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
