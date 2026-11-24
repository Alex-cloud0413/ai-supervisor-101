# 3.3 Markdown / JSON / YAML 三件套

> 学习目标：分清 Markdown（`.md`）、JSON（`.json`）、YAML（`.yaml`）在真实项目里的分工，能自己动手安全修改 `config.yaml` 控制程序行为，并避开三种格式最常踩的语法坑。
>
> 演示环境：Python `3.12.16` + `PyYAML 6.0.4`，实测运行 `practice/scripts/daily_briefing.py`，直接对照 `practice/config.yaml`、两份 `.json` 原始快照与生成的 `output/daily-briefing.md`。

---

## 1. 不懂 Python 也能「改程序」的秘密：把参数搬进配置文件

在 2.2 课里，想把模型比价表的汇率从 `7.2` 改成 `7.3`，还得打开 `.py` 脚本去改顶部变量。可如果每天都要微调一次关注的热点关键词（比如今天想多盯一下 `agent`、明天想把 Hacker News 热度门槛从 `50` 分提到 `500` 分），每次都去动 Python 代码既麻烦又容易手滑改坏缩进。

成熟的工程项目都用一招省心做法：**把「程序逻辑」留在 `.py` 脚本里，把「人经常改的参数」单独抽进一张配置文件 `config.yaml`，把「原始数据」留在 `.json`，把「最终给人看的简报和说明书」写成 `.md`。**

这就是你在 AI 项目里天天打交道的「纯文本三件套」：**JSON、YAML、Markdown**。它们全都可以用普通记事本打开，学会读和改这三样，你哪怕一行代码不写，照样能灵活指挥整套工具。

---

## 2. 系统位置：三件套正好串起 `ai-radar` 的「输入 → 控制 → 输出」

把 `practice/scripts/daily_briefing.py` 的一次运行画出来，三种格式各自站在最拿手的位置上：

```
机器给机器看的原始数据（JSON）                 人给机器调参数的控制面板（YAML）
data/openrouter-models-2026-11-24.json        practice/config.yaml          ← 【本课位置】
data/hn-frontpage-2026-11-24.json               (汇率 / 关键词 / 热度门槛)
                  \                                   /
                   └──────────→  scripts/daily_briefing.py  ←── Python 按配置加工
                                           ↓
                              给人读的文档与早报成品（Markdown）
                                 output/daily-briefing.md
                                 README.md / AGENTS.md
```

一句话分工记死：
- **JSON**：给程序之间传数据用（严谨、机器好解析，人不爱手改）；
- **YAML**：给人当配置面板用（极清爽、能写 `#` 中文注释，改完保存重跑脚本即生效）；
- **Markdown**：给人读文档、写简报、给 AI 写项目规则用（纯文本，预览出来自带标题、表格和链接）。

---

## 3. 讲清楚：三种格式的写法对照与 3 大高频语法坑

### 3.1 一张表看懂三件套的区别

| 格式 | 常见扩展名 | 核心长相 | 能不能写 `#` 注释 | `ai-radar` 里的真实文件 |
|---|---|---|---|---|
| **JSON** | `.json` | 花括号 `{}` + 方括号 `[]` + **双引号** + 逗号 | **不能**（写 `#` 直接报错） | `data/openrouter-models-2026-11-24.json`、`data/hn-frontpage-2026-11-24.json` |
| **YAML** | `.yaml` / `.yml` | `键: 值` + **2 个空格缩进** + `- ` 列表项 | **可以**（`#` 开头整行是注释） | `practice/config.yaml` |
| **Markdown** | `.md` | `#` 标题、`**加粗**`、`- ` 列表、`\| 表格 \|` | 纯文字直接写 | `practice/README.md`、`output/daily-briefing.md`、`AGENTS.md` |

### 3.2 每种格式最容易踩的 1 个致命小坑

#### 坑 ①：YAML 里绝对不能按 `Tab` 键缩进，冒号后面必须留 1 个空格

YAML 靠「左边对齐的空格数」判断层级关系（就像 Python 缩进），并且**官方标准严禁使用 `Tab` 制表符**。一旦你在 `config.yaml` 里顺手按了一下 `Tab` 键，运行脚本立刻吐出这行真实报错：

```text
yaml.scanner.ScannerError: while scanning for the next token
found character '\t' that cannot start any token
  in "config.yaml", line 2, column 1:
    	min_points: 50
    ^
```

