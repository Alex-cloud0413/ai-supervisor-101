# 4.3 分支与合并

> 学习目标：理解 `branch`（平行试错存档槽）与 `merge`（合并回主线）的作用，学会让 AI 在独立实验分支上做大改动、验收通过再合回 `main`，并能看懂合并冲突标记（`<<<<<<<` / `=======` / `>>>>>>>`）及用 `git merge --abort` 安全退出。
>
> 演示环境：Git `2.56.1`（Mac 终端与 Windows PowerShell 命令完全一致），在 `ai-radar` 沙盒上实测建分支、快进合并与真实合并冲突演练。

---

## 1. 想让 AI 试一个「大改版」，又怕把原本好用的主版本搅乱？

现在你的 `ai-radar` 在 `main` 上跑得稳稳当当，每天都能正常吐出早报。突然有一天你想做一个大实验：「让 AI 试着把早报改成更严苛的 500 分精选版，再顺便重构一下排版。」

问题来了：这种大改版可能要来回折腾五六轮，万一折腾到一半老板急着要一份按旧口径跑出来的早报，或者试到最后觉得新版还不如旧版好用——如果在原来的 `main` 上直接改，主版本早就被改得面目全非了。

游戏老玩家遇到这种分叉剧情，都会干一件事：**「另存到 2 号存档槽」**。主线存档（1 号槽 `main`）原封不动留着随时能用；2 号槽（实验分支 `feat/strict-hn`）放手让 AI 折腾，试成了合回主线，试崩了切回 1 号槽拍拍屁股走人。这套「平行存档槽」机制，就叫 **分支（Branch）与合并（Merge）**。

---

## 2. 系统位置：给 AI 开一条「隔离试错跑道」，验收通过再并入主干道

```
main（稳定主线，随时可运行）
  ● 4c5b030 初始化骨架 ───────────────────────────● 合并点（验收通过后合回 main！）
              \                                 /
               \ git switch -c feat/strict-hn  / git merge feat/strict-hn  ← 【本课位置】
                ↘                             ↗
  feat/strict-hn（实验分支：AI 放手折腾，改崩了随时删掉，绝不污染 main！）
                  ● 2080ca7 调整 HN 门槛与版式
```

一句话分工记死：
- **`main` 分支**：你的「正式可用版」，只放验收通过、能稳稳跑通的代码；
- **实验分支（常以 `feat/`、`fix/`、`exp/`、`agent/` 开头）**：给 AI 施展拳脚的独立沙盒——就算 AI 在分支里连改 10 个文件全改坏了，只要切回 `main`，你的正式版连一个标点都没动过！

---

## 3. 讲清楚：分支与合并的 5 个常用命令 + 合并冲突怎么破

### 3.1 日常只需记住的 5 条分支命令

| 命令 | 游戏存档类比 | 它是干嘛的 | 监工注意什么 |
|---|---|---|---|
| `git branch` | 查看现在开了几个存档槽 | 列出本地全部分支，名字前面带 `*` 星号的就是你当前所在的分支 | 让 AI 大改前扫一眼：千万别直接在 `* main` 上裸改 |
| `git switch -c feat/strict-hn` | 复制当前进度到新开的 2 号槽并切进去 | **新建并立刻切换**到名为 `feat/strict-hn` 的新分支 | 老教程和部分 AI 会写 `git checkout -b feat/strict-hn`，效果完全一样，认得就行 |
| `git switch main` | 切回 1 号稳定主线槽 | 从实验分支切回 `main` | 切分支前建议先 `git status` 确认当前分支改动已提交或还原 |
| `git merge feat/strict-hn` | 把 2 号槽的成果合并进 1 号主线 | **先切回 `main`**，再运行此命令把实验分支的提交并入 `main` | 合并前先用 `git diff main..feat/strict-hn` 复核一遍总差异 |
| `git branch -d feat/strict-hn` | 删除已合并完的空临时槽 | 合并成功后清理掉用完的实验分支，保持列表清爽 | 小写 `-d` 很安全（只删已合并分支）；大写 `-D` 会强制删除未合并分支，只有确认「这次实验彻底不要了」才批准 |

