# 2.4 `if`：什么情况做什么事

> 学习目标：看懂 `if / elif / else`、常见判断符号（`==`、`!=`、`<=`、`in`）和逻辑组合（`and`、`or`、`not`），能在 AI 的脚本里一眼发现筛选条件写反、写宽或漏掉边界。
>
> 演示环境：Python `3.12.16`，延续 `ai-radar` 项目的 `practice/scripts/build_top10.py` 与 `practice/data/openrouter-models-2026-11-24.json`（470 个真实模型实测统计）。

---

## 1. 为什么「输出必须含 `text`」还是放进了音乐模型？

还记得 0.1 课那个让人哭笑不得的翻车吗：我们让 AI 挑支持看图的文字对话模型，结果 Google 的音乐生成模型 `google/lyria-3-pro-preview` 混进了 Top 10。

现在我们用 2.3 课学过的字典知识，直接掀开 `google/lyria-3-pro-preview` 在 `openrouter-models-2026-11-24.json` 里的真实卡片：

```json
{
  "id": "google/lyria-3-pro-preview",
  "pricing": { "prompt": "0", "completion": "0" },
  "architecture": {
    "modality": "text+image->text+audio",
    "input_modalities": ["text", "image"],
    "output_modalities": ["text", "audio"]
  }
}
```

看最后一行！它的 `output_modalities` 是 **`["text", "audio"]`**——里面**确实包含 `"text"`**！

这意味着，哪怕你在第 2 轮提醒 AI 检查输出模态，如果 AI 写成下面这句：

```python
if "text" not in outputs:
    return False
```

`lyria-3` 依然会大摇大摆过关！只有把条件收紧成「**输出模态必须严格等于纯文字 `["text"]`**」：

```python
if outputs != ["text"]:
    return False
```

才能把 `lyria-3` 以及 `gemini-3.1-flash-image`、`gpt-5.4-image-2` 等 **17 个**「能看图但输出带音频或图片」的非纯文本对话模型一次性拦在门外。

这就是整个 M2 里**含金量最高的一课**：AI 写的业务口径对不对，90% 都藏在 `if` 后面的那一行条件里。

---

## 2. 系统位置：`if` 是每一条数据进门前的「安检闸机」

在 `build_top10.py` 里，470 个模型排队走过来，每一个都要先过 `if` 设下的 4 道闸机：

```
单个模型卡片（来自 470 个模型列表）
      ↓
闸机 1：if 名字以 ~ 开头，或含 :free / :batch → 拦下！   ← 【本课位置】
      ↓
闸机 2：if 输入模态里不含 image               → 拦下！
      ↓
闸机 3：if 输出模态不等于 ["text"]            → 拦下！
      ↓
闸机 4：if 输入价 <= 0 或 输出价 <= 0         → 拦下！
      ↓
全部通过（207 个合规商用实时多模态对话模型）→ 进入算价与排序
```

---

## 3. 讲清楚：`if` 的结构、判断符号和 `and` / `or` 大坑

### 3.1 `if / elif / else` 和缩进（4 个空格定生死）

把 `if` 翻译成中文，就是「**如果……就……；否则如果……就……；其余情况就……**」：

```python
if avg_cny <= 0.5:
    tier = "超低价"
elif avg_cny <= 2.0:
    tier = "常规价"
else:
    tier = "高端价"
```

看懂这段代码，盯住 Python 两个雷打不动的规矩：
1. **末尾冒号 `:`**：每一条 `if`、`elif`、`else` 结尾都有一个英文冒号，意思是「下面归我管」。
2. **左侧缩进（通常是 4 个空格）**：Python 不用大括号包代码块，而是靠**往右退 4 格**来表示「这几行只有在上面条件成立时才执行」。一旦某行忘了退格或退错格，逻辑就完全变了（或者直接报 `IndentationError`）。

### 3.2 监工必认的 6 个判断符号