同时注意 `min_points: 50` 中间那个**英文冒号后面必须紧跟 1 个空格**——写成 `min_points:50` 会被当成一整串普通文字，读不出数字 `50`！

还有个实用提醒：在 YAML 里遇到特殊符号开头的文字（比如 `~` 或 `:free`、`:batch`），像 `practice/config.yaml` 那样套上双引号 `":batch"` 最稳妥，防止被 YAML 误解成语法符号。

#### 坑 ②：JSON 里的「最后一行多打逗号」和「单引号」

手工改 `.json` 文件时，90% 的报错来自两件事：
1. **最后一项末尾多留了一个逗号**（例如 `{"min_points": 50,}`）→ Python 立刻报 `json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes`；
2. **把双引号 `"` 敲成了单引号 `'`** 或中文全角引号 `“”` → 标准 JSON 只认英文双引号 `"`。

#### 坑 ③：Markdown 的「`#` 后漏空格」和「代码块没闭合」

写 `README.md` 或 `AGENTS.md`（M5 会专门讲）时，只盯住 3 个小规矩就够了：
- 标题 `#` 后面必须空一格（`## 一、标题`，写成 `##标题` 不会变大字）；
- 代码块开头是三个反引号 ` ``` `，结尾也必须配对三个反引号 ` ``` `，漏掉末尾那三个，后面整篇文章都会被吸进灰框里；
- 链接固定写法是 `[显示文字](网址)`（方括号在前、圆括号在后）。

---

## 4. 现场看：改一行 `config.yaml`，零代码调整早报口径

打开配套仓库真实的 `practice/config.yaml`（共 34 行）：

```yaml
# ai-radar 项目配置文件（改完保存并重跑脚本即生效，不需要改 Python 代码）
# 注意：YAML 缩进必须用空格（本文件统一 2 空格），绝不能按 Tab 键

project:
  name: ai-radar
  data_dir: data
  output_dir: output

model_pricing:
  snapshot_file: openrouter-models-2026-11-24.json
  exchange_rate: 7.2
  top_n: 5
  exclude_prefixes:
    - "~"
  exclude_suffixes:
    - ":free"
    - ":batch"

daily_briefing:
  snapshot_file: hn-frontpage-2026-11-24.json
  output_file: daily-briefing.md
  min_points: 50
  max_items: 8
  keywords:
    - ai
    - llm
    - model
    - nvidia
    - oss
    - openai
    - anthropic
    - dario
    - deepseek
    - agent
```

直接运行 `python3 practice/scripts/daily_briefing.py`，终端打印：

```text
已按 config.yaml 生成简报：output/daily-briefing.md（模型 5 条，HN 热点 5 条）
```

打开生成的 `practice/output/daily-briefing.md`，里面就是一份干净可直接转发群里的 Markdown 成品：

```markdown
# ai-radar 每日 AI 选型与情报简报

> 口径来源：`config.yaml`（汇率 `1 USD = 7.2 RMB`，HN 热度门槛 `>= 50` 分）

## 一、商用实时多模态低价 Top 5（每百万 Token）

| 排名 | 模型 ID | 输入价 (¥/M) | 输出价 (¥/M) | 综合均价 (¥/M) |
|---|---|---|---|---|
| 1 | `google/gemma-3-4b-it` | ¥0.2880 | ¥0.3600 | ¥0.3240 |
| 2 | `nex-agi/nex-n2.5-mini` | ¥0.1800 | ¥0.7200 | ¥0.4500 |
| 3 | `qwen/qwen3.7-flash` | ¥0.2160 | ¥0.9360 | ¥0.5760 |
| 4 | `tencent/hy4-flash` | ¥0.2520 | ¥1.0116 | ¥0.6318 |
| 5 | `google/gemma-3-12b-it` | ¥0.3600 | ¥1.0800 | ¥0.7200 |

## 二、Hacker News 首页 AI 热点（命中 5 条）

1. **[Nvidia Reinstates Jensen Huang as CEO](https://www.cnbc.com/2026/11/23/nvidia-jensen-huang-ceo.html)**（2723 分 · 3581 条讨论）
2. **["Dario is hyping the dangers so OSS models are illegal and he stays in control"](https://twitter.com/ylecun/status/2124550037912920090)**（1909 分 · 1102 条讨论）
3. **[LLM agents work for their parent companies, not for you](https://michaelharley.net/posts/2026/11/01/llm-agents-work-for-their-parent-companies-not-for-you/)**（518 分 · 224 条讨论）
4. **[Who in Washington owns and trades Nvidia stock](https://www.kadoa.com/congress/insights/trump-nvidia)**（240 分 · 122 条讨论）
5. **[Declare is a UI language for you and your AI](https://davidtemkin.github.io/declarelang/)**（86 分 · 61 条讨论）
```

