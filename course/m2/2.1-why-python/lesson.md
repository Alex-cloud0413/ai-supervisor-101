# 2.1 为什么 AI 爱用 Python

> 学习目标：认出 `.py` 脚本文件，说清 AI 为什么优先写 Python 来干数据处理活，并且会自己或让 AI 安全运行一份 `.py` 脚本。
>
> 演示环境：Python `3.12.16`（Mac / Windows 通用），延续 `ai-radar` 项目，实测运行仓库参考脚本 `practice/scripts/build_top10.py` 与 470 个真实 OpenRouter 模型快照。

---

## 1. Excel 能算的账，AI 干嘛非要写 `.py`？

在 0.1 课里，我们只是让 AI 挑出最便宜的 10 个支持看图的大模型、做成 Excel。结果 AI 最后没停在聊天框里，而是在 `ai-radar` 文件夹里留下了一个以 `.py` 结尾的文件：`build_top10.py`。

很多刚上手 AI 编程工具的职场人，心里都会冒出同一个问号：「我平常拿 Excel 也能筛选、算汇率、排个序，干嘛非要让 AI 写一段代码？」

拿 `ai-radar` 这份真实数据算笔时间账就明白了：

- `data/openrouter-models-2026-11-24.json` 是一个 `1.4 MB` 的嵌套 JSON 文件，里面装着 **470 个模型**，每个模型下面还嵌套着价格字典、输入输出模态列表。直接拖进 Excel，连正常打开成表格都要折腾半天；
- 就算你费劲导进 Excel，想同时排除 `~` 动态别名、`:free` 免费版、`:batch` 离线版、输出含音频的音乐模型，再把每 Token 美元字符串折算成每百万 Token 人民币均价，手工拉公式少说花 20 分钟，还极容易漏行；
- 换成一份写好的 `build_top10.py`：敲一行运行命令，**不到 1 秒**就把 470 个模型按 4 道口径筛出 207 个合规模型，排好前 10 名、套好表头配色、生成 `output/模型比价Top10.xlsx`。下周拉回来新快照，**一字不改再跑一遍，口径完全一致，零手工出错**。

所以 AI 爱写 Python，不是为了炫技——而是因为把一次性聊天变成可复用的 `.py` 脚本，才是让电脑真正替你干重复劳动的最短路径。从这一课开始进入 **M2 读懂 Python**：你不需要背语法从头敲代码，只需要像看施工图纸一样，扫一眼就看懂 AI 写出来的脚本在干什么。

---

## 2. 系统位置：`.py` 脚本和 Python 解释器怎么配合

回到整条工作链路，看看 `.py` 文件和我们在 1.2 课见过的 `python3` 命令是什么关系：

```
你下达任务（例如「筛选商用实时付费 Top 10 并导出 Excel」）
      ↓
模型把你的业务口径写成一份纯文本图纸：build_top10.py   ← 【本课位置】
      ↓
Harness 在终端敲下运行命令：python3 build_top10.py
      ↓
Python 解释器逐行读懂这份图纸，去读 data/、算价格、写出 output/*.xlsx
      ↓
结果回到硬盘，终端把打印摘要或报错传回给模型和你
```

把这两个词拆开记牢，M2 后面 7 课就不会混：

- **`.py` 文件（Python 脚本）**：本质上就是一份**纯文本文件**，里面用英文关键词写满操作步骤。你用记事本、VS Code 甚至终端里的 `cat` 都能直接打开看它的字，它自己不会动。
- **Python 解释器（`python3` 或 `python`）**：装在电脑里的「翻译兼执行官」。你敲 `python3 build_top10.py`，就是在把图纸递给解释器，让它按顺序从头跑到尾。

---

## 3. 讲清楚：AI 最偏爱 Python 的 3 个实在原因

除了 Python，市面上还有 JavaScript、Java、C++、Go 等几十种编程语言。但只要你让 AI 处理表格、洗 JSON、抓公开数据、整理文档，十次里有九次它会主动选 Python，原因非常现实：

