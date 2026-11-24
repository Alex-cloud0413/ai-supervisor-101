# 2.7 小红书速查卡文案

> 适配风格：第六版单栏无衬线排版（1080×1440 / 导出 2160×2880，强调红 `#D03020`）。正式出图前按 `yiming-technical-image-text` 规则另行确认个人 IP 元素。

---

## 封面卡（第 1 张）

**主标题**：AI 弹窗要 `pip install`，怎么 5 秒防住钓鱼假包？
**副标题 / 导语**：零基础《给 AI 当监工》2.7｜分清标准库与第三方库，收藏 6 个办公安全白名单

---

## 第 2 张：标准库 vs 第三方库，一秒分清

**页眉标签**：01｜像手机装 App

- **标准库（自带 App）**：装好 Python 就有，**零安装**。常见：`json`、`pathlib`、`csv`、`datetime`、`urllib`。
- **第三方库（商店下载）**：开源社区写好的专业工具，需要靠 `pip install` 从 PyPI 官方商店安装。

---

## 第 3 张：职场办公 6 个高频白名单第三方库

**页眉标签**：02｜安全白名单

以后看到 AI 申请装这 6 个包，拼写核对无误一般都能放心批：

- `openpyxl`：读写带配色的 `.xlsx` Excel
- `pandas`：大表格合并、清洗、透视分析
- `requests`：抓公开接口/网页数据
- `pyyaml`：读 `.yaml` 配置文件（代码里写 `import yaml`）
- `python-docx`：批量读写 Word 文档（代码里写 `import docx`）
- `matplotlib`：自动画折线图、柱状图

---

## 第 4 张：看懂代码顶部的 3 种 `import`

**页眉标签**：03｜怎么读 `import`

- `import openpyxl` → 整箱工具搬进来
- `from pathlib import Path` → 只从箱子里拿 `Path` 这把工具
- `import pandas as pd` → 搬进来顺便起个短外号 `pd`

装包时看到 `python3 -m pip install` 比直接 `pip install` 更稳，能保证装进当前用的同一个 Python。

---

## 第 5 张：批 `pip install` 前必防的两个坑

**页眉标签**：04｜安全红线

1. **盯紧逐字母拼写（防包名投毒）**：
   - ✅ `openpyxl`（字母 `l`） vs ❌ `openpyx1`（数字 `1`）
   - ✅ `requests` vs ❌ `reqeusts`
2. **陌生网址直接拒**：看到 `pip install git+https://陌生网址...` 一律点「拒绝」！

想查已装包的版本和开源协议，随时可以跑只读命令 `python3 -m pip show openpyxl`。

---

## 正文配文（小红书发布参考）

用 AI 跑数据处理脚本时，最常弹出的审批命令之一就是 `pip install xxx`。

整理了《给 AI 当监工》2.7 课《库与 `pip install`》速查卡：
- 哪些是 Python 自带标准库（不用装）；
- 职场最高频的 6 个安全白名单库；
- 怎么 5 秒防住 `openpyx1` / `reqeusts` 这类黑客拼写投毒假包。

建议直接收藏，下次 AI 弹窗装包前对照拼写扫一眼！

#Python零基础 #pip #AI安全 #职场效率 #给AI当监工
