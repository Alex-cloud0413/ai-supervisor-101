# 2.6 函数：把功能打包

> 学习目标：看懂 `def`（定义函数）、参数（传进去的材料）和 `return`（交出来的结果），拿到一两百行的 AI 脚本时，能先看目录骨架再直奔要查的那一块。
>
> 演示环境：Python `3.12.16`，延续 `ai-radar` 项目的 `practice/scripts/build_top10.py`（188 行）和 `practice/scripts/fetch_snapshots.py`（42 行）。

---

## 1. 188 行代码，真要从第 1 行啃到最后一行吗？

随着你的需求越来越实用，AI 写出来的 `.py` 脚本很快就会从 20 行长到 150 行、300 行。拿仓库里的 `practice/scripts/build_top10.py` 来说，一共 188 行。

假设老板今天说：「表头里的中文列宽太窄，帮我调宽一点。」或者你说：「再加一条过滤，只看上下文超过 128K 的模型。」

如果每改一个小点都要从第 1 行读到第 188 行，谁都会头大。好消息是：**专业的脚本从不把 188 行糊成一锅粥，而是用 `def` 拆成一个个贴着门牌的独立「功能部门」**——这就是**函数（Function）**。

认出 `def`，不管脚本有多长，你 10 秒就能先扫出「目录清单」，然后只点开对应的那一个部门验收，剩下 80% 的代码直接略过。

---

## 2. 系统位置：函数把长脚本拆成清晰的「流水线部门」

把 `practice/scripts/build_top10.py` 的 188 行抽离成函数部门图，整份脚本其实只有 5 个部门，由最底下的 `main()` 总调度按顺序串联：

```
入口总开关：if __name__ == "__main__": main()
                     ↓
  ┌──────────────────────────────────────────────────────┐
  │ 1. load_models(DATA_PATH)           → 读 JSON，交出 470 个模型 │
  │ 2. select_top_models(models, ...)   → 批量筛选、算价、排前 10  │ ← 【本课位置】
  │      ├── 内部调用 is_valid_chat_vision_model(model)   │
  │      └── 内部调用 calc_cny_pricing(model, rate)       │
  │ 3. save_excel(top_models, ...)      → 写出带样式的 Excel     │
  └──────────────────────────────────────────────────────┘
```

改表头和列宽？直奔 `save_excel()`。改筛选门槛？直奔 `is_valid_chat_vision_model()`。改综合均价公式？直奔 `calc_cny_pricing()`。职责一清二楚。

---

## 3. 讲清楚：`def`、参数、`return` 和 `if __name__ == "__main__":`

### 3.1 函数的 3 个固定零件

看一个最精简的真实例子（摘自 `build_top10.py` 第 24–28 行）：

```python
def load_models(json_path: Path) -> list[dict]:
    """读取 JSON 快照，返回模型字典列表。"""
    with json_path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return raw_data.get("data", [])
```

拆成 3 块看：
1. **门牌和入口材料（第 1 行）**：
   - `def`（define 的缩写）宣告「这里开始定义一个函数」；
   - `load_models` 是函数名字（好名字本身就是说明书，一眼知道它干嘛）；
   - 括号里的 `json_path` 是**参数（Parameter）**——调用这个函数时要递进去的材料（路径）。后面带冒号和箭头的 `: Path`、`-> list[dict]` 是可选的「类型提示标签」，纯粹写给人看，提醒「进来的是路径、出去的是字典列表」。
2. **加工步骤（第 2–4 行）**：缩进 4 格，第一行三引号 `"""..."""` 是中文说明（文档字符串），底下是干活代码。
3. **交出成品（第 5 行 `return`）**：把算好的结果递回给外面喊它干活的人，并且立刻结束这个函数。

顺手认一下**带默认值的参数**：在 `def select_top_models(models, exchange_rate=EXCHANGE_RATE, top_n=TOP_N):` 里，带 `=` 号的参数表示「如果调用时不专门传新值，就默认用顶部配置里的 `7.2` 和 `10`」。

### 3.2 最常见的误解：分清 `print()` 和 `return`

很多零基础看代码时，会把函数里的 `print(...)` 当成「结果交出来了」。完全不是一回事：

- **`print(结果)`**：只是把字打在黑色终端屏幕上**给人的眼睛看**，后面的代码根本接不住它；
- **`return 结果`**：才是真正把成品递给下一道工序（下一个变量或下一个函数）继续加工。

如果 AI 在写筛选函数时忘了写 `return qualified`，只写了一句 `print(qualified)`，那外面 `top_models = select_top_models(models)` 接到的就会是空值 `None`，下一行写 Excel 立刻报错崩掉！

### 3.3 文件最底下那句神秘咒语：`if __name__ == "__main__":`

几乎每份规整的 Python 脚本末尾都有这两行：

```python
if __name__ == "__main__":
    main()
```

不用死记英文，把它翻译成一句话就行：**「如果你是在终端直接运行这份脚本，就从 `main()` 这里正式开工；如果只是别的脚本把里面的某个函数借去用，就先别自动跑。」**

当监工读一份陌生的长脚本时，**最高效的读法不是从第 1 行往下硬看，而是先直接拉到文件最底下看 `main()`**——6 行代码就能把整份脚本的全局流程摸透。

---

## 4. 现场看：用「先看 `main()` 再定位 `def`」速读仓库里的两份真实脚本

### 4.1 速读 `practice/scripts/build_top10.py`（188 行）

