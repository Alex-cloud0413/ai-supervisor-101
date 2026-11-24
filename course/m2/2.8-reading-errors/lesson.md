# 2.8 读懂报错

> 学习目标：掌握 Python 报错「从最后一行往上读」三步法，认出 5 类最高频报错，并且会用「报错三件套」把报错准确交给 AI 一次修对。
>
> 演示环境：Python `3.12.16`，所有报错原文均在 `ai-radar` 真实 OpenRouter 模型数据与脚本上实测触发。

---

## 1. 屏幕飙出十几行英文红字，别慌，也别只发一句「报错了」

哪怕是有十年经验的程序员，跑代码也天天见报错。对零基础监工来说，最容易踩的坑是两种极端：

- **第一种**：一看到终端吐出满屏 `Traceback (most recent call last): ...`，心脏一紧，以为把电脑搞坏了，立刻关掉窗口不敢再碰；
- **第二种**：只截半张图，或者在对话框里丢给 AI 一句「运行失败了，你修一下」。AI 根本看不到报错原文，只能瞎猜乱改，原本一行小毛病被改出三个新 Bug。

其实 Python 报错是一张极其贴心的「体检诊断书」——**它已经把病名、病因、精确到哪一页第几行全写好了，只不过把最重要的结论压在了最底下那一行**。学会倒着读这 3 行，你 10 秒就能搞清楚发生了什么，还能一次把 AI 指挥到位。

---

## 2. 系统位置：报错是 Python 递回给监工和 AI 的「质检报告」

回到整条工作链路，报错正好出现在「跑」和「再改」之间：

```
Harness 在终端运行脚本：python3 build_top10.py
      ↓
脚本中途撞到问题（找不到文件 / 缺库 / 拿错字段 / 类型不对）
      ↓
Python 解释器立刻停机，吐出 Traceback 报错堆栈  ← 【本课位置】
      ↓
你倒着扫 3 行看懂大意 → 连同原文和要求发给 AI → AI 按根因精准修完重跑
```

**先吃一颗定心丸**：普通的 Python 报错只会让当前这一次脚本运行停下来，**绝对不会弄坏你的操作系统，也不会删掉你的原始数据文件**。

---

## 3. 讲清楚：「从最后一行往上读」三步法 + 5 类高频报错速查表

### 3.1 「从最后一行往上读」三步法

以后不管屏幕吐出 5 行还是 50 行报错，眼睛永远按这个顺序扫：

1. **第一步：直接跳到最后一行（看病名 + 病因）**
   - 冒号左边是**错误类型**（例如 `KeyError`、`TypeError`、`FileNotFoundError`）；
   - 冒号右边是**具体解释**（例如 `'input'`、`No such file or directory: '...'`）。
   - 光看这最后一行，就已经解决 70% 的疑惑。
2. **第二步：从最后一行往上找，找到「属于你工作区脚本」的那一行（看病灶坐标）**
   - 报错上面通常会列出一条调用链（`File "...", line XX, in 函数名`）。
   - 如果中间夹杂着 `site-packages/openpyxl/...` 或 `pandas/...` 这类第三方库内部的路径，**先全部跳过不看**——99% 的情况错不在官方库，而在你项目里自己的 `.py` 脚本那一行。
3. **第三步：用「监工报错三件套」交给 AI 修**——把下面 3 样东西打包发给 AI，几乎一轮就能修对：
   - ① **完整复制报错原文**（至少包含「你的脚本文件名 + 行号」和「最后一行」，不要手打转述）；
   - ② **说清刚跑了哪条命令**（例如 `python3 practice/scripts/build_top10.py`）；
   - ③ **加一句监工护身符**：「先告诉我报错根因再改代码，不要用 `try/except` 静默填 0 把报错盖过去。」（还记得 0.1 课第 5 节的教训吗？不加这句，有些模型会偷懒吞掉报错！）

### 3.2 5 类最高频 Python 报错速查表（全为本机实测原文）

