# 2.7 录播参考脚本：库与 `pip install`

> 建议时长：7–9 分钟（边对比 `fetch_snapshots.py` 和 `build_top10.py` 的 `import` 区、边在终端跑 `pip show openpyxl` 边讲，以下为口播要点与屏幕节点，不作逐字稿）。

## 中英术语读法

| 术语 | 读法 | 首次出现时的口头解释 |
|---|---|---|
| Library / Package | 中文直接说「库」或「扩展包」 | 别人写好、拿来就能用的功能工具箱 |
| Standard Library | 中文说「标准库」 | 装好 Python 就免费自带的基础工具箱 |
| PyPI | P-Y-P-I（或读派-派） | Python 官方应用商店网站 `pypi.org` |
| `pip` | 皮普 | Python 应用商店的命令行下载工具 |
| `openpyxl` | 欧朋-P-Y-X-L | 专门读写带格式 Excel（`.xlsx`）的第三方库 |
| `pandas` | 潘达斯（熊猫） | Python 里最常用的数据表格分析库 |
| Typosquatting | 中文说「包名拼写投毒」 | 黑客抢注少打或错打一个字母的假包名骗人下载 |

---

## 0:00 – 0:45｜开场 Hook（为什么一个直接跑，一个非要装包？）

- **屏幕画面**：左屏放 `fetch_snapshots.py` 顶部 4 行 `import`，右屏放 `build_top10.py` 顶部 4 行 `import`，高亮 `import openpyxl`。
- **口播要点**：
  - 「同是仓库里的两个脚本，抓网页数据的 `fetch_snapshots.py` 什么都不用装直接跑；写 Excel 的 `build_top10.py` 在新电脑上就会提示缺 `openpyxl`，AI 马上弹窗问你能不能 `pip install openpyxl`。」
  - 用「新手机自带 App vs 应用商店下载 App」一秒讲透标准库和第三方库。

## 0:45 – 3:30｜职场高频白名单 + 3 种 `import` 写法

- **屏幕画面**：亮出 6 个办公高频第三方库白名单（`openpyxl`、`pandas`、`requests`、`pyyaml`、`python-docx`、`matplotlib`），顺便亮出 3 种 `import` 写法（整箱导入、`from ... import ...`、起外号 `as pd`）。
- **口播要点**：
  - 顺带消掉一个常见困惑：`pyyaml` 装的时候叫 `pyyaml`，代码里写 `import yaml`；`python-docx` 代码里写 `import docx`，不是 AI 写错了。
  - 提醒一句：看到 `python3 -m pip install` 比光秃秃的 `pip install` 更稳，防止装进电脑里另一个版本的 Python。

## 3:30 – 5:45｜监工最该记牢的安全红线 + `pip show` 验身

- **屏幕画面**：大字标红对比 `openpyxl` vs `openpyx1`（字母 l vs 数字 1）和 `requests` vs `reqeusts`；然后切到终端现场敲 `python3 -m pip show openpyxl`。
- **口播要点**：
  - **关键停顿**：讲清包名拼写投毒（Typosquatting）——「PyPI 谁都能上传包，看到 AI 申请 `pip install`，用 5 秒把包名拼写核对一遍，陌生仓库地址 `git+https://...` 一律点拒绝。」
  - 指着 `pip show openpyxl` 里的 `Version: 3.1.5`、`License: MIT`、`Requires: et-xmlfile`，教观众随时验明本地包的正身。

## 5:45 – 7:30｜现场 4 选 2 审批练习 + 下集预告

- **屏幕画面**：贴出第 5 节 4 条 `pip install` 命令，停 5 秒让观众辨真假再揭晓 `openpyx1` 和陌生 `git+https://` 两个坑。
- **口播要点**：
  - 预告 M2 压轴课 **2.8《读懂报错》**：代码顺风顺水时咱们都能看懂了，下节课专门攻克最让人发怵的大片英文报错，教你「从最后一行往上读」三步法。

---

## 录制注意事项

- 展示 `pip show openpyxl` 时注意确认终端输出的 `Location` 路径里没有个人真实姓名（如涉及本机用户目录，可以口播或用虚拟环境短路径展示）。
