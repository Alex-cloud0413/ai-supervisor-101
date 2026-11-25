# 4.1 Git = 游戏存档

> 学习目标：理解 Git 的 5 个核心动作（`init`、`status`、`add`、`commit`、`log`）和两种安全读档方式（`git restore` 撤销未存档改动、`git revert` 撤销已存档提交），学会在让 AI 改代码前先打存档、改坏后 3 秒安全回退。
>
> 演示环境：Git `2.56.1`（Mac 终端与 Windows PowerShell 命令完全一致），在 `ai-radar` 项目骨架（`practice/` 复制出的独立沙盒）上实测完整存档与回退流程。

---

## 1. 让 AI 改完第三版，突然想退回一小时前那一版怎么办？

没有版本控制工具之前，职场人保护文件全靠手动复制改名：

```text
daily_briefing.py
daily_briefing_v2.py
daily_briefing_v2_AI改坏前.py
daily_briefing_终版_别删.py
```

这种土办法碰上 AI 编程工具立刻失效——AI 往往一轮对话就同时改 3 个文件，改到一半你发现新思路跑偏了，根本记不清刚才它动过哪些行，手动 `Ctrl + Z` 早就撤不回去了。

打单机游戏遇到大 Boss 之前，老玩家都会先点一下「**保存进度**」：打输了直接「**读取存档**」，装备和血量一秒回到开打前的状态。在代码世界里，这个装在你自己电脑上的「游戏存档机」就叫 **Git**（读作「吉特」）。

从这一课进入 **M4 Git 与 GitHub**。前 3 课（4.1–4.3）先吃透装在本地电脑上的 **Git 存档机**，后 4 课（4.4–4.7）再把存档推到云端平台 **GitHub**。

---

## 2. 系统位置：Git 守在「AI 改文件」的前后两道关口

每次让 AI 动手改项目之前先存一档、改完验收通过再存一档，你就永远拥有「随时反悔」的底气：

```
你交代新任务前：先看 git status（确认当前干净）                     ← 【本课位置】
      ↓
AI 修改文件（比如改了 config.yaml 和 daily_briefing.py）
      ↓
验收环节（4.2 课用 git diff 看具体改了哪几行）
      ├── 改坏了 / 方向错了 ──→ git restore <文件>（3 秒读档，未存档改动瞬间还原）
      └── 改对了且跑通了    ──→ git add . → git commit -m "说明"（打一个新存档！）
                                     ↓（万一明天才发现这档有问题）
                                git revert HEAD（安全反悔，用新存档抵消旧改动）
```

一句话记死 **Git 和 GitHub 的区别**：**Git 是装在你电脑本地的存档软件，断网也能用；GitHub 是存 Git 存档的云端网站（4.4 课专门讲）。**

---

## 3. 讲清楚：Git 存档的 5 个常用命令 + 2 种安全回退

### 3.1 先确认电脑装好 Git 了没

在 Mac 终端或 Windows PowerShell 里敲一行：

```bash
git --version
```

