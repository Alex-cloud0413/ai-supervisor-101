# 7.1 录播参考脚本：同一个任务，在 Codex 上重做一遍

> 建议时长：8–10 分钟（边操作边录，此脚本只作参考，不逐字照念）
> 演示材料：浏览器打开 `learn.chatgpt.com/docs/agent-configuration/agents-md` 与 `learn.chatgpt.com/docs/codex/cli`；若作者本机已装 Codex CLI 或 ChatGPT 桌面端，可在 `ai-radar` 副本目录现场演示 1 轮。

---

## 中英术语读法

| 术语 | 读法 | 首次出现时的口头解释 |
|---|---|---|
| `Codex` | 科德克斯 | OpenAI 官方推出的 AI 编程智能体（含桌面端、终端 CLI 和云端版） |
| `CLI` | 西艾欧艾 | Command Line Interface，在黑框终端里敲命令交互的版本 |
| `workspace-write` | 沃克思佩斯 莱特 | Codex 里的「工作区内修改」沙箱档位，对应 DSH 同名权限 |
| `CODEX_HOME` | 科德克斯 霍姆 | Codex 存放全局配置和全局 `AGENTS.md` 的目录（默认 `~/.codex`） |

---

## 分段参考

| 时间 | 屏幕画面 | 口播要点 |
|---|---|---|
| 00:00–01:10 | 展示「上层外壳换掉 vs 底层 5 块通用底座不变」分层架构图 | 直击学员最大顾虑：工具半年一换，学这门课会不会过时？今天拿 OpenAI Codex 当场验证——**壳换了，脑子和文件一个字不用改！** |
| 01:10–03:30 | 展示「DSH ⇄ Codex 概念一一对照表」 | 逐行带读：安装入口、登录计费、项目说明书、三档权限、切模型、Git 验收——特别点出「就算以后换 Claude Code，概念照样 100% 通用」。 |
| 03:30–05:30 | 切到官方中文文档 `AGENTS.md` 页面与 `Codex CLI` 页面截图 | 放大指给观众看两处官方实锤：① `~/.codex/AGENTS.md` + 项目根 `AGENTS.md` + `32 KiB` 上限（和 5.2 课讲的几乎一模一样）；② `/init`、`/permissions`、`/model` 斜杠指令。 |
| 05:30–07:20 | 演示（或分步走读）在 Codex 里打开 `ai-radar`、复用同一份 `practice/AGENTS.md` 给 `release-radar.yaml` 增加 `psf/requests` 并用 `git diff` 验收 | 强调重点：**你的项目骨架、`.venv`、YAML 配置、`AGENTS.md` 和 Git 仓库完全不绑定任何一家 AI 厂商**，想切随时切。 |
| 07:20–08:30 | 展示第 5 节 3 个迁移小问题 | 停顿 5 秒，点出关键答案：全局路径 `~/.dsh` vs `~/.codex` 差异 / 严禁开 `danger-full-access` 跑桌面 / 找不到 Diff 按钮直接敲 `git diff`！ |
| 08:30–09:05 | 预告正课最后一讲 7.2《DSH vs Codex：怎么选、怎么搭配》 | 既然两边都会用了，下节帮大家算清账单、网络和场景，挑出最适合自己的主力搭配。 |

---

## 录制注意事项

- 如果本机实机演示 ChatGPT 桌面端或 Codex CLI，录制前请隐藏登录邮箱、账单余额与 `OPENAI_API_KEY` 环境变量。
- 强调「不要在任何工具里图省事直接开全放开权限」，把 1.5 课的安全意识一以贯之。