1. **读起来最接近普通英语句子**：比如 `if ":batch" in model_id:`（如果模型 ID 里包含 `:batch`）、`for model in models:`（对模型列表里的每一个模型），哪怕没学过编程，连猜带蒙也能读懂七八成。这对当监工的你来说是天然福利。
2. **现成「免费工具箱」极其齐全**：读 JSON 用自带的 `json`，做精美 Excel 用 `openpyxl`，做大数据统计用 `pandas`，抓网页接口用 `urllib` 或 `requests`，处理 Word 和 PDF 也都有现成工具包。AI 不用从零造轮子，拼几十行代码就能交活。
3. **AI 训练时见过海量 Python 代码**：写起来最稳、踩坑最少，报错信息也最直白，出了问题 AI 自己读完报错大多能一两轮修好。

**最常见的误解**：觉得「学 Python 就是背语法、自己从空白文件写程序」。在《给 AI 当监工》里，你完全不用自己手写。你拿到的永远是 AI 已经写好的 `.py` 文件——你需要的是**「体检式阅读」能力**：先看骨架，再盯关键参数和条件。

### 任何一份 `.py` 脚本，都可以按这 4 段「体检骨架」来扫

打开一份 AI 刚写完的 `.py` 文件，不管它有 50 行还是 200 行，从上往下基本都是这 4 块：

| 区域 | 常见长相 | 它的作用 | 监工看什么 |
|---|---|---|---|
| ① 顶部工具声明 | `import json`、`import openpyxl` | 声明这份脚本要借用哪些工具箱 | 有没有出现来路不明的陌生库 |
| ② 顶部配置变量 | `EXCHANGE_RATE = 7.2`、`TOP_N = 10` | 把文件路径、汇率、数量集中放在显眼处 | 路径对不对、汇率/条数是不是你要的 |
| ③ 功能模块 | 若干个 `def xxx():` | 把「读文件」「过滤」「算价」「导表」拆成一个个小步骤 | 扫一眼 `if` 过滤口径有没有漏或写反 |
| ④ 底部启动入口 | `if __name__ == "__main__":` | 整份脚本的「总开关」，按顺序串联上面各块 | 确认它最后写进了 `output/`，没覆盖原始 `data/` |

---

## 4. 现场看：把 `build_top10.py` 骨架摊开并跑一遍

配套仓库已经把 0.1 课的脚本整理成了清晰的参考版 `practice/scripts/build_top10.py`（共 188 行）。先把它的 4 段骨架缩略出来看一眼：

```python
# ① 顶部工具声明（第 10–14 行）
import json
from pathlib import Path
import openpyxl

# ② 顶部配置变量（第 17–21 行）
DATA_PATH = BASE_DIR / "data" / "openrouter-models-2026-11-24.json"
OUTPUT_PATH = BASE_DIR / "output" / "模型比价Top10.xlsx"
EXCHANGE_RATE = 7.2
TOP_N = 10

# ③ 功能模块（第 24–170 行，共 5 个打包好的步骤）
def load_models(json_path): ...               # 读 JSON 快照
def is_valid_chat_vision_model(model): ...    # 4 道筛子过滤模型
def calc_cny_pricing(model, exchange_rate): ...  # 美元折算人民币均价
def select_top_models(models, ...): ...       # 批量筛选、排序取前 10
def save_excel(top_models, ...): ...          # 写入 Excel 表格

# ④ 底部启动入口（第 173–188 行）
def main():
    models = load_models(DATA_PATH)
    top_models = select_top_models(models, exchange_rate=EXCHANGE_RATE, top_n=TOP_N)
    save_excel(top_models, OUTPUT_PATH, exchange_rate=EXCHANGE_RATE)
    ...
```

是不是一下子就不觉得 188 行代码吓人了？它就像一张只有 4 栏的菜单：上面摆原料和参数，中间列做法，底下按顺序下锅。

### 怎么让它真正跑起来？（两种方式）

- **方式一（最省心，在 DeepSeek Harness 里说人话）**：直接在对话框发「帮我运行 `practice/scripts/build_top10.py`，把终端输出结果贴给我看」，弹窗审批确认命令无误后点「允许一次」。
- **方式二（自己在终端敲一行）**：先 `cd` 进项目根目录，再按系统敲：
  - **Mac / Linux**：`python3 practice/scripts/build_top10.py`
  - **Windows（PowerShell）**：`python practice/scripts/build_top10.py`（如果电脑装了多版本也可以用 `py practice/scripts/build_top10.py`）

在本机实测运行 `python3 practice/scripts/build_top10.py`，终端立刻打印出真实结果：