如果返回类似 `git version 2.56.1` 的版本号，说明已经装好可以直接用。如果提示找不到命令：
- **Mac**：首次敲 `git --version` 时系统会自动弹窗提示安装「命令行开发者工具（Xcode Command Line Tools）」，点「安装」等几分钟即可；
- **Windows**：去官网 [git-scm.com](https://git-scm.com/) 下载「Git for Windows」，一路点「Next」装完，重启 PowerShell 再敲 `git --version` 即可。

### 3.2 把「打存档」拆成你一眼就懂的 5 个命令

第一次把 Git 放进一个普通项目文件夹时，记住这 5 个高频命令就够应付 90% 的日常监工场景：

| 命令 | 游戏存档类比 | 它是干嘛的 | 输入 / 输出是什么 |
|---|---|---|---|
| `git init -b main` | 买一台存档机放进当前文件夹 | 在当前目录建一个隐藏的 `.git/` 存档柜，主线叫 `main`（每个项目只做一次） | 输入：无；输出：提示 `Initialized empty Git repository` |
| `git status`（或 `git status -s`） | 查看当前桌面乱不乱 | 报告哪些文件改过、哪些是新文件、哪些准备存进下一档 | 输出简写：`??` 未跟踪新文件、`M` 已修改、`A` 已暂存 |
| `git add <文件>`（或 `git add .`） | 把要存的文件放进「待打包箱」 | 挑出本次打算打进存档的文件（叫「暂存区 / Staging Area」） | `git add .` 代表当前目录所有非忽略改动；被 `.gitignore` 拦住的 `.env`、`.venv/`、`output/` 会自动跳过 |
| `git commit -m "一句话说明"` | 正式按下「保存进度」并贴标签 | 把待打包箱里的状态永久刻成一个带编号（Commit ID）的历史快照 | 输出：7 位短编号（如 `4c5b030`）和改动行数统计 |
| `git log --oneline` | 打开「历史存档列表」 | 一行一条列出从新到旧的全部存档编号和说明 | 方便你随时回头翻看每次改了什么 |

**为什么 `add` 和 `commit` 要拆成两步？** 因为 AI 有时候一轮会改 3 个文件，但你只想先把验收通过的那 1 个文件存进这一档，剩下 2 个还在调试——先 `git add` 挑进箱子、确认无误再 `git commit` 封箱，就像寄快递前先挑货装箱再封口贴单。

### 3.3 AI 改坏了怎么回退？认准两招安全读档 + 一条红线

回退前先问自己一句话：**「这笔改坏的东西，我刚才按下 `git commit` 存档了吗？」**

| 场景 | 安全命令 | 实际效果 | 会丢历史记录吗？ |
|---|---|---|---|
| **场景 A：还没 `commit`**（AI 刚改坏 `config.yaml`，验收没通过） | `git restore config.yaml` | 把 `config.yaml` 一键恢复成上一次存档时的原样 | 只丢掉刚才那笔改坏的草稿，历史存档毫发无损 |
| **场景 B：已经 `commit` 了**（昨天存了一档，今天发现逻辑错了） | `git revert HEAD` | 新建一个「反向抵消存档」，把 `HEAD`（最近一档）的改动原样退回去 | **不删任何历史**，整个反悔过程留痕可查，团队协作最安全 |
| **高危红线：千万别乱敲 `git reset --hard`** | （1.3 课红灯命令） | 暴力抹掉未提交改动，甚至直接把历史指针往回硬掰 | **未存档改动直接永久蒸发，极难找回！** |

**最常见的误解**：以为「用了 Git 就等于文件会自动实时备份，改坏随时能恢复」。**不对！** Git 只保护你**已经 `git commit` 存过档**的内容。如果上午写了两小时代码一直没打存档，中午让 AI 一把覆盖坏了，Git 里只存着早上的状态。**监工铁律：每让 AI 做一次大改动前，先确认 `git status` 干净或先打一档！**

---

## 4. 现场看：给 `ai-radar` 打第一档，再亲手演练「改坏 → 读档」

我们把 `practice/`（连同根目录的 `.gitignore`）复制到一个干净的 `ai-radar` 测试目录里，按真实监工节奏跑一遍完整流程。

### 第 1 步：初始化存档柜，打下第一笔基线存档

```bash
git init -b main
git status -s
```

终端实测输出：

```text
Initialized empty Git repository in .../ai-radar/.git/
?? .env.example
?? .gitignore
?? README.md
?? config.yaml
?? data/
?? requirements.txt
?? scripts/
```

注意看：`??` 表示这些文件还没纳入 Git 存档。接下来打包存进第一档：

```bash
git add .
git commit -m "init: 初始化 ai-radar 项目骨架与公开快照"
```

终端实测输出：

```text
[main (root-commit) 4c5b030] init: 初始化 ai-radar 项目骨架与公开快照
 10 files changed, 55529 insertions(+)
 create mode 100644 .env.example
 create mode 100644 .gitignore
 create mode 100644 README.md
 create mode 100644 config.yaml
 create mode 100644 data/hn-frontpage-2026-11-24.json
 create mode 100644 data/openrouter-models-2026-11-24.json
 create mode 100644 requirements.txt
 create mode 100644 scripts/build_top10.py
 create mode 100644 scripts/daily_briefing.py
 create mode 100644 scripts/fetch_snapshots.py
```

看到 `4c5b030` 这串 7 位短编号，第一笔「初始安全存档」就永久刻进 `.git/` 了。如果此时目录里存在本地 `.env` 或 `output/`，因为有 `.gitignore` 守门，它们压根不会出现在这 10 个文件里。

### 第 2 步：模拟 AI 改乱 `config.yaml`，用 `git restore` 3 秒读档

假设 AI 帮你把 `config.yaml` 里的 `top_n` 和 `min_points` 改乱了，敲 `git status -s` 立刻看到红色标记：

```text
 M config.yaml
```

验收不满意？直接敲一行：

```bash
git restore config.yaml
git status -s
```

`git status -s` 瞬间变为空白——`config.yaml` 一字不差地退回了 `4c5b030` 那一档的原样。

### 第 3 步：如果已经存进去了才发现错？用 `git revert` 安全反悔

假如刚才不小心把「HN 热度门槛改成 500 分」存成了新存档 `2080ca7`，后来反悔想改回 `50` 分：

```bash
git revert HEAD --no-edit
git log --oneline
```

终端实测输出：

```text
5a26693 Revert "feat: 将 HN 热点门槛提高到 500 分"
2080ca7 feat: 将 HN 热点门槛提高到 500 分
4c5b030 init: 初始化 ai-radar 项目骨架与公开快照
```

看懂这个优雅结果：历史记录里没有强行擦除 `2080ca7`，而是在顶部多了一笔 `5a26693`，把 `config.yaml` 稳稳退回了修改前的 `50` 分。哪天想复盘「当初为什么试过 500 分又改回来了」，记录清清楚楚。

---

## 5. 你来读：遇到这 3 种现场状况，你该敲哪条命令？

下面是监工在终端里最常遇到的 3 个瞬间，先停 10 秒选出你的动作，再核对判断思路：

1. 你准备让 AI 给 `daily_briefing.py` 增加一个新功能，动手前你想先看一眼当前文件夹里有没有还没存档的零散修改。
2. AI 刚把 `scripts/daily_briefing.py` 改坏跑报错了，这笔改动**还没有**执行 `git commit`，你想立刻把它还原回刚才正常运行的样子。
3. 昨天你把一笔改坏了汇率口径的提交（`commit`）推给了团队，今天早上需要撤回它，AI 随口建议你跑 `git reset --hard HEAD~1`，你该批还是该拒？

**判断思路**：
1. **敲 `git status`（或 `git status -s`）**：如果输出为空，说明工作区干净可以开工；如果列出了一堆 `M` 或 `??`，先决定把它们 `commit` 存档还是清理掉，别把新旧改动搅成一锅粥。
2. **敲 `git restore scripts/daily_briefing.py`**：未提交的单文件改坏，用 `git restore` 是最精准、最安全的读档方式。
3. **坚决拒绝 `git reset --hard`，改用 `git revert HEAD`！** 第一，`reset --hard` 属于 1.3 课的红灯高危命令，会直接清掉本地未存修改并改写提交历史；第二，已经分享出去的历史只能用 `git revert` 追加一笔反向抵消提交来安全撤回。

---

## 6. 小检查（3 道判断题）

1. 只要在一个文件夹里执行过 `git init`，以后每次修改文件 Git 都会自动帮你保存每一个历史版本，不需要手动执行 `git add` 和 `git commit`。（对 / 错）
2. AI 刚把 `config.yaml` 改错了且尚未提交存档，运行 `git restore config.yaml` 可以把它安全恢复成最近一次提交时的内容。（对 / 错）
3. `git revert` 通过新增一条反向抵消的提交来撤销历史改动，不破坏原有提交记录，比 `git reset --hard` 更安全。（对 / 错）

---

## 7. 下一课

学会了打存档和读档，下一个紧迫问题是：每次 AI 说「改好了，请验收」，在按下 `git commit` 放行之前，你总不能把几百行代码从头到尾重读一遍。下一课 **4.2《读懂 diff》**，教你用 `git diff` 盯紧红删绿增的那几行变化，15 秒揪出 AI 偷偷改歪的小动作。

---

## 小检查答案

1. **错**。Git 不会自动实时存档，只有你明确执行 `git add` 和 `git commit` 后，当前状态才会被永久记录成一条历史快照。
2. **对**。`git restore <文件>` 专门用来丢弃未提交的本地修改、把文件还原到上一次存档状态。
3. **对**。`git revert` 留痕不删史，是撤销已提交改动的首选安全做法。

---

## 参考与事实边界

- **实际操作结果**：本课全部命令与输出（`git init -b main`、`git status -s`、`git commit` 编号 `4c5b030`、`git restore`、`git revert HEAD --no-edit` 编号 `5a26693`）均在 `Git 2.56.1` 环境下，使用配套仓库 `practice/` 的独立沙盒副本实测获得。
- **官方资料**：
  - Git 官方基础教程：[Pro Git — Git Basics](https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%85%B3%E4%BA%8E%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6)；
  - `git restore` 官方手册：[git-restore Documentation](https://git-scm.com/docs/git-restore)；
  - `git revert` 官方手册：[git-revert Documentation](https://git-scm.com/docs/git-revert)。
- **作者说明**：本课用「游戏存档机」类比 Git 工作流以便零基础理解；企业多人协作中若涉及强制推送（`git push --force`）或历史改写，同样属于高危红线操作，请遵循 1.3 课拦截原则。
