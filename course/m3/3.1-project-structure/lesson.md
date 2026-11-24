# 3.1 项目文件夹的标准结构

> 学习目标：看懂一个标准 AI 自动化项目文件夹的 5 个分区（说明与配置、原始数据 `data/`、脚本 `scripts/`、产物 `output/`、隐藏/隔离目录），拿到陌生项目时能在 30 秒内摸清「文件各放哪、哪些不能动」。
>
> 演示环境：延续 `ai-radar` 项目，直接对照仓库升级后的标准工程目录 `practice/`（含 `README.md`、`config.yaml`、`requirements.txt`、`.env.example`、`data/`、`scripts/` 与运行生成的 `output/`）。

---

## 1. 两周后连你自己都分不清「哪个是终版」的文件夹

很多职场人刚学会让 AI 写脚本时，会把所有东西一股脑塞进同一个文件夹，两周后打开一看全是这种画风：

```text
桌面/AI工具/
├── openrouter_new.json
├── openrouter_final_2.json
├── test.py
├── test_fix_v2.py
├── run_final.py
├── 模型比价_终版.xlsx
├── 模型比价_终版_真终版.xlsx
└── key.txt
```

这种「大杂烩文件夹」很快会出 3 件事：
1. 你自己忘了该跑 `test_fix_v2.py` 还是 `run_final.py`；
2. AI 进工作区扫目录时也被一堆旧脚本带偏，把新代码改到了过期文件里；
3. 最要命的是，某天想把整个文件夹打包发给同事或传上 GitHub，结果把 `key.txt` 和 50 MB 临时表一起发了出去。

从这一课进入 **M3 一个项目长什么样**。我们不再只盯着单份 `.py` 脚本，而是把 `ai-radar` 整理成一套干净、可交接、可长期维护的标准项目文件夹。

---

## 2. 系统位置：项目文件夹是 AI、配置和数据的「共同施工工地」

前面 M1–M2 我们认识了路径、脚本和报错；现在把整座工地的分区图画出来：

```
ai-radar/（工作区根目录）                           ← 【本课位置】
├── 门厅（根目录核心文件）
│     ├── README.md          → 给人看的总说明书（干嘛用、怎么跑）
│     ├── requirements.txt   → 给 pip 看的第三方库清单（3.2 课）
│     ├── config.yaml        → 给人改的参数控制面板（3.3 课）
│     ├── .env / .env.example→ 装 API 密钥的保险箱与空模板（3.4 课）
│     └── .gitignore         → 给 Git 看的不上传黑名单（防传密钥和临时产物）
├── 原料仓：data/            → 原始数据快照（只读！严禁覆盖）
├── 加工厂：scripts/         → 正式可复用的 .py 脚本
├── 成品库：output/          → 脚本跑出来的 Excel / Markdown 简报（可随时重算，不进 Git）
└── 独立工具间：.venv/       → 本项目专属的 Python 虚拟环境（不进 Git，3.2 课）
```

把这 5 块分区钉在脑子里，以后不管打开自己搭的工具，还是在 GitHub 上下载别人开源的项目，你 30 秒就能摸清门道。

---

## 3. 讲清楚：标准项目结构的 5 条铁律

| 分区 | 典型目录 / 文件 | 放什么 | 监工盯什么（底线规矩） |
|---|---|---|---|
| **① 门厅说明书与清单** | `README.md`、`requirements.txt`、`config.yaml`、`.env.example` | 项目用途、运行命令、依赖包、可调参数、密钥模板 | 根目录保持清爽，绝不把几十个数据表和临时脚本堆在根目录 |
| **② 原料仓（只读）** | `data/`（常见也叫 `raw/`、`input/`） | 原始公开快照、业务原始表 | **铁律：只读不改**。任何清洗和统计都另存到 `output/`，出事随时能重来 |
| **③ 加工厂（源码）** | `scripts/`（大型项目常叫 `src/`） | 正式跑通的 `.py` 脚本（如 `fetch_snapshots.py`、`build_top10.py`、`daily_briefing.py`） | 排查完口径留下的临时调试脚本及时清理，别让旧版 `v1`/`v2` 长期滞留 |
| **④ 成品库（可再生）** | `output/`（常见也叫 `dist/`、`reports/`） | 脚本生成的 `模型比价Top10.xlsx`、`daily-briefing.md` | 既然脚本 1 秒就能重新算出来，成品目录通常加进 `.gitignore`，不往 Git 仓库堆大文件 |
| **⑤ 隔离与保密区** | `.env`、`.venv/`、`.git/`、`.gitignore` | 真实密钥、独立虚拟环境、Git 历史存档 | **`.env` 和 `.venv/` 绝不上传 GitHub，也绝不随便打包发人** |

**最常见的误解**：以为「只有几百人研发团队的大软件才需要分目录，我自己写两三个脚本随便堆一起就行」。恰恰相反——当你用 AI 干活时，**目录越规范，AI 越不容易犯错**。因为 AI 每次开工前都会先 `ls` 扫描你的文件夹：看到清晰的 `data/`、`scripts/`、`output/` 和 `README.md`，它天然就知道去哪读原始数据、把新脚本写在哪、把结果存到哪，省掉一大半反复叮嘱的口水。

---

## 4. 现场看：升级后的 `ai-radar` 真实项目目录（`practice/`）

