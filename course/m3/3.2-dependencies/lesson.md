# 3.2 "在我电脑上能跑"：依赖与环境

> 学习目标：理解 `requirements.txt`（依赖清单）和 `.venv`（虚拟环境）的作用，会用 Python 内置 `venv` 在 Mac / Windows 上按清单一键装齐依赖，并在浏览开源仓库时认出常见依赖文件。
>
> 演示环境：Python `3.12.16`（Mac / Linux 终端与 Windows PowerShell 双系统对照），实测安装仓库 `practice/requirements.txt` 并运行 `practice/scripts/daily_briefing.py`。

---

## 1. 「明明在我电脑上好好的，怎么到你那儿就报错？」

3.1 课我们把 `ai-radar` 的目录整理得干干净净，你把项目打包发给同事，或者自己换了台新电脑打开终端运行 `python3 practice/scripts/daily_briefing.py`，结果一秒跳出红错：

```text
ModuleNotFoundError: No module named 'yaml'
```

就算同事照着报错装完 `PyYAML`，下个月你在电脑上做另一个老项目，老项目要求 `openpyxl` 旧版本，新项目要求 `openpyxl` 新版本——全电脑共用一套 Python 环境，装了这个、崩了那个，这就是程序员口中最经典的魔咒：**「在我电脑上能跑（Works on my machine）」**。

解决这个魔咒，靠的不是记性，而是两件固定搭档：**依赖清单（`requirements.txt`）** 和 **虚拟环境（`.venv`）**。

---

## 2. 系统位置：先搭独立房间，再按采购单进货

把电脑想成一栋办公楼：不建虚拟环境时，所有项目把工具全堆在大厅地板上，谁升级工具都会绊倒别人；建了 `.venv` 之后，每个项目各占一间独立工具间，互不打架。

```
拿到一个新项目（ai-radar/）
      ↓
第 1 步：python3 -m venv .venv               → 给这个项目建一间独立工具间（.venv/）   ← 【本课位置】
      ↓
第 2 步：激活 .venv                           → 走进这间工具间（提示符前出现 (.venv)）
      ↓
第 3 步：pip install -r requirements.txt     → 按采购单把需要的库全装进这间屋里
      ↓
第 4 步：python3 scripts/daily_briefing.py   → 稳稳跑通，换任何电脑 100% 复现！
```

---

## 3. 讲清楚：`requirements.txt`、`.venv` 与双系统实操

### 3.1 `requirements.txt`：项目的「工具采购清单」

打开配套仓库里的 `practice/requirements.txt`，总共就 4 行纯文本：

```text
# ai-radar 第三方 Python 依赖清单
# 安装方式：python3 -m pip install -r practice/requirements.txt
openpyxl>=3.1.5,<4.0
PyYAML>=6.0.2,<7.0
```

看懂里面的版本号符号（监工扫一眼就能明白）：
- `openpyxl>=3.1.5,<4.0`：意思是「装 `3.1.5` 及以上、但不到 `4.0` 的大版本」——既能拿到安全小修复，又防止大版本升级把旧写法改崩；
- 有时候你也会看到双等号 `openpyxl==3.1.5`，表示「死锁在 `3.1.5` 这一版，一个小数点都不许变」，常见于对稳定性要求极高的线上项目。

以前你得一个一个敲 `pip install openpyxl`、`pip install pyyaml`；有了这张清单，只要加一个 **`-r`**（requirement 的缩写）参数：`python3 -m pip install -r requirements.txt`，`pip` 就会一口气按清单全部装齐。

### 3.2 虚拟环境（`.venv`）：每个项目的独立工具间

Python 3 自带了 `venv` 模块，**不用额外装任何软件**，直接在项目根目录就能建一个叫 `.venv` 的隐藏文件夹。

下面是 **Mac / Linux** 和 **Windows（PowerShell）** 的完整三步对照：