> **给分支起名的实用习惯**：不用纠结复杂规则，用英文小写加斜杠就能一眼认出用途——加新功能叫 `feat/xxx`（feature），修问题叫 `fix/xxx`，纯做实验叫 `exp/xxx`。4.7 课你还会看到 OpenAI 官方仓库里 AI Agent 自己开的分支 `agent/fix-install-compact-release-json`，用的正是这套命名规矩。

### 3.2 撞上「合并冲突（Merge Conflict）」别慌：看懂 3 条分隔线 + 一键逃生命令

绝大多数时候，`git merge` 会全自动安静完成。只有在**同一个文件的同一行，在 `main` 和实验分支上被同时改成了两个不同值**时，Git 不敢替你瞎猜留哪个，就会停下来报 **`CONFLICT (content): Merge conflict in config.yaml`**。

此时打开冲突文件，你会看到 Git 插入的 3 条醒目标记线：

```text
<<<<<<< HEAD
  exchange_rate: 7.25     ← 你当前所在分支（main）上的写法
=======
  exchange_rate: 7.3      ← 你正要合并进来的分支（exp/rate-73）上的写法
>>>>>>> exp/rate-73
```

处理冲突只有两条路，**完全不用手抖**：
1. **想现在解决**：决定保留哪一行（比如保留 `7.25`），**把上面 3 条 `<<<<<<<` / `=======` / `>>>>>>>` 标记行和不要的那一行全部删干净**，保存文件，然后敲 `git add config.yaml` + `git commit` 即可完成合并；也可以直接把冲突提示发给 AI，明确告诉它「保留 `main` 的 `7.25`，清掉冲突标记」。
2. **一时拿不准，想先退回合并前**：立刻敲一行万能逃生命令——
   ```bash
   git merge --abort
   ```
   1 秒之内，一切干干净净退回合并前的状态，什么都没损失。

**最常见的误解**：以为「切一次分支会占双倍硬盘空间，或者把大文件全复制一份」。**其实不会！** Git 的分支本质上只是一个 41 字节的「书签指针」，建分支、切分支几乎零成本、瞬间完成，放心大胆地每做一次新实验就开一条新分支。

---

## 4. 现场看：在 `ai-radar` 里跑一遍「开分支 → 合并」与「真实冲突逃生」

### 场景 A：顺滑的「开分支试改 → 验收合回主线」

先给实验开一条独立分支 `feat/strict-hn`，把 `config.yaml` 的 `min_points` 从 `50` 改成 `500` 并存档：

```bash
git switch -c feat/strict-hn
# 修改 config.yaml 中的 min_points: 50 -> 500 并验收跑通后：
git add config.yaml
git commit -m "feat: 将 HN 热点门槛提高到 500 分"
git log --oneline --graph --all
```

终端实测输出：

```text
Switched to a new branch 'feat/strict-hn'
[feat/strict-hn 2080ca7] feat: 将 HN 热点门槛提高到 500 分
 1 file changed, 1 insertion(+), 1 deletion(-)
* 2080ca7 feat: 将 HN 热点门槛提高到 500 分
* 4c5b030 init: 初始化 ai-radar 项目骨架与公开快照
```

验收满意，切回 `main` 一键合入：

```bash
git switch main
git merge feat/strict-hn
```

终端实测输出：

```text
Switched to branch 'main'
Updating 4c5b030..2080ca7
Fast-forward
 config.yaml | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

看到 `Fast-forward`（快进合并），说明期间 `main` 没被别人改过，Git 直接把 `main` 的指针顺滑推到了 `2080ca7`，零冲突、一秒收工。

### 场景 B：真实撞上冲突时的终端现场

假设我们开了分支 `exp/rate-73` 把汇率改成了 `7.3`，同时又切回 `main` 把同一行汇率微调成了 `7.25`。此时在 `main` 上执行 `git merge exp/rate-73`，终端立刻如实报警：

```text
Auto-merging config.yaml
CONFLICT (content): Merge conflict in config.yaml
Automatic merge failed; fix conflicts and then commit the result.
```

打开 `config.yaml` 第 9–18 行，清清楚楚摆着刚才讲过的 3 条冲突标记：

```yaml
model_pricing:
  snapshot_file: openrouter-models-2026-11-24.json