直接拉到文件末尾第 173–188 行：

```python
def main() -> None:
    models = load_models(DATA_PATH)
    top_models = select_top_models(models, exchange_rate=EXCHANGE_RATE, top_n=TOP_N)
    save_excel(top_models, OUTPUT_PATH, exchange_rate=EXCHANGE_RATE)

    print(f"已读取 {len(models)} 个模型，筛出前 {len(top_models)} 名，保存至 {OUTPUT_PATH.relative_to(BASE_DIR)}")
    for rank, item in enumerate(top_models[:5], start=1):
        print(...)
```

只看这 3 行调用链，整份 188 行脚本的来龙去脉全部透明：
- 想换数据源或检查读文件有没有错 → 看 `load_models`；
- 想查为什么某个模型没排进前 10 → 看 `select_top_models`（及其内部的 `is_valid_chat_vision_model` 和 `calc_cny_pricing`）；
- 想改 Excel 颜色、列宽、小数位数 → 看 `save_excel`。

### 4.2 再顺手速读 `practice/scripts/fetch_snapshots.py`（42 行）

同样直接看它的函数骨架：

```python
def fetch_json(url: str) -> dict: ...   # 发网络请求，把网址返回的 JSON 转成 Python 字典

def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    for prefix, url in SOURCES.items():
        payload = fetch_json(url)
        out_path = DATA_DIR / f"{prefix}-{today}.json"
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved {out_path} ({out_path.stat().st_size:,} bytes)")
```

哪怕你从未学过网络请求，光看 `fetch_json` 和 `main` 两个名字，10 秒就能看出它干的事：循环抓取 `SOURCES` 里的两个公开网址，按今天日期存进 `data/` 目录，完事打印文件字节数。

---

## 5. 你来读：看这份 4 函数骨架，10 秒定位 3 个问题

以后在 M5 搭每日情报早报时，AI 写出了一份 140 行的 `daily_briefing.py`。你直接拉到底部和各个 `def` 行，看到了下面这份骨架：

```python
def fetch_hn_stories(url: str, timeout: int = 15) -> list[dict]:
    ...

def filter_ai_stories(stories: list[dict], keywords: list[str]) -> list[dict]:
    matched = [s for s in stories if any(k in s["title"].lower() for k in keywords)]
    print(f"命中 {len(matched)} 条 AI 热帖")

def render_markdown(ai_stories: list[dict]) -> str:
    ...

def save_briefing(markdown_text: str, output_path: Path) -> None:
    ...

def main() -> None:
    stories = fetch_hn_stories(HN_URL)
    ai_stories = filter_ai_stories(stories, KEYWORDS)
    md = render_markdown(ai_stories)
    save_briefing(md, OUTPUT_PATH)
```

停下来想 10 秒：
1. 如果生成的早报 Markdown 里「每条新闻缺了原文链接」，你应该让 AI 去查哪个函数？
2. 如果拉取 Hacker News 时经常网络超时，应该调哪个函数的参数？
3. 盯着 `filter_ai_stories` 这 3 行看——里面藏着一个**一定会让程序崩掉的漏写**，是什么？

**判断思路**：
1. 缺链接属于拼装 Markdown 内容的问题，直奔 `render_markdown()`。
2. 网络超时直接看 `fetch_hn_stories()` 的 `timeout` 参数（比如从 `15` 秒调宽或加一次重试）。
3. **`filter_ai_stories` 忘了写 `return matched`！** 它只写了 `print(...)` 打印到屏幕，没有把筛出来的列表交回给 `main()`，导致 `ai_stories` 变成 `None`，下一步传给 `render_markdown(ai_stories)` 就会直接报错。

---

## 6. 小检查（3 道判断题）

1. 在 Python 里，`def` 关键字用来定义一个打包好的功能块（函数），括号里放传进去的材料（参数）。（对 / 错）
2. 函数里写完 `print(result)`，外面的代码就能直接拿这个 `result` 去做下一步计算，不需要写 `return`。（对 / 错）
3. 拿到一份超过 150 行的 AI 脚本时，先看文件底部的 `main()` 和所有 `def` 函数名，能快速理清整体流程并锁定要检查的代码块。（对 / 错）

---

## 7. 下一课

到这里，脚本里面自己写的代码你都能拆明白。但有没有注意过 `build_top10.py` 最顶上那几行 `import json`、`import openpyxl`？为什么 `fetch_snapshots.py` 什么都不用装就能跑，而 `build_top10.py` 却要跑 `pip install openpyxl`？下一课 **2.7《库与 `pip install`》**，教你认清标准库和第三方库，并防住包名投毒陷阱。

---

## 小检查答案

1. **对**。`def 函数名(参数):` 是定义函数的标准写法。
2. **错**。`print()` 只把文字输出到屏幕给人看，不会把值交回给调用方；必须用 `return result` 才能把结果传给后续步骤。
3. **对**。自底向上先读 `main()` 调度链，再按需点开对应 `def` 细节，是审阅长脚本最高效的监工读法。

---

## 参考与事实边界

- **实际操作结果**：本课拆解的函数签名与调度流程直接摘自仓库实测可运行的 `practice/scripts/build_top10.py` 与 `practice/scripts/fetch_snapshots.py`。
- **官方资料**：Python 函数定义官方说明：[More Control Flow Tools — Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)。
- **作者说明**：第 5 节 `daily_briefing.py` 为承接 M5 每日早报场景设计的函数定位与 `return` 漏写排查练习。
