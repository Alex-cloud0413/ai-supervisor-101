# 4.2 读懂 diff

> 学习目标：看懂 `git diff` 的 4 个核心元素（文件头、`@@` 行号块、红 `-` 删行、绿 `+` 增行）和 `git diff --stat` 改动清单，能在 15 秒内判断 AI 的修改是否精准、有没有改反口径或越界乱动文件。
>
> 演示环境：Git `2.56.1`（Mac 终端与 Windows PowerShell 通用），使用 `ai-radar` 沙盒中的真实 `config.yaml` 与 `scripts/daily_briefing.py` 实测 `git diff` 输出。

---

## 1. AI 说「已经按要求改好了」，你总不能重读 200 行代码吧？

4.1 课我们学会了打存档和读档，但监工日常最常卡在中间那一步：你让 AI 给 `daily_briefing.py` 优化一下热点筛选逻辑，10 秒后它回你一句「已完成修改」。

这时候你面前摆着 156 行 Python 代码。从第 1 行逐行通读太耗时；闭着眼睛直接信任它，又怕它顺手把排序方向写反，或者偷偷改了不该动的文件。

程序员和 AI 监工的共同法宝，叫 **`diff`**（读作「迪夫」，英文 difference 差异的缩写）：**它自动隐藏没动的 150 行，只把「删掉了哪几行、新增了哪几行」拎出来并排给你看。** 学会读 `diff`，15 秒就能验收完一次修改。

---

## 2. 系统位置：`diff` 是「AI 交卷」和「你按下存档」之间的质检仪

不管你在终端敲 `git diff`、在 DeepSeek Harness 界面里看改动卡片，还是在 GitHub 网页上审核 Pull Request（4.7 课），底层的阅读规矩完全一样：

```
AI 动手修改文件（比如改了 config.yaml / daily_briefing.py）
      ↓
第 1 眼：git diff --stat      → 先看「动了哪几个文件、每个文件改了几行」（防越界）  ← 【本课位置】
      ↓
第 2 眼：git diff             → 逐块核对红 `-` 删行与绿 `+` 增行（查口径/查误改）   ← 【本课位置】
      ├── 发现改歪 / 动了不该动的文件 ──→ git restore <文件> 或把问题指给 AI 重改
      └── 每一行变化都清清楚楚        ──→ git add . → git commit（安心打存档）
```

---

## 3. 讲清楚：1 分钟认全 `diff` 的 4 个核心记号

下面是一段在 `ai-radar` 里把 `top_n` 从 `5` 改成 `10`、`min_points` 从 `50` 改成 `500` 的真实 `git diff` 片段：

```diff
diff --git a/config.yaml b/config.yaml
index ebfc475..90fa093 100644
--- a/config.yaml
+++ b/config.yaml
@@ -9,7 +9,7 @@ project:
 model_pricing:
   snapshot_file: openrouter-models-2026-11-24.json
   exchange_rate: 7.2
-  top_n: 5
+  top_n: 10
   exclude_prefixes:
     - "~"
   exclude_suffixes:
@@ -19,7 +19,7 @@ model_pricing:
 daily_briefing:
   snapshot_file: hn-frontpage-2026-11-24.json
   output_file: daily-briefing.md
-  min_points: 50
+  min_points: 500
   max_items: 8
   keywords:
     - ai
```

不要被前面的符号吓住，从上到下只认 4 样东西：

| 记号 / 区块 | 示例 | 一句话翻译 | 监工盯什么 |
|---|---|---|---|
| **① 文件头** | `--- a/config.yaml`<br>`+++ b/config.yaml` | `--- a/` 是改之前的旧文件，`+++ b/` 是改之后的新文件 | **第一眼先核对文件名**：AI 有没有动到我没让它改的文件（尤其是 `data/` 原表）？ |
| **② 行号块头（Hunk）** | `@@ -9,7 +9,7 @@ project:` | 原文件从第 `9` 行起共 `7` 行 → 改后从第 `9` 行起共 `7` 行 | 知道改动落在大致哪一段；在 `.py` 文件里末尾还会贴心显示所在函数名（如 `def pick_hn_ai_stories`） |
| **③ 删行（红 `-`）与增行（绿 `+`）** | `-  top_n: 5`<br>`+  top_n: 10` | **在 Git 眼里没有「原地修改」，改一行等于「删掉旧行 `-` + 插入新行 `+`」** | 逐对对照旧值和新值：数字对不对、符号有没有写反（如 `<` 变 `<=`、`True` 变 `False`）？ |
| **④ 空白开头行（上下文）** | `  exchange_rate: 7.2` | 没发生变化的相邻 3 行，用来帮你认清前后语境 | 确认周围代码没被连带破坏 |

