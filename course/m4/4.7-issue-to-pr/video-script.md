# 4.7 录播参考脚本：Issue → PR → 审核 → 合并

> 建议时长：9–11 分钟（边操作边录，此脚本只作参考，不逐字照念）
> 演示材料：浏览器预先打开 `github.com/openai/codex/issues/31520`、`github.com/openai/codex/pull/31667` 及其 `Files changed` 页面（无需登录）。

---

## 中英术语读法

| 术语 | 读法 | 首次出现时的口头解释 |
|---|---|---|
| `Issue` | 一休 | 工单 / 议题，用来正式记下 Bug 或新需求 |
| `Pull Request (PR)` | 普尔瑞奎斯特 / 皮阿 | 合并请求，分支干完活后申请并回 `main` 的交卷单 |
| `Review` | 瑞维尤 | 代码审核，看 `diff`、留批注、决定批准还是打回 |
| `Approve` | 额普鲁夫 | 审核通过，亮绿勾允许合并 |
| `Request changes` | 瑞奎斯特千吉斯 | 打回修改，说明哪里不对让作者或 AI 重改 |
| `Merge` | 默吉 | 正式把审核通过的改动并入 `main` 主线 |

---

## 分段参考

| 时间 | 屏幕画面 | 口播要点 |
|---|---|---|
| 00:00–01:15 | 展示「微信群传 ZIP 压缩包」混乱对比 → 切到「Issue → Branch → PR → Review → Merge」五步流程图 | 痛点引入：多人或人机协作靠发文件包一定乱套，整个软件世界靠这套 4 步标准流水线保持井井有条，也是 M4 的收官大串联。 |
| 01:15–03:30 | 展示 PR 页面顶部的 4 个标签页表格 + `Review changes` 3 按钮说明 | 把 4 个标签页翻成人话：`Conversation` 看为什么改、`Commits` 看步骤、`Checks` 看自动检查绿不绿、`Files changed` 看网页版 `diff` 验货！顺手破误解：不懂写代码照样能提好 Issue、审好 AI 的 PR。 |
| 03:30–05:15 | 切到 `openai/codex/issues/31520` 实景页面 | 带着观众看一份优秀 Issue 长什么样：报错命令 + 报错原文 + `CLI`/`bug` 标签，重点指一下右下角 `Development` 如何把 Issue 和 PR 双向绑在一起。 |
| 05:15–07:45 | 切到 `openai/codex/pull/31667` 总览页 → 再点进 `Files changed` 标签页 | **全场高光**：特写顶部一行 **`from agent/fix-install-compact-release-json into main`**！点出这正是 AI Agent 开分支交卷、36 项 Checks 体检、审稿人亮绿勾 `✓`、正文 `Fixes #31520` 合并后 2 秒自动关单的完整真实案例。接着切进 `Files changed` 指出 4.2 课学的红绿 `diff` 在网页里一模一样。 |
| 07:45–09:15 | 切到第 5 节的「审 AI 私有仓库 PR」模拟演练 | 停顿 5 秒，一口气串联 M3–M4 全部知识点：抓出 `Files changed` 里混进 `.env`（3.4 红线）+ `Checks` 报 `ScannerError`（3.3 YAML 坑），果断 `Request changes` 打回！ |
| 09:15–09:50 | 庆祝 M4 通关 + 预告 M5 第一课 5.1《把需求说清楚：先计划后动手》 | M4 全部 7 课完工，下一模块直接进入高效驱动 AI 的核心心法：怎么把需求写透、让 AI 先出计划再动手。 |

---

## 录制注意事项

- 展示 PR `#31667` 的 `Files changed` 时，可以鼠标悬停在某一行行号左边展示那个蓝色 `+` 号（如果已登录则会出现行内评论框；未登录时口头说明「登录后点行号旁的加号就能直接批注」即可），避免暴露个人 GitHub 账号。
- 强调 `Fixes #编号` / `Closes #编号` 是 GitHub 内置语法，学员以后自己建私有库也能直接用上。
