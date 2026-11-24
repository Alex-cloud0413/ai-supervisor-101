# 2.5 `for`：批量处理

> 学习目标：看懂 `for ... in ...:` 循环、`continue`（跳过这一条）和 `break`（立刻停止整个循环），能判断 AI 的批量处理代码会不会提前漏项、重复写入或扫错文件范围。
>
> 演示环境：Python `3.12.16`，延续 `ai-radar` 项目，实测处理 `practice/data/openrouter-models-2026-11-24.json`（470 个模型）与 `practice/data/hn-frontpage-2026-11-24.json`（30 条首页热帖）。

---

## 1. 同样一套动作，自动跑 470 遍和跑 30 遍

2.4 课我们拆完了给「单个模型」做安检的 4 道 `if` 门。问题来了：`openrouter-models-2026-11-24.json` 里有 **470** 个模型，`hn-frontpage-2026-11-24.json` 里有 **30** 条首页热帖；等到 M5 跑定时任务，文件夹里还会攒下几十天的历史快照。

AI 当然不可能把同一段代码复制粘贴 470 次。它在代码里只写短短一行：

```python
for model in models:
```

就这一句，电脑会自动把 `models` 列表里的 470 个模型一个接一个送进流水线，不到 0.1 秒全部筛完。你以后让 AI 批量重命名 200 张图片、合并 12 个月表格、每天扫一遍 30 条科技热点，背后核心全都是这个 **`for` 循环（Loop）**。

---

## 2. 系统位置：`for` 是把数据逐条送进流水线的「传送带」

回到 `build_top10.py` 的处理链路：

```
470 个模型的列表（models）
      ↓
for model in models:  ← 【本课位置：传送带逐条送货】
  ├── 拿第 1 条 → 过 if 闸机 → 合格就算价装进新列表 qualified；不合格就 continue 跳过
  ├── 拿第 2 条 → 过 if 闸机 → ……
  └── …… 一直跑到第 470 条自动结束
      ↓
跳出传送带（取消缩进）→ 统一排序、截前 10 名、一次性写入 Excel
```

看懂传送带的起点、终点和缩进边界，你就能判断 AI 有没有漏处理数据，或者有没有把「只该做一次的保存动作」错塞进了循环里。

---

## 3. 讲清楚：`for` 的读法、`continue` vs `break` 和两个高频搭档

### 3.1 怎么把 `for` 翻译成顺口中文

标准句式永远长这样：

```python
for 单项变量名 in 列表或集合:
    缩进 4 格：对每一条都要重复做的事
取消缩进：全部跑完以后才做一次的事
```

把它念成中文就是：**「对于右边集合里的每一个元素，临时起个名字叫左边变量，然后把下面缩进的代码逐条执行一遍。」**

注意一个和 2.4 课一脉相承的细节：**缩进决定「在传送带上」还是「下传送带后」**。
- 往右退 4 格的代码：470 条数据每来一条就跑一次；
- 退回左侧对齐的代码：等 470 条全部过完传送带，最后才统一执行一次（例如排序 `qualified.sort(...)` 和保存文件 `wb.save(...)`）。

### 3.2 最容易看混的一对词：`continue` vs `break`

在循环里面经常冒出这两个英文词，字面看着都像「停一下」，效果却天差地别：

| 关键词 | 白话意思 | 放进 470 个模型的循环里会发生什么 |
|---|---|---|
| `continue` | **跳过当前这一条，马上看下一条** | 碰到 `openrouter/auto` 不合口径，扔掉它，传送带继续看后面 469 个模型 |
| `break` | **立刻拉闸停机，后面全都不看了** | 碰到第一个不合口径的模型就当场收工，剩下几百个模型直接漏掉！ |

**最常见的翻车点**：在过滤列表的 `for` 循环里，AI 或新手不小心把 `continue` 写成了 `break`。程序照样不报错，也能顺利生成 Excel——只是表里要么空空如也，要么只剩前面 2 个模型，后面几百个全丢了。

### 3.3 监工必认的两个高频搭档

1. **`enumerate(列表, start=1)`**：一边跑循环，一边自动给你配上从 `1` 开始的排名序号。写进 Excel 时顺手就能把第 1 列填成 `1, 2, 3...10`，不用自己手动加 1。
2. **`Path("data").glob("*.json")`**：按扩展名批量找出某个文件夹下的所有同类文件（比如以后攒了 30 天快照，用 `for path in Path("data").glob("*.json"):` 就能一口气全扫一遍）。

---

## 4. 现场看：`ai-radar` 里的两组真实 `for` 循环

### 4.1 `build_top10.py`：一边筛 470 个模型，一边逐行写 Excel

看 `practice/scripts/build_top10.py` 第 91–104 行：

```python
def select_top_models(models, exchange_rate=EXCHANGE_RATE, top_n=TOP_N):
    qualified = []
    for model in models:
        if not is_valid_chat_vision_model(model):
            continue
        qualified.append(calc_cny_pricing(model, exchange_rate))

    qualified.sort(key=lambda item: (item["avg_cny"], item["prompt_cny"], item["completion_cny"]))
    return qualified[:top_n]
```