### 监工最顺手的 3 条 `diff` 变体命令

| 命令 | 什么时候用 | 看到什么 |
|---|---|---|
| `git diff --stat` | **验收第一步（强烈推荐）** | 一张极简汇总表：列出所有被改动的文件名和增删行数（例如 `config.yaml \| 4 ++--`），3 秒就能揪出「明明只让改配置，怎么动了 `data/`」的越界行为 |
| `git diff` | 验收还没 `git add` 的改动 | 逐行展示全部红删绿增细节 |
| `git diff --staged` | 已经 `git add` 进暂存箱、准备 `commit` 前最后复核 | 只看即将打进下一档的改动（注意：执行完 `git add` 后，直接敲 `git diff` 会变空，要加 `--staged` 才看得到） |

> **小提示**：在终端里 `git diff` 很长时，可能进入翻页浏览模式（底部冒出一个冒号 `:`），按空格键往下翻页，按英文小写 **`q`** 键（quit）即可随时退出回到命令行。

**最常见的误解**：以为「看到一堆红色 `-` 就说明 AI 删坏了东西，看到全是绿色 `+` 就安全」。**不一定！** 改一个变量值，必然是一红一绿配对出现；反倒是如果只让你改一行参数，结果 `git diff --stat` 冒出 **120 行 `+` 和 118 行 `-`**，往往说明 AI 顺手把整个文件重排了格式（甚至重写了无关逻辑）——这才是监工要立刻叫停的危险信号！

---

## 4. 现场看：15 秒用 `git diff` 抓出 AI 埋进 `daily_briefing.py` 的 2 个暗坑

假设你让 AI 帮忙检查 `scripts/daily_briefing.py` 里的 Hacker News 热点筛选逻辑，它改完后信心满满地说「整理好了」。你在存档前顺手敲了一行：

```bash
git diff scripts/daily_briefing.py
```

终端实测吐出下面这段短短 20 行的 `diff`：

```diff
diff --git a/scripts/daily_briefing.py b/scripts/daily_briefing.py
index e7d6166..11d4859 100644
--- a/scripts/daily_briefing.py
+++ b/scripts/daily_briefing.py
@@ -85,7 +85,7 @@ def pick_hn_ai_stories(data_path: Path, cfg: dict) -> list[dict]:
     for item in hits:
         title = item.get("title") or ""
         points = int(item.get("points") or 0)
-        if points < min_points:
+        if points <= min_points:
             continue
         if any(k in title.lower() for k in keywords):
             matched.append({
@@ -95,7 +95,7 @@ def pick_hn_ai_stories(data_path: Path, cfg: dict) -> list[dict]:
                 "url": item.get("url") or f"https://news.ycombinator.com/item?id={item.get('objectID', '')}",
             })
 
-    matched.sort(key=lambda x: x["points"], reverse=True)
+    matched.sort(key=lambda x: x["points"], reverse=False)
     return matched[:max_items]
```

看懂没？根本不用通读 156 行代码，盯着两处红绿配对，**15 秒就能抓出 2 个致命口径错误**：

1. **第 1 处（第 88 行附近）**：`- if points < min_points:` 被改成了 `+ if points <= min_points:`。
   - 结合 2.4 课学过的 `if` 条件：原本 `50` 分及格就会留下来；改成 `<=` 之后，**刚好 `50` 分的热帖会被直接跳过踢掉**，和 `config.yaml` 简报里写的「热度门槛 `>= 50` 分」互相打架！
2. **第 2 处（第 98 行附近）**：`- matched.sort(..., reverse=True)` 被改成了 `+ matched.sort(..., reverse=False)`。
   - `reverse=True` 是按分数**从高到低**排（2723 分排第一）；改成 `False` 以后，最冷门的帖子反倒排到了早报头条！