| 步骤 | Mac / Linux 终端 | Windows（PowerShell） | 成功信号 |
|---|---|---|---|
| **1. 建虚拟环境**（首次做一次） | `python3 -m venv .venv` | `python -m venv .venv` | 根目录多出一个 `.venv` 隐藏文件夹 |
| **2. 激活环境**（每次重开终端做一次） | `source .venv/bin/activate` | `.\.venv\Scripts\Activate.ps1` | 终端行首出现 **`(.venv)`** 字样 |
| **3. 按清单装依赖** | `python3 -m pip install -r practice/requirements.txt` | `python -m pip install -r practice/requirements.txt` | 看到 `Successfully installed ...` |
| **退出环境**（干完活可选） | `deactivate` | `deactivate` | 行首 `(.venv)` 消失 |

> **Windows 常见卡点提示**：第一次在 PowerShell 敲 `.\.venv\Scripts\Activate.ps1` 时，部分电脑会弹红字提示「禁止运行脚本（ExecutionPolicy）」。先运行一次 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 放行本地脚本权限，再激活即可；或者更省事——**不用激活，直接用完整路径调用虚拟环境里的 Python**：`.\.venv\Scripts\python.exe practice/scripts/daily_briefing.py`（Mac 对应 `./.venv/bin/python`）。

**最常见的误解**：觉得「既然 `.venv` 里装好了所有库，我把 `.venv` 一起传到 GitHub 或发给同事，对方不就省得装了吗？」**绝对不行！**
1. `.venv` 动辄几十 MB 到几百 MB（我们实测只装 `openpyxl` 和 `PyYAML` 两个轻量包，`.venv` 就已经占了 **`20 MB`**；一旦装进 `pandas`、`matplotlib`，轻松飙到 300 MB 以上）；
2. `.venv` 里的程序绑定了你这台电脑的操作系统和路径，Mac 上建的 `.venv` 拷到 Windows 根本跑不动！

正确交接姿势永远只有一条：**把 `.venv/` 写进 `.gitignore` 绝不上传；只提交 100 字节的 `requirements.txt`**，对方拿到后 5 秒就能在自己电脑上还原出一模一样的环境。

### 3.3 逛 GitHub 顺手认全：其他常见依赖清单「一眼认出表」

以后你在 GitHub 上下载别人的开源项目，根目录不一定叫 `requirements.txt`，看到下面这几个名字，知道它们都是同一回事就行：

| 文件名 | 常见于哪种项目 | 它是干嘛的 | 你怎么应对 |
|---|---|---|---|
| `requirements.txt` | 传统 Python 项目 / 数据脚本 | Python 第三方库清单 | `python3 -m pip install -r requirements.txt` |
| `pyproject.toml` | 现代 Python 项目（2026 年主流） | 整合了项目信息、依赖清单和工具配置的新标准 | 按项目 `README` 提示安装，或让 AI 照着装 |
| `uv.lock` | 使用 `uv` 加速工具的 Python 项目 | 精确锁死每个依赖版本号的锁文件 | 知道它和 `requirements.txt` 同类即可，暂不用急着学 `uv` |
| `package.json` / `package-lock.json` | Node.js / 前端项目（如 DeepSeek Harness） | JS/TS 世界的依赖清单与锁文件 | 对应 1.2 课见过的 `npm install` |

---

## 4. 现场看：从零建一个全新 `.venv`，实测装包并跑通早报

在本机新建一个完全空白的虚拟环境，按 `practice/requirements.txt` 安装依赖后，运行 `pip list` 和目录体积检查，实测输出如下：

```text
Package    Version
---------- -------
et_xmlfile 2.0.0
openpyxl   3.1.5
pip        25.0.1
PyYAML     6.0.4

20M    .venv
```

注意看两个真实细节：
1. `requirements.txt` 里只写了 2 行（`openpyxl` 和 `PyYAML`），但 `pip` 自动替我们顺手装上了 `openpyxl` 需要的底层小依赖 `et_xmlfile 2.0.0`——这就是包管理器的省心之处；
2. 哪怕只装 2 个包，整个 `.venv` 体积就已经达到 `20M`，再次印证它绝不该提交进 Git。