```text
已读取 470 个模型，筛出前 10 名，保存至 output/模型比价Top10.xlsx
Top 1: google/gemma-3-4b-it | 综合均价 ¥0.3240/M (输入 ¥0.2880 / 输出 ¥0.3600)
Top 2: nex-agi/nex-n2.5-mini | 综合均价 ¥0.4500/M (输入 ¥0.1800 / 输出 ¥0.7200)
Top 3: qwen/qwen3.7-flash | 综合均价 ¥0.5760/M (输入 ¥0.2160 / 输出 ¥0.9360)
Top 4: tencent/hy4-flash | 综合均价 ¥0.6318/M (输入 ¥0.2520 / 输出 ¥1.0116)
Top 5: google/gemma-3-12b-it | 综合均价 ¥0.7200/M (输入 ¥0.3600 / 输出 ¥1.0800)
```

同时，`practice/output/模型比价Top10.xlsx` 自动生成完毕，原始的 `practice/data/openrouter-models-2026-11-24.json` 丝毫未动。

---

## 5. 你来读：10 秒扫完这份陌生的 `.py` 脚本

假设 AI 在你的 `ai-radar` 工作区里新建了一个 `preview_hn.py`，准备先看一眼 Hacker News 首页热点快照。你在右侧代码面板里看到下面 9 行：

```python
import json
from pathlib import Path

DATA_PATH = Path("data/hn-frontpage-2026-11-24.json")

with DATA_PATH.open("r", encoding="utf-8") as f:
    payload = json.load(f)

hits = payload.get("hits", [])
print("今日热帖总数:", len(hits))
print("榜首标题:", hits[0]["title"])
```

停下来想 10 秒：
1. 这份脚本准备干什么？
2. 它有没有修改或删除你电脑里的任何文件？放心让 AI 运行吗？

**判断思路**：
1. 顶部只借用了 Python 自带的 `json` 和 `pathlib`，然后以只读模式（`"r"`）打开 `data/hn-frontpage-2026-11-24.json`，打印出热帖总数和第 1 条的标题（实测会打印 `今日热帖总数: 30` 和 `榜首标题: Nvidia Reinstates Jensen Huang as CEO`）。
2. 全程只有读（`"r"`）和屏幕打印（`print`），没有任何写文件、删文件或联网动作，完全安全，可以放心运行。

---

## 6. 小检查（3 道判断题）

1. `.py` 文件是一种特殊加密格式，必须装专业编程软件才能打开查看里面的文字。（对 / 错）
2. 同样是筛选 470 个模型算人民币均价，让 AI 写成 `.py` 脚本的好处是：下周换一份新快照，跑同一份脚本就能按完全一致的口径在 1 秒内出结果。（对 / 错）
3. 在 Mac 和 Windows 终端运行同一份脚本时，常见命令分别是 `python3 脚本名.py` 和 `python 脚本名.py`。（对 / 错）

---

## 7. 下一课

认清了 `.py` 脚本的 4 段骨架，下面我们从最顶上、监工改得最勤的那一块拆起。下一课 **2.2《变量：给数据贴标签》**，带你一眼看懂 AI 在 Diff 里改了哪个设置值、为什么把数字套上引号就会算崩。

---

## 小检查答案

1. **错**。`.py` 是纯文本文件，记事本、文本编辑、VS Code 或终端 `cat` 都能直接打开阅读。
2. **对**。把一次性分析沉淀成脚本，既省去重复手工操作，也避免了每次跟 AI 重新沟通导致的口径漂移。
3. **对**。Mac / Linux 常用 `python3`，Windows 常用 `python`（或 `py`），背后调用的都是本机的 Python 解释器。

---

## 参考与事实边界

- **实际操作结果**：本课展示的脚本骨架和终端输出结果均在 `Python 3.12.16` 环境下实际运行仓库脚本 `practice/scripts/build_top10.py`（读取 `practice/data/openrouter-models-2026-11-24.json`）获得。
- **官方资料**：Python 官方入门文档：[The Python Tutorial](https://docs.python.org/3/tutorial/index.html)。
- **作者说明**：第 5 节 `preview_hn.py` 为配合 `practice/data/hn-frontpage-2026-11-24.json` 设计的只读练习片段，其输出标题来自该真实快照第 1 条记录。