你甚至不需要自己改 Python，直接敲 `git restore scripts/daily_briefing.py` 一键复原，或者把这两行指出来打回给 AI 重改。

---

## 5. 你来读：AI 说「只把汇率改成了 7.3」，你看 `diff` 拦住哪 2 个问题？

你只交代了 AI 一句话：「把 `ai-radar` 的美元汇率改成 `7.3`。」AI 回复「改好了」，你立刻跑了 `git diff --stat` 和 `git diff`：

```text
$ git diff --stat
 config.yaml                               | 3 +--
 data/openrouter-models-2026-11-24.json    | 2 +-
 2 files changed, 2 insertions(+), 3 deletions(-)
```

```diff
diff --git a/config.yaml b/config.yaml
--- a/config.yaml
+++ b/config.yaml
@@ -9,9 +9,8 @@ project:
 model_pricing:
   snapshot_file: openrouter-models-2026-11-24.json
-  exchange_rate: 7.2
+  exchange_rate: 7.3
   top_n: 5
   exclude_prefixes:
     - "~"
   exclude_suffixes:
-    - ":free"
     - ":batch"
```

停下来想 10 秒：在这份改动里，有哪 **2 个** 明显越界或改坏的地方必须立刻叫停？

**判断思路**：
1. **严重越界：AI 偷偷动了只读原料仓 `data/openrouter-models-2026-11-24.json`！** 明明只让改汇率，从 `git diff --stat` 第一眼就能抓出它动了 `data/` 下的原始快照——必须立刻用 `git restore data/openrouter-models-2026-11-24.json` 还原。
2. **夹带误删：在 `config.yaml` 里顺手删掉了 `- ":free"`！** 删掉这行之后，免费限流模型就会重新混进商用付费比价表里（2.4 课刚排查过的坑）。应该立刻指着这行 `-    - ":free"` 让 AI 恢复回来，只保留 `exchange_rate: 7.3` 这一处变化。

---

## 6. 小检查（3 道判断题）

1. 在 `git diff` 输出里，带 `-` 号的行表示改之前的旧内容，带 `+` 号的行表示改之后的新内容；修改一行文字通常会显示为「删掉一行旧的 + 新增一行新的」。（对 / 错）
2. 每次验收 AI 的改动时，先跑一次 `git diff --stat` 能快速看出 AI 到底动了哪几个文件、有没有越界碰过 `data/` 里的原始数据。（对 / 错）
3. 只要看到 `git diff` 里只改动了 2 行、而且没有报错，就不需要核对逻辑了，可以直接 `git commit` 存档。（对 / 错）

---

## 7. 下一课

到这里，打存档（4.1）和看差异验货（4.2）都过关了。但如果今天你想让 AI 做一个「大改版」——比如把早报同时输出成 Excel 和网页版，不确定成不成，又怕改到一半把原本稳稳运行的主版本搅乱怎么办？下一课 **4.3《分支与合并》**，教你给 AI 开一条「平行实验分支」，试成了合并回主线，试崩了一键扔掉！

---

## 小检查答案

1. **对**。Git 的 diff 按行对比，修改一行就是旧行标 `-`、新行标 `+`。
2. **对**。`git diff --stat` 先看全局清单防越界，再用 `git diff` 看具体行变化，是最高效的两步验收法。
3. **错**。改动行数少不代表没暗坑——哪怕只改了 1 个符号（比如 `<` 改成 `<=`、`True` 改成 `False`），整份报表的口径都会完全颠倒，必须盯住红绿两行核对语义。

---

## 参考与事实边界

- **实际操作结果**：本课两段 `git diff`（`config.yaml` 参数变更与 `scripts/daily_briefing.py` 的 `<` / `reverse` 变更）均在 `Git 2.56.1` 下基于配套仓库 `practice/` 沙盒副本实测生成。
- **官方资料**：Git 官方 `diff` 手册：[git-diff Documentation](https://git-scm.com/docs/git-diff)。
- **作者说明**：第 5 节的「改汇率时夹带删 `:free` 并改动 `data/`」为提炼自真实 AI 编程越界案例的监工验收练习。