<<<<<<< HEAD
  exchange_rate: 7.25
=======
  exchange_rate: 7.3
>>>>>>> exp/rate-73
  top_n: 5
```

此时如果先不想动，敲 `git merge --abort` 立刻全身而退；如果决定采用 `7.25`，删掉冲突标记与 `7.3` 后 `git add config.yaml && git commit` 即可完成合并。

---

## 5. 你来读：AI 给你发来这 3 个操作提议，你该怎么拍板？

先停 10 秒看清每个场景，再核对参考判断：

1. 你让 AI 给 `ai-radar` 加一个「自动输出 HTML 网页简报」的大功能，AI 申请先执行 `git switch -c feat/html-report` 再动手写代码。你应该批准吗？
2. 合并实验分支时，终端跳出 `CONFLICT (content): Merge conflict in config.yaml`，你有点懵，担心把项目弄坏，想先恢复到合并前再慢慢看。应该敲哪条命令？
3. 你和 AI 一起解决了 `config.yaml` 里的合并冲突，但 AI 忘了删掉文件里的 `=======` 和 `>>>>>>> exp/rate-73` 这两行标记就直接运行 `python3 scripts/daily_briefing.py`。会发生什么？

**判断思路**：
1. **立刻批准，而且值得点赞！** 做跨文件或不确定成败的大功能前主动开独立分支，是保护稳定 `main` 主线的标准好习惯。
2. **敲 `git merge --abort`**：这是合并冲突时的万能撤销键，1 秒回到合并前干干净净的状态。
3. **`PyYAML` 解析 `config.yaml` 会直接报语法错！** 冲突标记（`<<<<<<<`、`=======`、`>>>>>>>`）只是 Git 写给人类看的临时提示，不是合法的 YAML 或 Python 语法，解决冲突时**必须连同这 3 行标记一起彻底删干净**。

---

## 6. 小检查（3 道判断题）

1. 在本地新建一条 Git 分支（如 `git switch -c feat/test`）会把整个项目文件夹里几十兆的数据全部复制一份，非常占硬盘空间。（对 / 错）
2. 想把实验分支 `feat/strict-hn` 的改动合回主线，正确顺序是先 `git switch main` 切回主线，再运行 `git merge feat/strict-hn`。（对 / 错）
3. 合并时遇到 `Merge conflict`，如果暂时拿不准该保留哪一版，可以运行 `git merge --abort` 安全退回合并前的状态。（对 / 错）

---

## 7. 下一课

到这里，装在你自己电脑里的 **本地 Git 三件套**——打存档与读档（4.1）、看 `diff` 验货（4.2）、开分支试错与合并（4.3）——已经全部打通。接下来我们把本地存档推上云端，进入 **4.4《从 0 认识 GitHub：注册与全平台板块导览》**，哪怕以前从没注册过 GitHub，也能一步步把整个平台摸得门儿清。

---

## 小检查答案

1. **错**。Git 分支本质只是一个轻量级指针，创建和切换几乎瞬间完成且几乎不额外占用硬盘空间。
2. **对**。合并的目标是把「别的分支」拉进「当前所在分支」，所以要先站在 `main` 上再执行 `git merge <实验分支名>`。
3. **对**。`git merge --abort` 会中止本次合并并把工作区还原到合并前的干净状态。

---

## 参考与事实边界

- **实际操作结果**：本课 `git switch -c feat/strict-hn`、`Fast-forward` 合并（`4c5b030..2080ca7`）、`config.yaml` 合并冲突标记（`7.25` vs `7.3`）以及 `git merge --abort` 均在 `Git 2.56.1` 下基于配套仓库 `practice/` 沙盒副本实测获得。
- **官方资料**：
  - Git 官方分支教程：[Pro Git — Git Branching](https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%AE%80%E4%BB%8B)；
  - `git switch` 与 `git merge` 手册：[git-switch](https://git-scm.com/docs/git-switch)、[git-merge](https://git-scm.com/docs/git-merge)。
- **作者说明**：部分 AI 编程工具或旧教程仍沿用 `git checkout -b <分支名>`，与 `git switch -c <分支名>` 等效，课中已作对照标注方便识别。
