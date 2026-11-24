# 2.7 库与 `pip install`

> 学习目标：分清 Python 自带标准库和第三方库，看懂代码顶部的 `import` 与审批框里的 `pip install`，AI 申请装包时能 5 秒判断「这包认不认识、安不安全、要不要批」。
>
> 演示环境：Python `3.12.16`、`pip`、`openpyxl 3.1.5`，对照仓库 `practice/scripts/fetch_snapshots.py`（纯标准库）和 `practice/scripts/build_top10.py`（需第三方库）。

---

## 1. 为什么一个脚本直接能跑，另一个非要 `pip install`？

把配套仓库里的两份脚本摆在一起，你会发现一个有意思的差别：

- 运行 `python3 practice/scripts/fetch_snapshots.py`（联网拉取 OpenRouter 和 Hacker News 公开快照）：**装好 Python 就能直接跑，什么都不用额外装**。
- 运行 `python3 practice/scripts/build_top10.py`（把筛选结果写成带配色、列宽和货币格式的 Excel）：如果在刚装好 Python 的新电脑上直接跑，终端立刻蹦出一句红错 `ModuleNotFoundError: No module named 'openpyxl'`，AI 马上弹窗问你能不能执行 `pip install openpyxl`。

为什么有的功能开箱即用，有的非要让 AI 去网上装包？以后 AI 动不动弹出 `pip install xxx` 要你审批，怎么一眼分清它是「正常办公组件」还是「来路不明的可疑包」？

这一课专门把 Python 里的 **库（Library / Package）** 和 **`pip`** 讲透。

---

## 2. 系统位置：`import` 和 `pip` 在整个工作流里扮演什么角色

用手机打个最直白的比方：Python 本体好比刚拆封的新手机，自带电话、短信、计算器（**标准库**）；想剪视频、做复杂 Excel 报表，得去应用商店下载专业 App（**第三方库**），而 `pip` 就是 Python 的官方应用商店。

```
AI 准备写脚本（例如生成带样式的 Excel 比价表）
      ↓
检查 Python 自带标准库够不够用：
  ├── 够用（读 JSON、拼路径、拿日期）→ 直接在顶部写 import json，零安装
  └── 不够用（写 .xlsx 配色表、做透视统计）→ 走 pip install openpyxl 去 PyPI 商店下载  ← 【本课位置】
      ↓
包安装进电脑后，脚本顶部 import openpyxl 就能正常调用
```

---

## 3. 讲清楚：标准库 vs 第三方库、`import` 写法和监工防投毒清单

### 3.1 标准库 vs 第三方库

- **标准库（Standard Library）**：安装 Python 时官方直接打包附送的基础工具箱，**永远不需要 `pip install`**，也不用担心安全来源。在 `ai-radar` 里高频露脸的有：
  - `json`（读写 `.json` 快照）
  - `pathlib`（拼装跨系统文件路径）
  - `csv`（读写纯文本逗号分隔表）
  - `datetime`（拿今天日期，比如生成 `2026-11-24` 文件名）
  - `urllib.request`（发基础网络请求，像 `fetch_snapshots.py` 就只靠它）
  - `os`（看环境变量和系统目录）
- **第三方库（Third-Party Package）**：全球开源社区写好、发布在官方仓库 **PyPI（Python Package Index，pypi.org）** 上的专业工具，需要通过 `pip install <包名>` 下载到电脑里才能 `import`。

### 3.2 职场办公 6 个高频白名单第三方库

日常让 AI 帮你做表、整理文档、抓公开数据、画图，90% 的 `pip install` 逃不出下面这 6 个老熟人：

| 包名（`pip install` 写法） | 代码里常见 `import` 写法 | 干什么用 | 典型场景 |
|---|---|---|---|
| `openpyxl` | `import openpyxl` | 读写带样式、公式、列宽的 `.xlsx` Excel | `build_top10.py` 生成模型比价表 |
| `pandas` | `import pandas as pd` | 表格清洗、合并、透视汇总（代码版超级 Excel） | 合并多月报表、按厂商分组统计均价 |
| `requests` | `import requests` | 比自带 `urllib` 更顺手的联网抓公开数据工具 | 调 OpenRouter / Hacker News / GitHub API |
| `pyyaml` | `import yaml` | 读写 `.yaml` 配置文件（注意包名和 `import` 名不同！） | M3 读取 `config.yaml` 配置清单 |
| `python-docx` | `import docx` | 读写 `.docx` Word 文档 | 自动生成周报、合同模板批量填字 |
| `matplotlib` | `import matplotlib.pyplot as plt` | 把数据画成折线图、柱状图导出 PNG | 给汇报材料自动配价格对比图 |

**顺手破一个常见疑惑**：你会注意到 `pyyaml` 装的时候叫 `pyyaml`，写代码时叫 `import yaml`；`python-docx` 装的时候带 `python-`，写代码时叫 `import docx`。这是历史命名习惯，并不是 AI 写错了。

### 3.3 脚本顶部的 3 种 `import` 写法，一眼读懂

```python
import openpyxl                     # ① 整箱搬进来：后面用 openpyxl.Workbook()
from pathlib import Path            # ② 只从 pathlib 箱子里拿 Path 这一件工具
import pandas as pd                 # ③ 整箱搬进来并起个短外号 pd，少打几个字母
```

### 3.4 监工批 `pip install` 的 2 个安全守则

