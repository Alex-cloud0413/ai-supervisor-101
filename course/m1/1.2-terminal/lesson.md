# 1.2 终端与常用命令

> 学习目标：看懂终端里「提示符 → 动词 → 参数 → 路径」四段结构；认识 12 个高频命令（含 `cd`、`npm`、`npx`、`python` / `python3`、`pip` 等），能看懂 AI 后台在跑什么、也会自己敲安装命令。
>
> 演示环境：Linux / Mac 终端与 Windows PowerShell 双系统对照；命令输出实测于本地「青禾文具」目录。**本课先认识命令，下一课认完危险命令，1.4 课再正式安装工具。**

---

## 1. 那个黑色窗口，为什么躲不开？

不管你看哪个 AI 工具的安装教程，几乎第一页就会蹦出一个黑底白字的方块，让你复制一行天书进去按回车：

```bash
npx @deepseek-ai/dsh web
```

打开 0.1 课里 AI 的「轨迹」流水账，里面也全是类似的英文短词：`ls sales`、`cd sales`、`pip install openpyxl`、`python3 merge_sales.py`。

很多零基础的人一看见这个窗口就发怵：既没有图标也没有按钮，只有一个光标在闪，生怕多敲一个空格就把电脑系统搞崩了。

其实换个视角就不怕了：**平时你在桌面用鼠标双击文件夹（图形界面 GUI），和在黑窗口里打字发指令（命令行界面 CLI），管的是同一台电脑、同一块硬盘。** 你在黑窗口里敲一行 `mkdir output`，桌面的文件夹窗口里下一秒就会多出一个叫 `output` 的新文件夹。

AI 没有手指点鼠标，所以 Harness 替模型干活时走的就是终端这条路。你不需要把命令全背下来手敲，但必须做到两件事：
1. 看到 AI 后台跑过一行命令，一眼知道它在看文件、装插件，还是在跑脚本；
2. 到了 1.4 课装工具时，能自己稳稳敲进 `node -v` 和 `npx @deepseek-ai/dsh web`。

---

## 2. 系统位置：终端是 Harness 动手干活的「施工现场」

回到整条链路，看看终端坐在哪里：

```
你下达任务（自然语言）
        ↓
模型决定怎么干（例如「先看目录，再装 Excel 库，再跑脚本」）
        ↓
Harness 打开终端（Shell）真正敲下命令  ← 【本课位置】
        ↓
终端把执行结果或报错文字吐回给 Harness
        ↓
模型读完输出，决定下一步
```

### 怎么在你自己电脑上打开终端？

- **Mac**：按 `Command + 空格` 调出聚焦搜索，输入「终端」（或 `Terminal`）按回车。
- **Windows**：按键盘左下角 `Win` 键，直接输入「终端」或「PowerShell」，点开 **Windows PowerShell**（优先用 PowerShell，不要用老旧的「命令提示符 CMD」，因为 PowerShell 原生兼容下面绝大多数 Mac/Linux 命令）。

> `[可选补拍：Mac 聚焦搜索打开「终端」与 Windows 开始菜单打开 PowerShell 的对照截图]`

---

## 3. 讲清楚：拆解命令结构 + 12 个必认高频命令

### 3.1 一条命令永远长这 3 段

不管是谁敲的命令，去掉最前面电脑自动显示的「当前位置提示符」（比如 `xiaolin@Mac 青禾文具 %` 或 `PS C:\Users\xiaolin\青禾文具>`），后面你或 AI 输入的内容都按固定顺序排：

```text
ls       -la          sales
↑        ↑            ↑
动词     参数/选项     目标路径
（干什么）（怎么干）    （动哪儿）
```

- **动词（Command）**：永远在最开头，决定动作是什么（看、切目录、新建、运行、删除）。
- **参数 / 选项（Flag / Option）**：通常带 `-` 或 `--`，用来微调动作（比如 `-a` 表示连隐藏文件一起显示，`--version` 表示只查版本号）。
- **目标路径（Argument）**：要操作的文件或文件夹（可以是 1.1 课学过的相对路径或绝对路径）。

### 3.2 第一组：看文件、走目录的 7 个基础命令

这 7 个命令在 Mac 终端和 Windows PowerShell 里几乎完全通用（括号里顺带标出老 CMD 写法，万一在旧教程里碰到也能认出来）：

| 命令 | 英文来历 | 干什么用 | 常见例子 | 监工注意 |
|---|---|---|---|---|
| `pwd` | Print Working Directory | 打印「我现在站在哪个文件夹」 | `pwd` | 在终端里迷路时，第一条就敲它 |
| `ls` | List（老 CMD 叫 `dir`） | 列出当前文件夹里有什么 | `ls`、`ls -la` | 加上 `-a` 才能看到 `.env`、`.git` 这类隐藏项 |
| `cd` | Change Directory | **切换文件夹**（走进或退出目录） | `cd sales`、`cd ..`、`cd ~` | **最容易误解**：敲完 `cd` 不会弹出窗口，只是提示符里的当前路径变了 |
| `mkdir` | Make Directory | 新建文件夹 | `mkdir output` | 只新建空文件夹，非常安全 |
| `cat` | Concatenate（老 CMD 叫 `type`） | 把纯文本文件的内容直接打到屏幕上 | `cat .gitignore` | 适合看 `.md`、`.py`、`.txt`；不要拿它看 `.xlsx`（会吐乱码） |
| `cp` / `mv` | Copy / Move（老 CMD 叫 `copy` / `move`） | 复制文件 / 移动或重命名文件 | `cp a.xlsx b.xlsx`、`mv 旧.xlsx 新.xlsx` | `mv` 后面如果带 `..` 会把文件挪出工作区 |
| `clear` | Clear（老 CMD 叫 `cls`） | 清空终端屏幕显示 | `clear` | **只清屏幕上的字，绝不删硬盘里的任何文件** |

