# 3.3 录播参考脚本：Markdown / JSON / YAML 三件套

> 建议时长：8–10 分钟（边改 `practice/config.yaml` 边实测重跑 `daily_briefing.py` 看 `output/daily-briefing.md` 变化，以下为口播要点与屏幕节点，不作逐字稿）。

## 中英术语读法

| 术语 | 读法 | 首次出现时的口头解释 |
|---|---|---|
| Markdown（`.md`） | 马克当 | 带标题、表格、链接的轻量纯文本写作格式 |
| JSON（`.json`） | 杰森 | 花括号加双引号的机器交换数据格式 |
| YAML（`.yaml`） | 牙默 | 缩进清晰、能写注释的人类友好配置文件格式 |
| Trailing comma | 中文说「尾随逗号」 | JSON 最后一项末尾多打出来的逗号，一打就报错 |

---

## 0:00 – 0:45｜开场 Hook（不碰一行 Python 代码，直接改程序行为）

- **屏幕画面**：打开 `practice/config.yaml`，把鼠标停在 `min_points: 50` 和 `keywords:` 列表上，旁边切出生成的 `output/daily-briefing.md`。
- **口播要点**：
  - 「以后想换汇率、加关键词、调热度门槛，难道每次都要打开 Python 代码改吗？不用——专业项目会把参数抽到 `config.yaml` 里。今天把 AI 项目里最常见的三种纯文本格式一次串起来：JSON、YAML、Markdown。」

## 0:45 – 2:30｜一句话分工：输入（JSON）→ 控制（YAML）→ 输出（Markdown）

- **屏幕画面**：展示「`data/*.json` + `config.yaml` → `daily_briefing.py` → `output/daily-briefing.md`」流程图和三件套对比表。
- **口播要点**：
  - 交代清楚谁给谁看：JSON 给机器看，YAML 给人调参，Markdown 给人读文档和早报。

## 2:30 – 5:30｜3 个最容易踩的语法坑（现场演示真实报错）

- **屏幕画面**：
  1. 在临时命令行触发 YAML Tab 缩进报错（`found character '\t'`）和指明 `min_points: 50` 冒号后必须空一格；
  2. 触发 JSON 尾随逗号报错（`JSONDecodeError`）并强调 JSON 不能写 `#` 注释、只能用英文双引号；
  3. 扫一眼 Markdown 的 `# 标题`、` ``` ` 闭合代码块和 `[文字](网址)`。
- **口播要点**：
  - **关键停顿**：「手改 YAML 只要记住两件事——**绝不按 Tab 键（只敲空格）**、**英文冒号后面空一格**，就能避开 90% 的坑。」

## 5:30 – 8:00｜现场实测改 `config.yaml` + 排错练习 + 下集预告

- **屏幕画面**：先跑一遍默认 `practice/scripts/daily_briefing.py` 预览漂亮的 `daily-briefing.md`（Top 5 模型 + 5 条 HN 热点）；接着把 `config.yaml` 里 `min_points: 50` 改成 `500` 重跑，现场看到 HN 热点立刻收紧成最重磅的 3 条（2723 分 Nvidia、1909 分 OSS 争论、518 分 LLM Agents）——全程一行 Python 没动！最后切到第 5 节 3 雷找错练习。
- **口播要点**：
  - 预告 M3 压轴课 **3.4《密钥与数据安全》**：汇率、关键词可以大大方方写进 `config.yaml`；但 API Key、客户手机号、公司工资条绝不能进这里——下节课划清所有安全红线。

---

## 录制注意事项

- 现场演示把 `min_points` 改成 `500` 重跑完之后，记得把 `practice/config.yaml` 改回默认的 `50`，保持仓库示例一致。