| 报错类型（最后一行冒号前） | 白话翻译 | `ai-radar` 里的实测真实例子 | 第一反应怎么处理 |
|---|---|---|---|
| `FileNotFoundError` | **找不到这个文件或文件夹** | `FileNotFoundError: [Errno 2] No such file or directory: 'data/openrouter-models-2026-11-25.json'` | 查 3 处：文件名日期拼错没有？文件放进 `data/` 了没有？终端是不是没 `cd` 进工作区根目录？ |
| `ModuleNotFoundError` | **缺第三方库，还没装** | `ModuleNotFoundError: No module named 'openpyxl'` | 对应 2.7 课：核对包名拼写安全后，让 AI 跑 `python3 -m pip install openpyxl`（Windows 用 `python -m pip install`） |
| `KeyError` | **字典里找不到这个字段名** | `KeyError: 'input'` | 对应 2.3 课：AI 把真实字段名猜错了（OpenRouter 叫 `'prompt'`，不是 `'input'`），让它先打印真实键名再改 |
| `TypeError` / `ValueError` | **数据类型对不上 / 格式转不了** | `TypeError: can't multiply sequence by non-int of type 'float'` | 对应 2.2 课：十有八九是拿带引号的文字（如 `"0.00000004"`）去算数学，或碰到 `None` 空值忘了判空 |
| `SyntaxError` / `IndentationError` | **标点漏写或缩进空格没对齐** | `IndentationError: expected an indented block after 'if' statement on line 2` | 对应 2.4 课：漏了英文冒号 `:`、用了中文全角引号 `“”`、或 `if`/`for` 底下忘了退 4 个空格，把报错发给 AI 秒修 |

---

## 4. 现场看：把 3 段真实 Traceback 拆开画重点

下面 3 段报错均在 `Python 3.12.16` 针对 `ai-radar` 真实场景触发，跟着标号练习倒着读：

### 案例 A：把快照日期写错 1 天（`FileNotFoundError`）

```text
Traceback (most recent call last):
  File "practice/scripts/build_top10.py", line 174, in main
    models = load_models(DATA_PATH)
  File "practice/scripts/build_top10.py", line 26, in load_models
    with json_path.open("r", encoding="utf-8") as f:
FileNotFoundError: [Errno 2] No such file or directory: 'data/openrouter-models-2026-11-25.json'
```

- **看最后一行**：找不到 `data/openrouter-models-2026-11-25.json`；
- **往上看坐标**：`build_top10.py` 第 26 行 `load_models`（从第 174 行 `main` 传进来的 `DATA_PATH`）；
- **一秒定因**：我们硬盘里存的是 `2026-11-24.json`，不是 `11-25`，去顶部改一下 `DATA_PATH` 文件名即可。

### 案例 B：AI 凭印象猜错价格字段（`KeyError`）

```text
Traceback (most recent call last):
  File "practice/scripts/build_top10.py", line 72, in calc_cny_pricing
    prompt_usd_m = float(pricing["input"]) * 1_000_000
                         ~~~~~~~^^^^^^^^^
KeyError: 'input'
```

- **看最后一行**：`KeyError: 'input'`（字典里没有 `'input'` 这个键）；
- **往上看坐标**：Python 3.12 还贴心地用 `~~~~~~~^^^^^^^^^` 波浪线和尖角号指出了罪魁祸首就是 `pricing["input"]`；
- **发给 AI**：贴上这 5 行，告诉它「`pricing` 里没有 `input`，请先核对 JSON 里真实的字段名（应该是 `prompt`）再修改」。

### 案例 C：忘了用 `float()` 转换字符串单价（`TypeError`）

```text
Traceback (most recent call last):
  File "practice/scripts/build_top10.py", line 74, in calc_cny_pricing
    prompt_cny_m = pricing["prompt"] * exchange_rate
                   ~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~
TypeError: can't multiply sequence by non-int of type 'float'
```

- **看最后一行**：不能拿文字序列（`sequence`，即带引号的字符串）去乘小数（`float`）；
- **往上看坐标**：第 74 行，`^` 尖角正好指着乘号 `*`；
- **一秒定因**：`pricing["prompt"]` 是 `"0.00000004"` 字符串，没套 `float(...)` 就直接乘 `exchange_rate`（`7.2`）。

---

## 5. 你来读：一份真实的多层级报错，10 秒拆出 3 个答案