顺带提两个高频辅助词：`which <程序>`（Windows 叫 `where <程序>`）用来查某个程序装在电脑哪个路径；`rm`（Windows 叫 `del`）是**删除文件**——因为删除不可逆，下一课 1.3 我们专门拿整节课做成危险命令识别表。

### 3.3 第二组：装工具、跑脚本必见的 5 个「引擎与商店」命令

零基础看教程和 AI 轨迹时，最容易晕的是这 5 个英文词：`python`、`pip`、`node`、`npm`、`npx`。把它们分成**两对兄弟**，用「手机系统 + 应用商店」来记，一秒分清：

#### 第一阵营：Python 阵营（AI 替你算表格、处理数据时天天见）

- **`python` / `python3`**：启动 Python 解释器来运行 `.py` 脚本。
  - **怎么用**：查版本敲 `python3 --version`（Windows 常直接写 `python --version`）；跑脚本敲 `python3 merge_sales.py`。
  - **为什么有的写 `python`、有的写 `python3`**：Mac 和 Linux 系统历史原因常把新版命令叫 `python3`，Windows 安装官方 Python 后一般直接叫 `python`。看到两个写法，知道是一回事就行。
- **`pip`**（Python Package Installer）：**Python 的应用商店**。
  - **怎么用**：`pip install openpyxl`（或者更稳妥的 `python3 -m pip install openpyxl`）。
  - **为什么老出现**：Python 刚装好时自带功能有限，想让它读写 Excel 表格、解析 PDF，就需要靠 `pip` 去网上免费把 `openpyxl`、`pandas` 这类扩展包（库）装进来。M2 的 2.7 课会展开讲。

#### 第二阵营：Node.js 阵营（1.4 课装 DeepSeek Harness 时马上要用）

- **`node`**：Node.js 运行环境（JavaScript 的本地引擎）。很多现代 AI 工具（包括 DeepSeek Harness）是用它跑起来的。查装没装好，敲 `node -v`。
- **`npm`**（Node Package Manager）：**Node.js 的应用商店**，地位和 Python 里的 `pip` 完全对应，用来下载、安装、更新 Node.js 工具包（例如 `npm install -g <包名>`）。
- **`npx`**（Node Package Execute，装好 Node.js 后随 `npm` 自动附带）：**「免安装即跑」启动器**。
  - **它和 `npm` 差在哪**：`npm install -g` 是把软件正式永久装进系统；`npx` 像手机里的「小程序 / 快应用」——不用先手动安装配置，直接敲 `npx @deepseek-ai/dsh web`，它会自动下载缓存并立刻帮你把 DeepSeek Harness 网页版启动起来。

| 阵营 | 运行引擎（干活本体） | 应用商店（装扩展包） | 免安装即跑启动器 | 课程里什么时候见到 |
|---|---|---|---|---|
| **Python 阵营** | `python` / `python3` | `pip` | — | M2–M6 跑数据汇总、自动化脚本 |
| **Node.js 阵营** | `node` | `npm` | `npx` | **1.4 课立刻用 `npx` 启动 DeepSeek Harness** |

### 3.4 三个最常见的误解

1. **敲了 `cd sales` 没弹出窗口，以为失败了**：`cd` 成功后默认**什么字都不回**，只把光标前面的路径从 `青禾文具` 改成 `青禾文具/sales`。拿不准就敲一句 `pwd` 确认。
2. **屏幕刷出 `npm warn` 就以为安装失败**：`warn`（Warning）只是提醒，不是报错。真正中断任务要看 `Error` 或 `command not found`。
3. **敲 `clear` 会把刚才算出来的文件清空**：完全不会，`clear` 就像拿黑板擦擦掉屏幕上的旧字，硬盘上的文件毫发无损。

---

## 4. 现场看：在「青禾文具」目录里实跑一遍

下面是在本地演示目录 `/tmp/qinghe/青禾文具` 真实敲下上面这组命令后的原样输出，逐段看懂它在发生什么：

