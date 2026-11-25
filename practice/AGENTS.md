# AGENTS.md — ai-radar 项目说明书

本文件写给在本项目（`ai-radar`）中工作的 AI 编程工具（DeepSeek Harness、OpenAI Codex、Claude Code 等）。开始任何修改前，请先读完本文件。

## 1. 项目定位与目录分工

`ai-radar` 是面向职场团队的「AI 模型选型与每日情报雷达」，核心目录分工如下：

- `data/`：公开免 Key 数据快照（OpenRouter 模型目录 + Hacker News 首页热点）。**只读原料仓**。
- `scripts/`：正式可复用 Python 脚本（`fetch_snapshots.py`、`build_top10.py`、`daily_briefing.py`）。
- `config.yaml`：人类可读的参数控制面板（汇率、排除前后缀、HN 热度门槛与关键词）。
- `output/`：脚本生成的成品目录（Excel 比价表、Markdown 简报），可随时重算，不进 Git。
- `requirements.txt` / `.env.example`：第三方库清单与密钥空模板。

## 2. 运行与自检命令

修改代码或配置后，必须用项目虚拟环境实测跑通对应脚本，再汇报完成：

```bash
# 多模态商用比价 Top 10（输出 output/模型比价Top10.xlsx）
python3 scripts/build_top10.py

# 每日 AI 情报简报（读取 config.yaml，输出 output/daily-briefing.md）
python3 scripts/daily_briefing.py
```

验收时请向我汇报：实际运行的命令、终端退出码、输出文件路径，以及本次命中的模型条数与热点条数。

## 3. 代码与配置约定

1. **参数与逻辑分离**：汇率、关键词、条数上限、追踪的开源仓库列表等会变化的参数，统一写进 `config.yaml`，不要硬编码进 `.py` 脚本。
2. **数据口径一致**：商用模型比价必须继续过滤 `~` 前缀（动态路由）、`:free` / `:batch` 后缀以及输入或输出价格 `<= 0` 的条目。
3. **依赖同步更新**：如果新安装了第三方 Python 库，必须同步更新 `requirements.txt`。
4. **保持中文输出清晰**：报错提示、简报标题和 `config.yaml` 注释使用简洁中文。

## 4. 绝对红线（严禁触碰）

- **绝不修改或覆盖 `data/` 下的原始快照文件**（除非我明确要求运行 `fetch_snapshots.py` 刷新快照）。
- **绝不把任何真实 API Key 或 Token 写进代码、`config.yaml` 或提交进 Git**；密钥一律通过本地 `.env` 环境变量读取。
- **绝不提交 `.env`、`.venv/` 或 `output/`**；不要运行 `git reset --hard`、`rm -rf` 等不可逆破坏命令。
- **涉及跨文件修改或新增功能时，先出书面计划并等我确认，再动手改文件**。

## 5. 协作与交付习惯

- 做大改动前优先在独立分支（如 `feat/...` 或 `agent/...`）操作，不要直接破坏 `main`。
- 完成后简要列出修改的文件清单（如 `git diff --stat`），说明如何验证，便于我 15 秒验收。