紧接着用这个全新环境直接运行 `python3 practice/scripts/daily_briefing.py`，终端立刻干脆吐出结果：

```text
已按 config.yaml 生成简报：output/daily-briefing.md（模型 5 条，HN 热点 5 条）
```

零报错、一次过，换到同事的 Mac 或 Windows 上走完同样三行命令，结果分毫不差。

---

## 5. 你来读：AI 准备提交代码前，你在改动列表里拦住哪两样？

你在 `ai-radar` 里让 AI 加了一个新图表功能，装上了 `matplotlib`，然后准备把项目同步给同事。提交前你扫了一眼待上传文件列表：

```text
M  practice/scripts/daily_briefing.py
A  practice/.venv/lib/python3.12/site-packages/matplotlib/... （共 1,842 个文件）
M  practice/README.md
```

停下来想 10 秒：
1. 这份待提交清单里，有一个**绝不能传上去的庞然大物**，是什么？
2. 同时还**漏改了一个关键文件**——如果现在直接发给同事，对方一运行立刻报 `ModuleNotFoundError: No module named 'matplotlib'`，漏改了哪个文件？

**判断思路**：
1. **立刻拦下 `.venv/` 里的 1,842 个文件**：把 `.venv/` 确认写进 `.gitignore`，绝不上传虚拟环境目录。
2. **漏更新了 `practice/requirements.txt`**：AI 刚给你的本地环境装了 `matplotlib`，却忘了把 `matplotlib` 写进 `requirements.txt`！告诉 AI：「把新增的 `matplotlib` 补进 `requirements.txt`，并确认 `.venv/` 已被 `.gitignore` 忽略。」

---

## 6. 小检查（3 道判断题）

1. 为了方便同事省去安装步骤，应该把本机建好的 `.venv/` 文件夹直接上传到 GitHub 仓库。（对 / 错）
2. 看到终端提示符最前面出现 `(.venv)`，说明当前终端已经进入这个项目专属的虚拟环境，此时运行 `pip install` 装的包不会污染电脑里其他项目。（对 / 错）
3. 在 GitHub 上逛到别的 Python 项目时，如果根目录没有 `requirements.txt`，而是放着 `pyproject.toml`，它同样承载着项目的依赖配置信息。（对 / 错）

---

## 7. 下一课

目录架好了，虚拟环境和依赖清单也打通了。刚才我们实测跑 `daily_briefing.py` 时，终端里冒出了一句「已按 `config.yaml` 生成简报：`output/daily-briefing.md`」——里面一下子串起了 `.json`、`.yaml`、`.md` 三种文件。下一课 **3.3《Markdown / JSON / YAML 三件套》**，教你彻底分清这三种格式，并且不碰一行 Python 代码，直接改 `config.yaml` 控制程序行为。

---

## 小检查答案

1. **错**。`.venv/` 体积庞大且绑定本机操作系统路径，必须列入 `.gitignore`；协作时只提交轻量的 `requirements.txt`，对方按清单重建即可。
2. **对**。激活 `.venv` 后，装包和运行脚本都会隔离在当前项目的独立环境里。
3. **对**。`pyproject.toml` 是现代 Python 项目的标准配置与依赖清单文件，认出它就不会在开源仓库里发懵。

---

## 参考与事实边界

- **实际操作结果**：本课 `pip list` 输出（`et_xmlfile 2.0.0`、`openpyxl 3.1.5`、`PyYAML 6.0.4`）、`.venv` 体积（`20M`）以及 `daily_briefing.py` 运行结果，均在 `Python 3.12.16` 空白 `venv` 中实测安装 `practice/requirements.txt` 获得。
- **官方资料**：
  - Python 官方虚拟环境文档：[venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)；
  - `requirements.txt` 与依赖规范：[Requirements File Format — pip documentation](https://pip.pypa.io/en/stable/reference/requirements-file-format/)。
- **作者说明**：第 5 节的提交清单为提炼自高频 Git 提交失误的监工检查练习。