现在做个真实小实验：**一行 Python 代码都别碰**，只把 `config.yaml` 里的 `min_points: 50` 改成 `min_points: 500` 保存重跑——实测脚本立刻把 Hacker News 热点自动收紧为最重磅的 **3 条**（2723 分的 Nvidia、1909 分的 OSS 争论、518 分的 LLM Agents 文章）。这就是把参数拆到 YAML 里的爽感：以后天天调口味，只改这份 34 行的中文注释白纸就行。

---

## 5. 你来读：10 秒揪出这两小段配置文件里的 3 个语法雷

下面是新手自己手改配置文件后，一运行就报错的两段片段：

片段 A（`config.yaml`）：
```yaml
daily_briefing:
	min_points:500
  keywords:
    - ai
    - deepseek
```
（提示：第 2 行前面敲了一个 `Tab` 键）

片段 B（`settings.json`）：
```json
{
  "exchange_rate": 7.2,
  "top_n": 10,
}
```

停下来想 10 秒：这两段文件里一共藏着哪 **3 个** 必报错的语法问题？

**判断思路**：
1. **片段 A 第 2 行用了 `Tab` 缩进**：YAML 严禁 Tab，会触发 `ScannerError: found character '\t'`，必须删掉 Tab 改成和下面 `keywords:` 对齐的 **2 个空格**。
2. **片段 A 第 2 行 `min_points:500` 冒号后缺空格**：必须写成 `min_points: 500`，否则 YAML 会把它当成一整串字符串而不是键值对。
3. **片段 B 第 3 行 `"top_n": 10,` 末尾多了一个逗号**：JSON 对象的最后一项后面严禁留逗号，删掉这个逗号就立刻合法了。

---

## 6. 小检查（3 道判断题）

1. 在标准 `.json` 文件里，可以直接用 `#` 号写中文注释，并且最后一项后面多留一个逗号也没关系。（对 / 错）
2. 编辑 `.yaml` 配置文件时，层级缩进应该始终用空格（如 2 个空格），不要按 `Tab` 键，并且英文冒号后面要留 1 个空格。（对 / 错）
3. 把汇率、关键词和热度门槛抽进 `config.yaml` 的好处是：调整业务口径时直接改配置重跑脚本即可，不需要反复修改 `.py` 代码。（对 / 错）

---

## 7. 下一课

到这里，项目文件夹结构（3.1）、依赖和虚拟环境（3.2）、纯文本配置三件套（3.3）全部配齐了。现在只剩下 M3 最重要的一道防线：那些**绝不能放进 `config.yaml`、绝不能写进代码、更不能随便喂给公有云 AI 的敏感东西**该怎么管？下一课就是 M3 压轴课 **3.4《密钥与数据安全》**。

---

## 小检查答案

1. **错**。标准 JSON 不支持 `#` 注释，也不允许最后一项后面留尾随逗号，否则解析立刻报 `JSONDecodeError`。
2. **对**。只用空格缩进 + 冒号后空一格，就能避开 YAML 90% 的语法报错。
3. **对**。把会变的参数和稳定的代码拆开，既安全又方便日常维护。

---

## 参考与事实边界

- **实际操作结果**：本课 `practice/config.yaml`、`practice/scripts/daily_briefing.py` 生成的 `output/daily-briefing.md`（`min_points: 50` 命中 5 条、`min_points: 500` 命中 3 条），以及 `yaml.scanner.ScannerError`（Tab 报错）和 `json.decoder.JSONDecodeError`（尾随逗号报错），均在 `Python 3.12.16` + `PyYAML 6.0.4` 环境实测获得。
- **官方资料**：
  - JSON 官方标准：[Introducing JSON](https://www.json.org/)；
  - YAML 1.2 规范：[YAML Official Specification](https://yaml.org/spec/1.2.2/)；
  - GitHub Flavored Markdown 语法说明：[Basic writing and formatting syntax — GitHub Docs](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)。
- **作者说明**：第 5 节两段错误片段为基于真实高频解析异常构造的监工排错练习。