1. **防「包名拼写投毒」（Typosquatting）**：PyPI 上任何人都能上传包，黑客常抢注少打一个字母或把字母 `l` 换成数字 `1` 的假包（例如把 `requests` 写成 `reqeusts`，把 `openpyxl` 写成 `openpyx1`）。**审批弹窗看到 `pip install` 时，一定逐字母核对包名拼写！**
2. **优先认准 `python3 -m pip install`（Windows 用 `python -m pip install`）**：电脑装了多个 Python 版本时，直接敲 `pip install` 有时会装进另一个 Python 里，导致脚本依然报找不到库；加上 `-m` 能保证「装给当前跑脚本的同一个 Python」。

（注：多个项目混用不同版本库怎么办？M3 的 **3.2 课《依赖与环境》** 会专门讲 `requirements.txt` 和虚拟环境隔离，这一课先认清库和安全装包。）

---

## 4. 现场看：对比两份仓库脚本 + 用 `pip show` 验明正身

先对照仓库里两份真实脚本的顶部 `import` 区域：

```python
# practice/scripts/fetch_snapshots.py（全部是 Python 自带标准库，0 外部安装）
import json
import urllib.request
from datetime import date
from pathlib import Path
```

```python
# practice/scripts/build_top10.py（前 2 行是标准库，后 2 行借用第三方库 openpyxl）
import json
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
```

如果你批完安装，或者想确认电脑里装的 `openpyxl` 到底是什么版本、什么开源协议，在终端敲一行只读查询命令 `python3 -m pip show openpyxl`，本机实测输出如下：

```text
Name: openpyxl
Version: 3.1.5
Summary: A Python library to read/write Excel 2010 xlsx/xlsm files
Home-page: https://openpyxl.readthedocs.io
Author: See AUTHORS
License: MIT
Location: /opt/pyenv/versions/3.12.16/lib/python3.12/site-packages
Requires: et-xmlfile
```

扫 3 个字段就能彻底放心：
- `Name` 和 `Summary`：名字拼写准确，简介明确写着读写 Excel 表格；
- `License: MIT`：宽松商用友好的开源协议；
- `Requires: et-xmlfile`：只顺带依赖 1 个轻量辅助小包，没有夹带一堆乱七八糟的东西。

---

## 5. 你来读：AI 弹出 4 条 `pip install` 审批，哪两条批、哪两条拒？

假设你在 `ai-radar` 里让 AI 加一个「按厂商统计平均价格并画柱状图」的功能，下面 4 条装包命令依次跳进审批框：

1. `python3 -m pip install pandas`
2. `pip install openpyx1`
3. `python3 -m pip install requests`
4. `pip install git+https://unknown-user.invalid/super-fast-excel.git`

停下来想 10 秒：哪 **2 条** 可以点「允许一次」，哪 **2 条** 必须立刻点「拒绝」？

**判断思路**：
1. **允许一次**。`pandas` 是最常见的数据表格分析库，而且用了稳妥的 `python3 -m pip install` 写法。
2. **立刻拒绝！** 盯紧最后一个字符——它是数字 **`1`**（`openpyx1`），不是小写字母 `l`（`openpyxl`）！这是典型的拼写投毒或手滑拼错，绝不能批。
3. **允许一次**。`requests` 拼写正确，是抓取公开接口最常用的成熟第三方库。
4. **立刻拒绝！** `git+https://...` 表示绕过官方 PyPI 商店，直接从陌生人的仓库拉未审核代码安装执行，写 Excel 用成熟的 `openpyxl` 就够了，绝不装来路不明的外部仓库包。

---

## 6. 小检查（3 道判断题）

1. `json`、`pathlib`、`datetime` 属于 Python 自带标准库，装好 Python 就能直接 `import`，不需要先运行 `pip install`。（对 / 错）
2. 审批框里看到 `pip install reqeusts`，因为看起来很像 `requests`，可以直接点「允许一次」。（对 / 错）
3. `python3 -m pip show openpyxl` 是一条只读查看命令，用来查看已安装包的版本、简介和协议，不会修改或删除电脑文件。（对 / 错）

---

## 7. 下一课

读懂了脚本骨架、变量、列表字典、`if`、`for`、函数和库，你在「代码顺风顺水」的时候已经完全看得明白。但真正用 AI 干活时，最常让人心慌的是屏幕突然飙出一大片英文红错。下一课就是 M2 压轴课 **2.8《读懂报错》**，教你「从最后一行往上读」三步法，把报错精准喂给 AI 一次修对。

---

## 小检查答案

1. **对**。标准库随 Python 解释器内置，开箱即用。
2. **错**。`reqeusts` 把 `u` 和 `e` 拼反了，正是黑客常用的包名投毒（Typosquatting）陷阱，必须立刻点「拒绝」并纠正为 `requests`。
3. **对**。`pip show` 只查询本地已安装包的元信息，不联网也不改文件。

---

## 参考与事实边界

- **实际操作结果**：本课对比的两份 `import` 代码摘自仓库 `practice/scripts/fetch_snapshots.py` 和 `practice/scripts/build_top10.py`；`pip show openpyxl` 输出在 `Python 3.12.16` 环境实测获得（`openpyxl 3.1.5`，MIT 协议）。
- **官方资料**：
  - Python 官方标准库目录：[The Python Standard Library](https://docs.python.org/3/library/index.html)；
  - Python 官方包安装指南：[Installing Python Modules (`pip`)](https://docs.python.org/3/installing/index.html) 与 [PyPI](https://pypi.org/)。
- **作者说明**：第 5 节的 `openpyx1` 与 `unknown-user.invalid` 为模拟包名投毒与陌生源安装的安全演练案例。