```text
# 1. 先确认自己站在哪
$ pwd
/tmp/qinghe/青禾文具

# 2. 走进 sales 文件夹，看看里面有几张表，再退回上一级
$ cd sales
$ pwd
/tmp/qinghe/青禾文具/sales
$ ls
2026-08-销售明细.xlsx  2026-09-销售明细.xlsx  2026-10-销售明细.xlsx
$ cd ..

# 3. 分别检查 Python 阵营和 Node.js 阵营是否就位
$ python3 --version
Python 3.12.16
$ pip --version
pip 26.3 from /opt/pyenv/versions/3.12.16/lib/python3.12/site-packages/pip (python 3.12)
$ node -v
v22.23.5
$ npm -v
12.2.2
$ npx --version
12.2.2
```

注意看两个很实用的信号：
- `npm -v` 和 `npx --version` 返回的都是 `12.2.2`——因为 `npx` 就是跟着 `npm` 一起打包安装的，只要 `node` 和 `npm` 装好了，`npx` 自然就有。
- 如果你在自己电脑上敲 `node -v` 时返回 `command not found: node`（Mac）或「无法将 `node` 项识别为 cmdlet」（Windows PowerShell），那就说明电脑里还没装 Node.js——到 1.4 课照着链接下安装包即可。

再看一条 1.4 课你马上会亲眼见到的真实 `npx` 输出（在 Node `v22.23.5` 下实测运行 `npx @deepseek-ai/dsh@0.2.2-rc.5 --version`）：

```text
npm warn EBADENGINE Unsupported engine {
npm warn EBADENGINE   package: '@deepseek-ai/dsh@0.2.2-rc.5',
npm warn EBADENGINE   required: { node: '>=24.9.0' },
npm warn EBADENGINE   current: { node: 'v22.23.5', npm: '12.2.2' }
npm warn EBADENGINE }
npm notice run npx
npm notice run 'dsh' --version
0.2.2-rc.5
```

你看，前 6 行密密麻麻的英文只是 `npm warn`（提醒你官方推荐 `node >= 24.9.0`，当前是 `v22.23.5`），最后一行照样稳稳吐出了 `0.2.2-rc.5`。懂了 `warn` 和 `Error` 的区别，以后看到满屏英文就不会心慌。

---

## 5. 你来读：把这 6 行终端记录翻译成白话

假设你在 AI 的「轨迹」或同事发来的排查截图里看到下面 6 行命令，停下来想 10 秒：每行在干什么？哪两行需要联网？哪一行真正在算表格？

```bash
pwd
cd ~/青禾文具
ls -a
pip install openpyxl
python3 merge_sales.py
npx @deepseek-ai/dsh@0.2.2-rc.5 web
```

**参考判断**：
1. `pwd`：查看当前站在哪个文件夹（本地只读）。
2. `cd ~/青禾文具`：切换到当前用户主目录下的 `青禾文具` 文件夹（本地导航）。
3. `ls -a`：列出 `青禾文具` 里的所有文件，包括以 `.` 开头的隐藏文件（本地只读）。
4. `pip install openpyxl`：**需要联网**，通过 Python 的应用商店安装 `openpyxl`（用来读写 `.xlsx` Excel 表格的扩展包）。
5. `python3 merge_sales.py`：**真正在算表格的一行**，用 Python 运行工作区里的 `merge_sales.py` 脚本。
6. `npx @deepseek-ai/dsh@0.2.2-rc.5 web`：**首次需要联网下载缓存**，通过 `npx` 直接拉起 DeepSeek Harness `0.2.2-rc.5` 的网页版界面。

---

## 6. 小检查（3 道判断题）

1. 在终端里敲 `clear`（或 Windows 的 `cls`），会把当前文件夹里刚生成的文件全部清掉。（对 / 错）
2. `pip` 是 Python 的包管理器（用来装 `openpyxl` 这类工具包），而 `npm` / `npx` 属于 Node.js 阵营（用来装包或直接运行像 DeepSeek Harness 这样的工具）。（对 / 错）
3. 敲完 `cd sales` 回车后，屏幕上没有弹出新窗口也没有打印任何提示，说明这条命令一定执行失败了。（对 / 错）

---

## 7. 下一课

常用命令全认识了，但在真正放 AI 进你的电脑前，还有最后一道必须先学会的防身课——下一课 **1.3《危险命令识别表》**，我们把 8 类绝不能随手点「允许」的高危命令列成速查表，练熟「4 秒核查法」，再正式去 1.4 课装工具。

---

## 小检查答案

1. **错**。`clear` 只清除终端窗口里的历史文字显示，不会删除硬盘上的任何文件。
2. **对**。记住两对兄弟：`python` 配 `pip`，`node` 配 `npm` / `npx`。
3. **错**。`cd` 切换目录成功后默认静默不输出文字，只更新提示符里的当前路径；敲一条 `pwd` 就能确认已经切进去了。

---

## 参考与事实边界

- **实际操作结果**：第 4 节全部命令输出（`pwd`、`cd`、`ls`、`python3 --version`、`pip --version`、`node -v`、`npm -v`、`npx --version` 以及 `npx @deepseek-ai/dsh@0.2.2-rc.5 --version` 的真实 `npm warn EBADENGINE` 提示）均于 2026-11-24 在本地演示环境实测获得。
- **官方资料**：DeepSeek Harness 通过 `npx @deepseek-ai/dsh web` 启动的说明见官方 [README.zh.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/README.zh.md)。