| 写法 | 读法 | 真实例子（`ai-radar`） | 含义 |
|---|---|---|---|
| `==` | 等于（注意是**两个等号**） | `outputs == ["text"]` | 输出模态正好只有纯文字 |
| `!=` | 不等于 | `outputs != ["text"]` | 输出模态不是纯文字（带音频/图像都算） |
| `>` / `>=` / `<` / `<=` | 大于 / 大于等于 / 小于 / 小于等于 | `prompt_usd <= 0` | 价格是 `0`（免费）或 `-1`（动态路由） |
| `in` / `not in` | 在里面 / 不在里面 | `":batch" in model_id` | 模型 ID 里包含 `:batch` 字样 |
| `.startswith(...)` | 以……开头 | `model_id.startswith("~")` | 模型 ID 是 `~` 开头的动态别名 |
| `.endswith(...)` | 以……结尾 | `file_name.endswith(".json")` | 文件名是 `.json` 结尾 |

**顺手回扣 2.2 课**：单个 `=` 是「把值装进盒子（赋值）」，两个 `==` 才是「问两边相不相等（判断）」。看到 `if` 后面出现 `==`，就放心地读成「是不是等于」。

### 3.3 最容易翻车的逻辑词：`and`、`or`、`not`

当多个条件拼在一行时，全靠这三个英文词串联：

- **`and`（并且）**：左右两边**同时成立**才算数。
- **`or`（或者）**：左右两边**只要有一个成立**就算数。
- **`not`（不是 / 取反）**：把「真」翻成「假」，把「假」翻成「真」。

**最常见的翻车点**：AI（甚至人自己）在写「排除条件」时，最容易把 `or` 和 `and` 写反！看一个真实对比：

- **正确（要排除所有价格异常的模型）**：`if prompt_usd <= 0 or completion_usd <= 0: return False`
  - 读法：只要**输入价 `<= 0` 或者 输出价 `<= 0`**（任意一边不合规），就踢掉。
- **错误（写成 `and`）**：`if prompt_usd <= 0 and completion_usd <= 0: return False`
  - 读法：只有输入和输出**同时** `<= 0` 才踢掉。结果快照里真实的 `scaledown/summarize`（输入价 `$0.04/M`，输出价 `$0/M`）就会直接漏网溜进商用付费榜！

---

## 4. 现场看：`build_top10.py` 的 4 道真实过滤门

打开 `practice/scripts/build_top10.py` 第 31–64 行，这就是我们在 0.1 课反复打磨出来的 `is_valid_chat_vision_model()` 函数：

```python
def is_valid_chat_vision_model(model: dict) -> bool:
    model_id = model.get("id", "")

    # 规则 1：排除 ~ 动态别名、:free 免费版、:batch 离线批处理版
    if model_id.startswith("~"):
        return False
    if ":free" in model_id or ":batch" in model_id:
        return False

    # 规则 2：输入必须支持图片
    arch = model.get("architecture") or {}
    inputs = arch.get("input_modalities") or []
    outputs = arch.get("output_modalities") or []
    modality = arch.get("modality") or ""
    if ("image" not in inputs) and ("image->" not in modality):
        return False

    # 规则 3：输出必须是纯文字（排除输出含 audio 的音乐生成模型，如 lyria-3）
    if outputs != ["text"]:
        return False

    # 规则 4：输入价和输出价都必须大于 0（排除 -1 动态路由和 0 免费项）
    pricing = model.get("pricing") or {}
    try:
        prompt_usd = float(pricing.get("prompt") or 0)
        completion_usd = float(pricing.get("completion") or 0)
    except (ValueError, TypeError):
        return False

    if prompt_usd <= 0 or completion_usd <= 0:
        return False

    return True
```

