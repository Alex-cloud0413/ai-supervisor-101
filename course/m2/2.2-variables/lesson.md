# 2.2 变量：给数据贴标签

> 学习目标：看懂 Python 里的变量赋值（`=`）和 4 种常见数据类型，能在代码差异（Diff）里一眼核对「AI 改了哪个设置值、有没有把数字当文字算」。
>
> 演示环境：Python `3.12.16`，延续 `ai-radar` 项目的 `practice/scripts/build_top10.py` 与真实 OpenRouter 模型报价快照。

---

## 1. 汇率改个数字，3 秒验收完一整份脚本

做完 0.1 课的比价表后，假设下周美元汇率涨到了 `7.3`，团队又说：「只看前 10 个太少了，给我拉前 20 名出来。」

你给 AI 发了一句话让它改一下。几秒后，右侧代码差异（Diff）面板弹出两处变动：

```diff
- EXCHANGE_RATE = 7.2
+ EXCHANGE_RATE = 7.3
- TOP_N = 10
+ TOP_N = 20
```

你根本不需要去读底下 140 行算价和画表格的代码，只扫这 4 行红绿字，3 秒就能确认两件事：AI 只动了汇率和条数，而且两个数字都改对了。

这 4 行里最左边的 `EXCHANGE_RATE` 和 `TOP_N`，就是 Python 里的**变量（Variable）**。看懂变量，你就拿到了整份脚本的「仪表盘」。

---

## 2. 系统位置：变量是 AI 存放设置值和中间结果的「贴签盒子」

回到脚本内部，变量串起了每一步的数据流转：

```
顶部配置变量（监工最常调的参数：文件路径、汇率、取前几名） ← 【本课位置】
      ↓
中间计算变量（读取进来的 470 个模型、换算后的单价、综合均价）
      ↓
把结果写进 Excel 表格并打印摘要
```

如果一份代码把 `7.2` 散落在第 30 行、第 75 行、第 120 行到处硬写，AI 改汇率时就很容易漏改一处；把它抽成顶部一个叫 `EXCHANGE_RATE` 的变量，改一次，全脚本跟着同步生效。

---

## 3. 讲清楚：变量赋值 + 4 种必认数据类型

### 3.1 变量是什么：`=` 是「装进去」，不是数学里的「等于」

把变量想成一个贴了名字标签的收纳盒：

```python
EXCHANGE_RATE = 7.2
```

- **左边**（`EXCHANGE_RATE`）：盒子外面的标签名（不能有空格，不能用数字开头，常在单词间用下划线 `_` 连接）。
- **中间**（`=`）：动作——**「把右边的值装进左边这个盒子里」**。
- **右边**（`7.2`）：真正装进去的数据。

**最常见的误解**：按中学数学的习惯把 `=` 读成「两边相等」。所以在代码里看到 `count = count + 1` 时会懵：「一个数怎么可能等于它自己加 1？」换成收纳盒的读法就通了——**先把 `count` 盒子里原来的数字拿出来加 1，再放回 `count` 盒子里盖住旧值**。在 Python 里，真正问「两边相不相等」用的是两个等号 `==`（2.4 课会用到）。

还有一个业内默契：**全大写带下划线的变量名**（比如 `DATA_PATH`、`OUTPUT_PATH`、`EXCHANGE_RATE`、`TOP_N`），一般表示「放在文件最顶上的固定配置项（常量）」。你每次想调整口径，先去脚本前 25 行找全大写的名字准没错。

### 3.2 4 种必认数据类型（加没加引号，天差地别！）

装进盒子的数据有不同「材质」，Python 里最常碰到的就 4 种：

| 类型 | 英文名 | 长什么样 | `ai-radar` 里的真实例子 | 监工要注意什么 |
|---|---|---|---|---|
| 文字（字符串） | `str` | **必须带引号**（`'...'` 或 `"..."`） | `"google/gemma-3-4b-it"`、`"0.00000004"` | **哪怕里面是数字，只要套了引号就是文字，不能直接乘小数** |
| 整数 / 小数 | `int` / `float` | **不带引号**的纯数字 | `10`、`131072`、`7.2`、`0.324` | 可以做加减乘除和比大小 |
| 开关（布尔值） | `bool` | 只有 `True`（真/开）和 `False`（假/关），首字母大写、不带引号 | `exclude_batch = True` | 别写成带引号的 `"False"`（带引号会变成普通文字，反而被当成「开」！） |
| 空值 | `None` | 只有一个 `None`，首字母大写 | `context_length = None` | 表示「这里压根没填数据」，不是数字 `0`，也不是空白文字 `""` |

### 3.3 真实大坑：OpenRouter 快照里的「伪数字」

打开 `practice/data/openrouter-models-2026-11-24.json`，看 `google/gemma-3-4b-it` 的真实价格字段：

```json
"pricing": {
  "prompt": "0.00000004",
  "completion": "0.00000005"
}
```

注意看 `"0.00000004"` 两边——**带着双引号**！也就是说，OpenRouter 传回来的是**字符串（文字）**，而不是小数。

如果 AI 偷懒直接拿它去乘汇率 `7.2`，Python 立刻翻脸报错：

```text
TypeError: can't multiply sequence by non-int of type 'float'
```

