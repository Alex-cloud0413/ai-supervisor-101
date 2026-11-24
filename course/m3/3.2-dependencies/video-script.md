# 3.2 录播参考脚本："在我电脑上能跑"：依赖与环境

> 建议时长：8–10 分钟（现场新建空白 `.venv`、按 `requirements.txt` 装包并跑通 `daily_briefing.py`，以下为口播要点与屏幕节点，不作逐字稿）。

## 中英术语读法

| 术语 | 读法 | 首次出现时的口头解释 |
|---|---|---|
| Dependency | 中文直接说「依赖」 | 项目正常运行所必须借用的外部库 |
| `requirements.txt` | 瑞快尔门茨点 T-X-T | 项目的第三方库采购清单 |
| Virtual Environment / `.venv` | 虚拟环境 / 点 V-E-N-V | 给单个项目隔出来的独立工具间 |
| `activate` / `deactivate` | 激活 / 退出 | 走进虚拟环境 / 退出虚拟环境 |
| `pyproject.toml` | P-Y-project 点托默 | 现代 Python 项目的新标准配置文件 |
| `package.json` | 派克基点杰森 | Node.js / 前端项目的依赖清单 |

---

## 0:00 – 0:50｜开场 Hook（还原「在我电脑上能跑」魔咒）

- **屏幕画面**：终端现场展示刚换新环境跑 `daily_briefing.py` 蹦出 `ModuleNotFoundError: No module named 'yaml'`。
- **口播要点**：
  - 「自己电脑上跑得好好的，发给同事一跑就缺包；或者老项目要旧版库、新项目要新版库，装了一个崩了另一个。今天两件搭档彻底终结这个问题：`requirements.txt` 和 `.venv`。」

## 0:50 – 3:00｜办公楼工具间比喻 + `requirements.txt` 写法

- **屏幕画面**：打开 `practice/requirements.txt`（只有 4 行），指出 `openpyxl>=3.1.5,<4.0` 和 `PyYAML>=6.0.2,<7.0`，顺带对比双等号 `==` 锁版本。
- **口播要点**：
  - 解释 `-r` 参数：`pip install -r requirements.txt` 等于把采购单直接交给应用商店一次性配齐。

## 3:00 – 5:45｜Mac / Windows 双系统实操建 `.venv` 并跑通

- **屏幕画面**：并列展示 Mac（`source .venv/bin/activate`）和 Windows PowerShell（`.\.venv\Scripts\Activate.ps1`），在终端现场敲三行命令，放大行首亮起的 `(.venv)`，再展示 `pip list`（自动顺带装了 `et_xmlfile 2.0.0`）和 `du -sh .venv`（`20M`），最后跑通 `daily_briefing.py`。
- **口播要点**：
  - **重点破误解**（指着 `20M` 的 `.venv`）：「千万别把 `.venv` 发给同事或传上 GitHub！Mac 建的 `.venv` 到 Windows 根本跑不动，而且装了 pandas 动辄几百兆。只交 100 字节的 `requirements.txt`，让对方 5 秒原地重建！」
  - 顺口提一句 Windows PowerShell 激活报错时的备选免激活跑法：`.\.venv\Scripts\python.exe 脚本名.py`。

## 5:45 – 7:30｜逛 GitHub「一眼认出表」+ 实战找错 + 下集预告

- **屏幕画面**：快速过一遍 `pyproject.toml`、`uv.lock`、`package.json` 对照表；再贴出第 5 节藏着 `.venv/`（1,842 个文件）且漏更新 `requirements.txt` 的待提交列表。
- **口播要点**：
  - 提醒观众：以后每次让 AI 新装了一个第三方库，顺嘴补一句「记得同步更新 `requirements.txt`」。
  - 预告 **3.3《Markdown / JSON / YAML 三件套》**：刚才终端说「已按 `config.yaml` 生成 `daily-briefing.md`」，下节课彻底分清这三种格式，教你不动一行 Python 代码直接改配置文件！

---

## 录制注意事项

- 录屏结束后记得把演示临时创建的 `.venv/` 保持在 `.gitignore` 状态，不要意外提交。
- 如果在 Windows 实机录播，顺手演示一次 `.\.venv\Scripts\Activate.ps1` 激活后行首出现绿色 `(.venv)` 的真实画面。
