# 2.3 列表与字典：数据长什么样

> 学习目标：分清列表 `[]`（按顺序排队的条目）和字典 `{}`（成对的「字段名: 值」），能把一行 JSON 或表格记录翻译回代码里的取值写法。
>
> 演示环境：Python `3.12.16`，延续 `ai-radar` 项目的 `practice/data/openrouter-models-2026-11-24.json`、`practice/data/hn-frontpage-2026-11-24.json` 与 `practice/scripts/build_top10.py`。

---

## 1. 打开 JSON 满屏括号，其实只有两种盒子

如果你好奇点开过 `practice/data/openrouter-models-2026-11-24.json`，第一眼多半会被密密麻麻的 `[`、`]`、`{`、`}` 和冒号劝退：

```json
{
  "data": [
    {
      "id": "google/gemma-3-4b-it",
      "name": "Google: Gemma 3 4B",
      "context_length": 131072,
      "pricing": {
        "prompt": "0.00000004",
        "completion": "0.00000005"
      },
      "architecture": {
        "input_modalities": ["text", "image"],
        "output_modalities": ["text"]
      }
    }
  ]
}
```

看着吓人，但只要分清两种括号，10 秒就能拆明白：
- **方括号 `[ ... ]` 是列表（List）**：按顺序排成一队的多条数据（比如 470 个模型、或者这个模型支持的输入模态 `["text", "image"]`）。
- **花括号 `{ ... }` 是字典（Dict）**：一张带表头字段名的卡片，成对写着 `"字段名": 值`（比如 `"id": "google/gemma-3-4b-it"`）。

全天下 90% 的公开接口数据、配置文件和 Excel 表格，进到 Python 代码里全都是**「列表套字典，字典再套列表」**。认准这两种括号，你就看懂了 AI 怎么从几百条数据里精准挑出你要的那一格。

---

## 2. 系统位置：数据读进 Python 后长成什么样

在 `build_top10.py` 的流水线里，列表和字典正好坐在「硬盘文件」和「筛选算价」之间：

```
硬盘上的原始文件（data/openrouter-models-2026-11-24.json）
      ↓
json.load(f) 把文件内容读进内存，变成 Python 的字典和列表   ← 【本课位置】
      ↓
470 张模型「卡片」（字典）排成一队（列表）：models = [模型0, 模型1, ..., 模型469]
      ↓
后续的 if 过滤和 for 循环，全都在这张卡片里按字段名取值
```

把 Excel 表格拿来对照，就更好理解了：
- **整张 Excel 表** ≈ 一个**列表**（第 1 行、第 2 行、第 3 行排成队）；
- **表里的某一行** ≈ 一个**字典**（`{"排名": 1, "模型 ID": "google/gemma-3-4b-it", "综合均价": 0.324}`）。

---

## 3. 讲清楚：列表 `[]`、字典 `{}` 和最稳的 `.get()` 取值

### 3.1 列表（List，`[...]`）：排成一队，从 `0` 开始数！

列表用方括号包起来，里面的条目用逗号隔开：

```python
inputs = ["text", "image", "video"]
```

监工看列表，盯住 3 个最常见的动作：

- **按位置编号取值（注意从 `0` 开始数！）**：`inputs[0]` 是第 1 个 `"text"`，`inputs[1]` 是第 2 个 `"image"`，`inputs[-1]` 是倒数第 1 个 `"video"`。
- **切片取前几条**：`qualified[:10]` 表示「从开头取前 10 条」（编号 0 到 9），这就是 `build_top10.py` 截取 Top 10 的写法。
- **查总数**：`len(models)` 返回列表长度（在我们的快照里是 `470`）。

**最常见的误解**：以为 `models[1]` 拿的是第 1 名。错！Python 和绝大多数编程语言一样**从 `0` 开始编号**，`models[0]` 才是第 1 名，`models[1]` 已经是第 2 名了。如果看到 AI 在代码里写 `top1 = qualified[1]`，你一眼就能把它揪出来。

### 3.2 字典（Dict，`{...}`）：按字段名查值，可以「套娃」

字典用花括号包起来，每一项都是 `键(key): 值(value)`：

```python
pricing = {"prompt": "0.00000004", "completion": "0.00000005"}
```

- **直接按名字取**：`pricing["prompt"]` 拿到 `"0.00000004"`。
- **套娃（嵌套）连续取**：因为整个模型 `model` 是一个大字典，里面的 `"pricing"` 对应的值又是一个小字典，所以要连写两层方括号：
  - `model["pricing"]["prompt"]` → 先走进 `"pricing"` 抽屉，再拿里面的 `"prompt"`；
  - `model["architecture"]["input_modalities"]` → 拿到列表 `["text", "image"]`。

### 3.3 方括号直接取 `model["pricing"]` vs 安全取值 `model.get("pricing")`

处理真实世界数据时，经常碰到某些字段偶尔缺席（比如某个内测模型压根没填 `architecture` 或 `pricing`）。两种写法后果完全不同：

| 写法 | 字段存在时 | 字段缺失时 | 适用场景 |
|---|---|---|---|
| `model["pricing"]` | 返回对应的字典 | **立刻报 `KeyError` 中断程序** | 确认绝不能缺的核心主键（如 `model["id"]`） |
| `model.get("pricing") or {}` | 返回对应的字典 | **不报错，安全给一个空字典 `{}`** | 真实公开接口里可能缺值或填了 `null` 的字段 |

所以你在 `build_top10.py` 里会频繁看到 `.get("xxx", 默认值)` 或 `.get("xxx") or []`——这是 AI 写得比较稳妥的防崩保护，不用觉得眼花。

---

