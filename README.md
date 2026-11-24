# 给 AI 当监工

**白领和老板的零基础代码常识课**

现在的 AI 编程工具已经能替你读文件、改代码、跑命令。问题是：它请求你批准一条命令的时候，你看得懂吗？它说"已完成"的时候，你知道它改了什么吗？

这门课不教你自己写代码，只教你看懂 AI 在干什么、判断它做得对不对：

- 看懂 AI 要执行的命令，知道哪些该批、哪些该拒；
- 看懂 AI 写的 Python，能指出"这里不对"；
- 看懂 AI 改了哪几行（diff），出错时能一键回退；
- 看懂 GitHub 上每个页面是干什么的，能判断一个开源项目靠不靠谱；
- 用 AI 解决自己工作里一个真实的重复劳动。

> [!NOTE]
> 本仓库目前处于写作阶段（私有）。开更后会转为公开，作为课程配套仓库。

## 课程结构

| 模块 | 内容 | 课数 |
|---|---|---|
| M0 | 开篇：AI 到底在你电脑上干了什么 | 2 |
| M1 | 电脑基本功与安装 | 5 |
| M2 | 读懂 Python | 8 |
| M3 | 一个项目长什么样 | 4 |
| M4 | Git 与 GitHub | 7 |
| M5 | 和 AI 高效协作 | 3 |
| M6 | 毕业项目 | 1 |
| M7 | 换个工具也会用：迁移到 Codex | 2 |
| 附录 | 国产备选：豆包工作、TRAE | 2 |

完整清单见 [docs/syllabus.md](docs/syllabus.md)。

## 演示环境

- 主线工具：[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（网页版，版本 `0.2.2-rc.5`）
- 演示模型：Gemini（国内学员可改用 DeepSeek 官方 API Key，见第 1.4 课）
- 贯穿项目：`ai-radar`（AI 模型比价与每日情报雷达），练习数据为真实公开接口快照（OpenRouter 模型目录 + Hacker News 首页讨论），见 [practice/](practice/)

## 仓库结构

```text
course/      每课一个文件夹：图文稿 lesson.md、录播参考脚本 video-script.md、速查卡 card.md、截图 images/
practice/    贯穿项目 ai-radar 的公开数据快照、抓取脚本与参考代码（如 build_top10.py）
docs/        课程大纲、写作规范、决策记录
```

## 授权

- 课程文字与图片：[CC BY-NC-SA 4.0](LICENSE)（可转载、需署名、不可商用、相同方式共享）
- 示例代码（`practice/` 下的代码文件）：[MIT](LICENSE-CODE)