为了让你从 M3 到 M6 都能对着真文件练手，配套仓库的 `practice/` 目录已经正式升级成了完整的 `ai-radar` 工程骨架：

```text
practice/
├── README.md                 # 项目总说明书（目录导航 + 安装与运行命令）
├── requirements.txt          # 第三方库清单：openpyxl 与 PyYAML
├── config.yaml               # 人类参数控制面板：汇率、排除后缀、HN 关键词与热度门槛
├── .env.example              # 密钥模板（空占位符，安全提交）
├── data/                     # 原始公开快照（只读）
│   ├── openrouter-models-2026-11-24.json
│   └── hn-frontpage-2026-11-24.json
├── scripts/                  # 3 个各司其职的正式脚本
│   ├── fetch_snapshots.py    # 抓取最新公开快照写入 data/
│   ├── build_top10.py        # M2 参考脚本：导出多模态 Top 10 Excel
│   └── daily_briefing.py     # M3–M5 参考脚本：读 config.yaml 生成 Markdown 早报
└── output/                   # 运行脚本后自动生成（已列入 .gitignore，不提交）
    ├── 模型比价Top10.xlsx
    └── daily-briefing.md
```

顺手看一眼 `practice/README.md` 的骨架，感受一份合格的项目说明书该写清哪 3 件事：
1. **目录结构**：每个文件夹和文件是干嘛的；
2. **快速运行**：装依赖（`.venv` + `requirements.txt`）和跑脚本的复制即用命令；
3. **安全约定**：`.env` 不提交、`data/` 只读不改。

以后每次让 AI 帮你从零起一个新工具，第一句话就可以直接交代：「按 `README.md` + `config.yaml` + `requirements.txt` + `data/` + `scripts/` + `output/` 的标准结构建工作区。」

---

## 5. 你来读：帮同事给这个工作区做一次「30 秒结构诊断」

同事跟着教程搭了一个「周报自动汇总工具」，把目录截图发你帮忙把关：

```text
weekly-report/
├── 11月销售原表.xlsx
├── 11月销售原表_AI修改版.xlsx
├── make_report.py
├── make_report_old.py
├── .env
├── .venv/
└── .gitignore        （里面目前只写了 .DS_Store）
```

停下来想 10 秒：这个文件夹里至少藏着 **4 个** 马上要改的结构和安全隐患，你能一眼点出几个？

**判断思路**：
1. **原始数据和产物混在根目录，且没有 `data/` 和 `output/` 分区**：`11月销售原表.xlsx` 应该放进只读的 `data/`，生成的修改版放进 `output/`，防止 AI 一手滑直接覆盖原表。
2. **新旧脚本并存没清理**：`make_report.py` 和 `make_report_old.py` 混在根目录，应该把正式脚本移进 `scripts/`，删掉废弃旧版（靠 Git 留历史，不要靠 `_old` 堆文件）。
3. **缺少项目门厅三件套**：没有 `README.md`（过两周谁都不记得怎么跑）、没有 `requirements.txt`（换电脑不知道装什么库）、也没有 `.env.example` 模板。
4. **高危隐患：`.gitignore` 漏写了 `.env`、`.venv/` 和 `output/`！** 一旦传到 GitHub，真实 API 密钥（`.env`）、几十兆的虚拟环境（`.venv/`）和公司业务产出表全都会被直接打包上传！

---

## 6. 小检查（3 道判断题）

1. 在标准项目结构里，AI 生成出来的 Excel 报表和 Markdown 简报应该直接覆盖写回 `data/` 文件夹，这样最省硬盘空间。（对 / 错）
2. 根目录里的 `README.md` 写清了目录分工和运行命令，既方便自己两周后接手，也能让新打开会话的 AI 快速看懂项目规矩。（对 / 错）
3. `output/` 和 `.venv/` 都可以由脚本和依赖清单重新生成，因此通常应该列入 `.gitignore`，不提交进 Git 仓库。（对 / 错）

---

## 7. 下一课

目录分区规整好了，下一个职场高频坑马上到来：你把这套干净的 `ai-radar` 发给同事，对方一运行却跳出 `ModuleNotFoundError: No module named 'yaml'`——明明「在我电脑上好好的」！下一课 **3.2《"在我电脑上能跑"：依赖与环境》**，带你用 `requirements.txt` 和 `.venv` 彻底解决换电脑跑不通的问题。

---

## 小检查答案

1. **错**。`data/` 是原始原料仓，必须保持只读不改；所有加工成品一律写入 `output/`。
2. **对**。`README.md` 是整个项目的总说明书，对人和 AI 都同样高效。
3. **对**。代码、配置和依赖清单进 Git；可再生的大产物（`output/`）和本机虚拟环境（`.venv/`）放进 `.gitignore`。

---

## 参考与事实边界

- **实际操作结果**：本课展示的 `practice/` 目录树与 `README.md`、`config.yaml`、`requirements.txt`、`.env.example`、`scripts/daily_briefing.py` 均为配套仓库真实可运行文件，已在 `Python 3.12.16` 下实测运行并输出 `output/daily-briefing.md`。
- **官方资料**：Python 打包与项目结构官方参考：[Python Packaging User Guide](https://packaging.python.org/en/latest/)。
- **作者说明**：第 5 节的 `weekly-report/` 为汇总常见新手失误设计的结构诊断练习。
