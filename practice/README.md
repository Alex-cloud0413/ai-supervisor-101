# ai-radar（AI 选型与每日情报雷达）

> 《给 AI 当监工》全课贯穿实战项目的标准工程目录。所有练习数据均采自免 Key 公开接口的真实离线快照，不含任何私人信息或公司机密。

## 目录结构

```text
practice/
├── README.md                 # 项目总说明书（你正在看的这份）
├── requirements.txt          # Python 第三方库依赖清单（openpyxl、PyYAML）
├── config.yaml               # 人类可读的参数控制面板（汇率、关键词、热度门槛）
├── .env.example              # API 密钥环境变量模板（复制为 .env 后再填真实密钥）
├── data/                     # 原始公开数据快照（只读，绝不直接覆盖）
│   ├── openrouter-models-2026-11-24.json
│   └── hn-frontpage-2026-11-24.json
├── scripts/                  # 可复用的 Python 脚本
│   ├── fetch_snapshots.py    # 从公开免 Key 接口刷新最新快照
│   ├── build_top10.py        # M2 教学参考脚本：筛选多模态商用付费 Top 10 导出 Excel
│   └── daily_briefing.py     # M3–M5 参考脚本：读取 config.yaml 生成每日 AI 情报简报
└── output/                   # 程序生成的成品目录（已加入 .gitignore，不提交进 Git）
```

## 快速运行

### 1. 创建并激活虚拟环境，安装依赖

Mac / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r practice/requirements.txt
```

Windows（PowerShell）：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r practice/requirements.txt
```

### 2. 运行脚本

```bash
# 生成商用实时付费多模态模型 Top 10 Excel（输出至 practice/output/模型比价Top10.xlsx）
python3 practice/scripts/build_top10.py

# 按 practice/config.yaml 口径生成每日 AI 情报简报（输出至 practice/output/daily-briefing.md）
python3 practice/scripts/daily_briefing.py

# 可选：联网刷新最新 OpenRouter 与 Hacker News 公开快照（写入 practice/data/）
python3 practice/scripts/fetch_snapshots.py
```

## 安全约定

- 真实 API Key 仅写在本地 `.env`（复制 `.env.example` 生成），绝不硬编码进 `.py` 或提交到 GitHub。
- `data/` 下的原始快照只读不改，所有运行结果一律写入 `output/`。