你让 AI 帮忙改完算价公式后，运行 `python3 practice/scripts/build_top10.py`，终端跳出下面 10 行：

```text
Traceback (most recent call last):
  File "practice/scripts/build_top10.py", line 188, in <module>
    main()
  File "practice/scripts/build_top10.py", line 175, in main
    top_models = select_top_models(models, exchange_rate=EXCHANGE_RATE, top_n=TOP_N)
  File "practice/scripts/build_top10.py", line 101, in select_top_models
    qualified.append(calc_cny_pricing(model, exchange_rate))
  File "practice/scripts/build_top10.py", line 72, in calc_cny_pricing
    prompt_usd_m = float(pricing["prompt"]) * 1_000_000
ValueError: could not convert string to float: 'N/A'
```

停下来想 10 秒：
1. 真正出事是在哪个函数的第几行？
2. 发生了什么事？
3. 如果要把这条报错交给 AI 修，你怎么发一句话最稳妥？

**判断思路**：
1. **病灶坐标**：从下往上数第一条代码行——`practice/scripts/build_top10.py` 第 **72 行**，在 `calc_cny_pricing` 函数里（上面 `main` 和 `select_top_models` 只是顺路喊它干活的上级部门）。
2. **病因**：看最后一行 `ValueError: could not convert string to float: 'N/A'`——某条模型数据的 `pricing["prompt"]` 里填的不是数字字符串，而是 `'N/A'`（暂无报价），所以 `float('N/A')` 转不成小数崩掉了。
3. **发给 AI 的三件套提示**：「我运行 `python3 practice/scripts/build_top10.py` 报了下面这个错（粘贴完整 10 行 Traceback）。看起来某条模型的 `prompt` 价格是 `'N/A'`。请先检查是哪几个模型，并把无法转成有效正数的模型在 `is_valid_chat_vision_model` 里过滤掉，**不要把 `'N/A'` 填成 0 混进榜单**。」

---

## 6. 小检查（3 道判断题）

1. 看到 Python 吐出 20 行 `Traceback` 报错时，最核心的错误类型和原因通常写在**第一行**，应该从上往下逐行背下来。（对 / 错）
2. 报错最后一行写着 `ModuleNotFoundError: No module named 'pandas'`，说明电脑上还没给当前 Python 环境安装 `pandas` 这个第三方库。（对 / 错）
3. 把报错交给 AI 修复时，除了贴完整报错原文和所跑命令，最好明确要求它「先查根因再改，不要靠静默填 0 盖住报错」。（对 / 错）

---

## 7. 下一课

恭喜你！到这里，**M2 读懂 Python** 全部 8 节课正式通关：你已经把 `.py` 脚本的 4 段骨架、变量、列表字典、`if`、`for`、函数、第三方库和读懂报错全部拿捏在手里。

接下来，我们把视角从「单个脚本」拉高到「一整个可维护的真实项目」。下一课进入 **M3 一个项目长什么样**，从 **3.1《项目文件夹的标准结构》** 开始，看看 `README`、脚本、原始快照、配置文件和输出目录各自该放哪里。

---

## 小检查答案

1. **错**。Python 报错（Traceback）把最核心的错误类型与原因压在**最后一行**，正确读法是「从最后一行往上读」。
2. **对**。`ModuleNotFoundError` 表示找不到对应的扩展模块，核对包名拼写正确后用 `python3 -m pip install pandas` 安装即可。
3. **对**。给足上下文能避免 AI 瞎猜，加上防静默吞错要求能防止它用假数据把业务漏洞盖过去。

---

## 参考与事实边界

- **实际操作结果**：本课速查表和拆解案例中的 5 类报错格式（含 Python 3.12 新增的 `~~~~~~~^^^^^^^^^` 精准错误位置指示符）均在 `Python 3.12.16` 环境下实测验证。
- **官方资料**：Python 内置异常与报错说明：[Built-in Exceptions — Python 3 Documentation](https://docs.python.org/3/library/exceptions.html)。
- **作者说明**：第 4 节案例 A/B/C 与第 5 节的 `'N/A'` `ValueError` 为结合 `build_top10.py` 行号与真实错误输出构造的教学演示场景。