扫 3 个关键信号：
- `for model in models:` 把 470 个模型逐个送进来；
- 不合规时用 `continue`（跳过这一条，绝不用 `break`）；
- `qualified.append(...)` 把合规模型算完人民币价格后追加到 `qualified` 列表末尾；
- 取消缩进后，统一排序并切片 `[:top_n]` 取前 10 名。

再看第 142–164 行往 Excel 填数据：

```python
    for rank, item in enumerate(top_models, start=1):
        row_num = rank + 2
        ...
```

这里就是用 `enumerate(..., start=1)` 自动生成 `1` 到 `10` 的排名，顺手把写入行号对齐到第 3–12 行（避开第 1 行大标题和第 2 行表头）。最后 `wb.save(output_path)` 写在循环外面（取消缩进），等 10 行全写完才保存一次文件。

### 4.2 用 `for` 循环扫一遍 Hacker News 30 条热帖，筛出 AI 情报

这套循环换到下半场的每日情报早报完全通用。下面这段 10 行代码实测扫描 `practice/data/hn-frontpage-2026-11-24.json`：

```python
keywords = ["ai", "llm", "model", "nvidia", "oss", "openai", "anthropic", "dario"]

ai_hits = []
for story in hits:
    title = (story.get("title") or "").lower()
    if any(word in title for word in keywords):
        ai_hits.append(story)
```

在本机 `Python 3.12.16` 实测运行，30 条首页热帖瞬间精准筛出 **6 条** AI 圈高热帖：

```text
HN total=30, AI-keyword matches=6
  [2723 pts] Nvidia Reinstates Jensen Huang as CEO
  [1909 pts] "Dario is hyping the dangers so OSS models are illegal and he stays in control"
  [518 pts] LLM agents work for their parent companies, not for you
  [240 pts] Who in Washington owns and trades Nvidia stock
  [86 pts] Declare is a UI language for you and your AI
  [13 pts] A training engine for your local model, using your idle compute
```

---

## 5. 你来读：这两段 `for` 循环都有硬伤，10 秒挑出来

AI 帮你写了一段「筛模型并保存 Excel」的脚本片段：

```python
qualified = []
for model in models:
    if not is_valid_chat_vision_model(model):
        break
    qualified.append(calc_cny_pricing(model, EXCHANGE_RATE))

for rank, item in enumerate(qualified[:10], start=1):
    write_row(ws, rank + 2, item)
    wb.save(OUTPUT_PATH)
```

停下来想 10 秒：第一段循环和第二段循环里，各藏着一个什么问题？

**判断思路**：
1. **第一段把 `continue` 写成了 `break`**：只要 470 个模型里遇到第一个不合规的模型（比如排在前面的动态路由或纯文本模型），循环立刻拉闸中止，后面几百个合规模型全都不会被检查，结果大概率筛出 0 个或极少数模型。必须改回 `continue`。
2. **第二段把 `wb.save(OUTPUT_PATH)` 错缩进放进了循环里面**：每写一行就重新保存一整份 Excel，10 行就反复读写硬盘 10 次（如果是 1 万行大表会慢到卡死）。应该把 `wb.save(OUTPUT_PATH)` 往左退 4 个空格，移到 `for` 循环外面，等全部行写完统一保存一次。

---

## 6. 小检查（3 道判断题）

1. 在筛选 470 个模型的 `for` 循环里，遇到不合规的模型想跳过它继续看下一个，应该写 `continue` 而不是 `break`。（对 / 错）
2. 看到代码里 `wb.save(OUTPUT_PATH)` 这一行和 `for` 顶头对齐（没有缩进），说明它会在所有循环跑完之后只执行一次。（对 / 错）
3. `for path in Path("data").glob("*.json"):` 的意思是逐个处理 `data` 文件夹下所有以 `.json` 结尾的文件。（对 / 错）

---

## 7. 下一课

到这里，单个脚本里的四大积木（变量、列表字典、`if`、`for`）你全都认齐了。但当 AI 写出 150 行甚至 300 行代码时，怎么做到不用逐行硬啃、10 秒直奔要改的那一块？下一课 **2.6《函数：把功能打包》**，教你用 `def` 给代码画「部门分工图」。

---

## 小检查答案

1. **对**。`continue` 跳过当前条目进入下一轮；`break` 会直接终止整条循环。
2. **对**。取消缩进代表已离开 `for` 循环体，会在全部条目遍历结束后执行一次。
3. **对**。`glob("*.json")` 按通配符匹配目录内所有 `.json` 文件，配合 `for` 即可批量处理。

---

## 参考与事实边界

- **实际操作结果**：本课 `select_top_models`、`save_excel` 代码摘自仓库 `practice/scripts/build_top10.py`；Hacker News 30 条热帖中命中 6 条 AI 相关帖子的结果，均在 `Python 3.12.16` 上对 `practice/data/hn-frontpage-2026-11-24.json` 实测获得。
- **官方资料**：Python `for` 循环与 `break` / `continue` 说明：[More Control Flow Tools — `for` Statements](https://docs.python.org/3/tutorial/controlflow.html#for-statements)。
- **作者说明**：第 5 节的 2 处循环缺陷为提炼自高频逻辑与性能错误的监工练习。