翻译成白话就是：「你不能拿一段文字去乘一个小数。」所以必须先套一层 `float(...)` 把文字转成小数，才能安全算钱。

---

## 4. 现场看：`build_top10.py` 里的配置区和换算变量

打开 `practice/scripts/build_top10.py` 的第 16–21 行，就能看到整份脚本的「顶部仪表盘」：

```python
# 1. 顶部配置变量（监工最常核对、改动的一块）
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "openrouter-models-2026-11-24.json"
OUTPUT_PATH = BASE_DIR / "output" / "模型比价Top10.xlsx"
EXCHANGE_RATE = 7.2
TOP_N = 10
```

扫一眼这 5 个变量，4 个关键信息全部锁死：
1. `DATA_PATH` 指着 11 月 24 日的原始快照；
2. `OUTPUT_PATH` 指着 `output/` 文件夹（绝不覆盖 `data/`）；
3. `EXCHANGE_RATE` 汇率是纯小数 `7.2`（没加引号）；
4. `TOP_N` 取前 `10` 名，是纯整数 `10`。

再看第 72–76 行，脚本怎样把 OpenRouter 的字符串单价算成人民币综合均价：

```python
    prompt_usd_m = float(pricing["prompt"]) * 1_000_000
    completion_usd_m = float(pricing["completion"]) * 1_000_000
    prompt_cny_m = prompt_usd_m * exchange_rate
    completion_cny_m = completion_usd_m * exchange_rate
    avg_cny_m = (prompt_cny_m + completion_cny_m) / 2.0
```

顺便认两个小细节：
- `float(...)` 就是刚才说的「把带引号的 `"0.00000004"` 脱掉引号变成小数 `0.00000004`」；
- `1_000_000` 里的下划线只是为了让你一眼数清有 6 个零（代表「每百万 Token」），Python 读它和读 `1000000` 完全一样。

---

## 5. 你来读：看这段 Diff，10 秒挑出 2 个隐患

你让 AI 把脚本改成「用最新 12 月快照、汇率调成 7.3、只输出前 5 名」，结果右侧 Diff 面板亮出下面 6 行改动：

```diff
- DATA_PATH = BASE_DIR / "data" / "openrouter-models-2026-11-24.json"
+ DATA_PATH = BASE_DIR / "data" / "openrouter-models-2026-12-01.json"
- OUTPUT_PATH = BASE_DIR / "output" / "模型比价Top10.xlsx"
+ OUTPUT_PATH = BASE_DIR / "data" / "模型比价Top5.xlsx"
- EXCHANGE_RATE = 7.2
+ EXCHANGE_RATE = "7.3"
- TOP_N = 10
+ TOP_N = 5
```

停下来想 10 秒：先别点运行，这段改动里藏着哪 **2 个** 必须立刻打回的问题？

**判断思路**：
1. **`EXCHANGE_RATE = "7.3"` 多套了引号**：把小数变成了文字（`str`），下面一旦拿美元单价去乘 `exchange_rate`，程序立刻报 `TypeError` 崩掉；应该改成不带引号的 `7.3`。
2. **`OUTPUT_PATH` 写进了 `"data"` 目录**：按我们的工作区规矩，`data/` 只放原始只读快照，生成出来的 Excel 必须写到 `output/` 文件夹（`BASE_DIR / "output" / "模型比价Top5.xlsx"`），不能把产物混进原始数据目录。

---

## 6. 小检查（3 道判断题）

1. 在 Python 里，`EXCHANGE_RATE = 7.2` 和 `EXCHANGE_RATE = "7.2"` 效果完全一样，都能直接拿来乘单价。（对 / 错）
2. 看到代码里写 `count = count + 1`，意思是把 `count` 原来的值加 1 后，再存回 `count` 这个变量里。（对 / 错）
3. 代码顶部出现 `DATA_PATH`、`OUTPUT_PATH`、`TOP_N` 这类全大写变量名，通常是专门集中放置配置参数的地方，方便后续核对和调整。（对 / 错）

---

## 7. 下一课

认清了单个数据怎么贴标签，下一课来看成百上千条数据怎么打包在一起。下一课 **2.3《列表与字典：数据长什么样》**，把 `openrouter-models-2026-11-24.json` 里满屏的 `[]` 和 `{}` 拆开给你看。

---

## 小检查答案

1. **错**。带引号的 `"7.2"` 是字符串（文字），不是数字，直接和小数相乘会触发 `TypeError`。
2. **对**。在 Python 中单个 `=` 是「赋值」（把右边结果装进左边盒子），不是数学等式。
3. **对**。把配置常量全大写集中在脚本顶部是常见规范，监工改口径或核对 Diff 时最先看的就是这一块。

---

## 参考与事实边界

- **实际操作结果**：本课引用的配置常量、换算代码和 `TypeError` 报错均实测自仓库 `practice/scripts/build_top10.py`、`practice/data/openrouter-models-2026-11-24.json` 与 `Python 3.12.16`。
- **官方资料**：Python 内置数据类型说明：[Built-in Types — Python 3 Documentation](https://docs.python.org/3/library/stdtypes.html)。
- **作者说明**：第 5 节的 Diff 为依据真实高频失误设计的监工找错练习。