## 4. 现场看：把两份真实快照和代码左右对照

### 4.1 OpenRouter 模型快照 vs `build_top10.py`

看 `practice/scripts/build_top10.py` 第 24–28 行和第 67–76 行怎么拆开 470 个模型：

```python
# 1. 整份 JSON 最外层是个大字典，真正的 470 个模型藏在 "data" 这个列表里
with json_path.open("r", encoding="utf-8") as f:
    raw_data = json.load(f)
return raw_data.get("data", [])
```

拿到单个模型字典 `model` 后，取值过程和 JSON 结构一一对应：

```python
model["id"]                            # → "google/gemma-3-4b-it"
model.get("context_length") or 0       # → 131072
pricing = model.get("pricing") or {}
pricing["prompt"]                      # → "0.00000004"
arch = model.get("architecture") or {}
arch.get("input_modalities") or []     # → ["text", "image"]
arch.get("output_modalities") or []    # → ["text"]
```

最后 `calc_cny_pricing()` 又把算完的干净字段重新组装成一张新字典返回（第 78–88 行），准备写进 Excel 的一行：

```python
return {
    "id": model["id"],
    "name": model.get("name") or model["id"],
    "avg_cny": avg_cny_m,
    ...
}
```

### 4.2 再顺手看一眼 Hacker News 快照（结构完全同理）

打开 `practice/data/hn-frontpage-2026-11-24.json`，最外层同样是个字典，30 条首页热帖排在 `"hits"` 列表里：

```python
hits = hn_data.get("hits", [])
hits[0]["title"]         # → "Nvidia Reinstates Jensen Huang as CEO"
hits[0]["points"]        # → 2723
hits[0]["num_comments"]  # → 3581
```

学会了列表和字典，不管以后接 OpenRouter、Hacker News 还是公司飞书多维表格的接口，你看数据结构的方式全都是一模一样的。

---

## 5. 你来读：对照这条真实模型卡片，挑出 2 行写错的取值

下面是快照里 `qwen/qwen3.7-flash` 的真实数据结构，假设它排在 `top_models` 列表的第 3 位（前两位是 `gemma-3-4b-it` 和 `nex-n2.5-mini`）：

```json
{
  "id": "qwen/qwen3.7-flash",
  "name": "Qwen: Qwen3.7 Flash",
  "context_length": 1000000,
  "pricing": {
    "prompt": "0.00000003",
    "completion": "0.00000013"
  },
  "architecture": {
    "input_modalities": ["text", "image", "video"],
    "output_modalities": ["text"]
  }
}
```

AI 写了下面 4 行取值代码，想把「第 1 名模型的名称」和 `qwen` 这一条的「输入单价、支持模态」打印出来：

```python
first_model = top_models[1]
qwen_prompt = qwen["pricing"]["input"]
qwen_ctx = qwen.get("context_length") or 0
qwen_inputs = qwen["architecture"]["input_modalities"]
```

停下来想 10 秒：哪 **2 行** 有问题，分别会出什么事？

**判断思路**：
1. **第 1 行 `top_models[1]` 拿错名次**：列表从 `0` 开始数，`top_models[1]` 拿到的是第 2 名（`nex-agi/nex-n2.5-mini`），第 1 名应该写 `top_models[0]`。
2. **第 2 行 `qwen["pricing"]["input"]` 拼错字段名**：真实 JSON 里价格字典的键叫 `"prompt"` 和 `"completion"`，不叫 `"input"`，运行到这行会直接报 `KeyError: 'input'`。第 3、4 行都完全正确。

---

## 6. 小检查（3 道判断题）

1. 在 Python 列表 `top_models` 里，`top_models[0]` 代表第 1 条记录，`top_models[:5]` 代表前 5 条记录。（对 / 错）
2. 看到带花括号 `{...}` 的数据结构时，应该按位置编号 `0, 1, 2` 去取里面的值；看到带方括号 `[...]` 时，按字段名去取。（对 / 错）
3. 当 JSON 里某个字段偶尔可能缺失时，用 `model.get("pricing") or {}` 比直接写 `model["pricing"]` 更不容易让脚本中途崩溃。（对 / 错）

---

## 7. 下一课

现在你已经看懂单条模型数据长什么样、代码怎么从里面精准取值。接下来最关键的监工能力来了：怎么判断哪些模型该留、哪些该扔？下一课 **2.4《`if`：什么情况做什么事》**，拿 0.1 课「音乐模型 `lyria-3` 混进文字对话榜」的真实案发现场，教你一眼识破写反、写漏的筛选条件。

---

## 小检查答案

1. **对**。Python 列表索引从 `0` 开始，`[:5]` 截取索引 0、1、2、3、4 共 5 条记录。
2. **错**。刚好说反了：方括号 `[]` 是列表，按顺序编号（0, 1, 2）取；花括号 `{}` 是字典，按字段名（key）取。
3. **对**。方括号直接取不存在的键会立刻抛出 `KeyError` 中断运行，`.get(...)` 可以在缺失时给出安全默认值。

---

## 参考与事实边界

- **实际操作结果**：本课引用的 `google/gemma-3-4b-it`、`qwen/qwen3.7-flash` 嵌套结构与 Hacker News 榜首热帖字段，均直接采自仓库公开快照 `practice/data/openrouter-models-2026-11-24.json` 和 `practice/data/hn-frontpage-2026-11-24.json`。
- **官方资料**：Python 列表与字典官方说明：[Data Structures — Python 3 Documentation](https://docs.python.org/3/tutorial/datastructures.html)。
- **作者说明**：第 5 节的 4 行代码为测试「0 起始索引」与「字段名拼写核对」设计的监工练习。
