+++
date = '2026-11-11T00:00:00+08:00'
draft = false
title = 'RunSift 实战：验证历史日志能把漏数定位到哪一步'
description = '用完整日志和缺失日志对照，验证批次对账、证据回读，以及证据不足时的判断。'
tags = ['Rust', 'RunSift', '日志', '故障排查']
categories = ['编程技术']
+++

客户反馈一个批次少了 10 条数据，现场只剩历史日志。我们能从日志确认差额出现在哪个阶段吗？如果恰好缺了关键一行，工具又会怎么回答？

本文用 RunSift v0.5.0 跑一组对照。完整样例应定位到输出确认阶段。删除最终确认计数后，应明确指出缺少这份证据。整个对账过程在本地运行，无需模型或 API Key。

## 准备

以下命令从源码构建，使用 macOS 或 Linux 的常用 shell。需要 Git 和 Rust 工具链。
Apple Silicon 用户也可以下载预编译程序，并用它替换后文的 `"$runsift_bin"`。

```bash
git clone --branch v0.5.0 --depth 1 https://github.com/HHjoker/runsift.git
cd runsift
cargo build --locked --release
runsift_bin=./target/release/runsift
verify_dir=$(mktemp -d)
"$runsift_bin" --version
```

[v0.5.0 Release 和 macOS arm64 下载](https://github.com/HHjoker/runsift/releases/tag/v0.5.0)

## 1. 用完整日志确认差额

```bash
"$runsift_bin" import --case-id complete --output "$verify_dir" \
  examples/batch-shortfall.log

"$runsift_bin" inspect "$verify_dir/complete" check-batch A17 \
  --profile examples/batch-profile.json
```

检查 JSON 输出。预期 `status` 为 `difference`，`first_difference` 显示
`queued → confirmed`，预期 9,800 条，实际记录 9,790 条，差额 10 条。

从 `stages` 中复制 `confirmed` 对应的 `event_id`，回读日志和前后文：

```bash
"$runsift_bin" inspect "$verify_dir/complete" evidence '替换为实际事件ID'
```

这一步确认的是日志里的计数差额。实际丢失、延迟确认和统计错误仍需要输出文件或下游确认记录来区分。

## 2. 删除关键证据再验证

继续在同一个终端运行：

```bash
sed '/^batch=A17 final stage=confirmed /d' \
  examples/batch-shortfall.log > "$verify_dir/missing.log"

"$runsift_bin" import --case-id missing --output "$verify_dir" \
  "$verify_dir/missing.log"

"$runsift_bin" inspect "$verify_dir/missing" check-batch A17 \
  --profile examples/batch-profile.json
```

这次预期 `status` 为 `insufficient_evidence`，`missing_stages` 包含
`confirmed`，`first_difference` 为 `null`。样例仍保留 A170 的确认计数，
所以也能检查 A17 有没有误用相似批次的数据。

## 3. 换成自己的历史日志

```bash
"$runsift_bin" import --case-id real --output "$verify_dir" /path/to/app.log
"$runsift_bin" inspect "$verify_dir/real" overview
"$runsift_bin" inspect "$verify_dir/real" search '实际批次号或报错关键词'
```

普通文本日志可以先导入和搜索。搜索区分大小写，命中后用事件 ID 回读。
批次对账则需要日志里有批次号、可比较的最终计数和完成标记。
示例 profile 只匹配样例格式，换日志后要按项目调整。v0.5 会把历史输入读入内存，
首次试用大日志时可以先选择故障时间附近的文件或片段。

如果想验证 AI 调查有没有增益，选一个自己已经查清楚的真实事故，先记录正确定位和关键出处。
再让同一个模型分别直接查原始日志、用 RunSift 查询，对比定位准确性、引用能否复核、
证据不足时有没有误判，以及人工还需补几步。v0.5 的 `investigate` 需要自备适配器，
也可以先让已有的编码 Agent 调用 `inspect`。

这一组验证最值得关注的是结论会不会随证据变化。日志齐全时能定位到一个阶段，缺了最终计数后能说清还缺什么，调查结果才有复核价值。