把 470 个真实模型放进这 4 道闸机实测统计，每一道拦下了多少「脏数据」一目了然：
- 规则 1 挡掉：**19** 个 `~` 动态别名、**11** 个带 `:free` 的免费限流版、**92** 个 `:batch` 离线批处理版；
- 规则 2 挡掉：所有不支持看图的纯文本模型；
- 规则 3 挡掉：**17** 个虽能看图但输出含音频/图片的非纯文字模型（包括 `google/lyria-3-pro-preview`、`google/gemini-3.1-flash-image`、`openai/gpt-5.4-image-2`）；
- 规则 4 挡掉：**8** 个 `-1` 动态路由（如 `openrouter/auto`）及输入/输出单价为 `0` 的模型（如 `scaledown/summarize`）。

最后稳稳剩下 **207** 个真正可用于实时多模态文字对话的商用付费模型，再进入排序取前 10。

---

## 5. 你来读：AI 给你加了条新口径，10 秒查出哪一行写反了

你对 AI 说：「再加一条过滤——只保留上下文窗口（`context_length`）至少 128,000（128K）、并且输入价和输出价都大于 0 的模型。」

AI 在 `is_valid_chat_vision_model()` 里改出了下面 4 行：

```python
    if context_length > 128000:
        return False

    if prompt_usd <= 0 and completion_usd <= 0:
        return False
```

停下来想 10 秒：这两条 `if` 竟然**全都写错了**！分别错在哪儿？

**判断思路**：
1. **第一条把方向写反了（还漏了等于）**：你要保留 `>= 128000` 的模型，所以被拦掉（`return False`）的应该是「**小于** 128,000」的模型，即 `if context_length < 128000:`。AI 写成 `> 128000` 会把所有长上下文模型全踢掉，反而留下小上下文的！
2. **第二条把 `or` 写成了 `and`**：只要输入价或输出价**任意一个** `<= 0` 就该淘汰，写成 `and` 会放行一边收费、一边标价 `0` 的异常模型（例如 `scaledown/summarize`）；必须改成 `if prompt_usd <= 0 or completion_usd <= 0:`。

---

## 6. 小检查（3 道判断题）

1. 在 Python 里，`if prompt_usd = 0:` 可以用来判断输入价格是否等于 0。（对 / 错）
2. 过滤带 `:free` 或 `:batch` 的模型时，`if ":free" in model_id or ":batch" in model_id:` 表示只要命中其中一个后缀就拦下。（对 / 错）
3. 对于 `output_modalities` 为 `["text", "audio"]` 的 `google/lyria-3-pro-preview`，条件 `if "text" not in outputs:` 会把它成功拦截。（对 / 错）

---

## 7. 下一课

学会了怎么给「单个模型」设安检闸机，接下来看 Python 怎么一口气把这 4 道闸机自动套用到 470 个模型、或者 30 条 Hacker News 热帖上。下一课 **2.5《`for`：批量处理》**，带你读懂循环、`continue` 和 `break`。

---

## 小检查答案

1. **错**。判断相等必须用两个等号 `==`（`if prompt_usd == 0:`），单个 `=` 是赋值，写在 `if` 条件里会直接报语法错误。
2. **对**。`or` 表示「任意一边成立即满足」，命中 `:free` 或 `:batch` 都会进入 `return False`。
3. **错**。因为 `["text", "audio"]` 里包含 `"text"`，所以 `"text" not in outputs` 为假，会直接放行它；必须写成 `outputs != ["text"]` 才能精准拦截非纯文字输出模型。

---

## 参考与事实边界

- **实际操作结果**：本课统计的 470 个模型细分拦截数（`~` 别名 19 个、`:free` 11 个、`:batch` 92 个、`-1` 负价 8 个、支持图片但非纯文字输出 17 个、最终合规 207 个）及 `google/lyria-3-pro-preview` 真实 `output_modalities` 字段，均在 `Python 3.12.16` 上对 `practice/data/openrouter-models-2026-11-24.json` 实测获得。
- **官方资料**：Python 流程控制文档：[More Control Flow Tools — `if` Statements](https://docs.python.org/3/tutorial/controlflow.html#if-statements)。
- **作者说明**：第 5 节的 4 行代码为提炼自高频业务口径失误的监工练习。
