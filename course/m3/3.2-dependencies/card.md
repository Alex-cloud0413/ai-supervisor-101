# 3.2 小红书速查卡文案

> 适配风格：第六版单栏无衬线排版（1080×1440 / 导出 2160×2880，强调红 `#D03020`）。正式出图前按 `yiming-technical-image-text` 规则另行确认个人 IP 元素。

---

## 封面卡（第 1 张）

**主标题**：发给同事就报错「缺模块」？看懂 `.venv` 和 `requirements.txt` 彻底解决
**副标题 / 导语**：零基础《给 AI 当监工》3.2｜Mac / Windows 三行命令还原一模一样的运行环境

---

## 第 2 张：两个搭档，终结「在我电脑上能跑」魔咒

**页眉标签**：01｜核心概念

- **`requirements.txt`（采购清单）**：写清项目需要哪几个第三方库及版本范围（如 `openpyxl>=3.1.5,<4.0`、`PyYAML>=6.0.2,<7.0`）。
- **`.venv`（独立工具间）**：给这个项目隔出来的专属虚拟环境，防止不同项目装不同版本库互相打架。

---

## 第 3 张：Mac / Windows 建环境三步命令（照抄）

**页眉标签**：02｜三行搞定

1. **建工具间**：
   - Mac：`python3 -m venv .venv`
   - Win：`python -m venv .venv`
2. **走进去（看到行首亮 `(.venv)`）**：
   - Mac：`source .venv/bin/activate`
   - Win：`.\.venv\Scripts\Activate.ps1`
3. **按清单一次性装齐**：
   - `python3 -m pip install -r requirements.txt`（Win 用 `python`）

---

## 第 4 张：监工必记的 2 条黄金铁律

**页眉标签**：03｜避坑指南

1. **`.venv/` 绝不传 GitHub、绝不打包发人！** 它动辄几十到几百 MB，而且绑定操作系统，Mac 拷到 Windows 根本跑不动——**永远写进 `.gitignore`**，只交 `requirements.txt`！
2. **让 AI 新装了包，顺嘴补一句**：「请把新装的库同步补进 `requirements.txt`」，不然换台电脑照样报错。

---

## 第 5 张：逛 GitHub 顺手认全 4 种依赖清单

**页眉标签**：04｜一眼认出

以后在开源项目根目录看到这些文件，知道它们都是同一类采购单：

- `requirements.txt` → 传统 Python 依赖清单
- `pyproject.toml` / `uv.lock` → 现代 Python 依赖与版本锁文件
- `package.json` → Node.js / 前端项目依赖清单（对应 `npm install`）

---

## 正文配文（小红书发布参考）

把 AI 帮自己写好的脚本发给同事，对方一运行就红字 `ModuleNotFoundError`？或者自己做新项目装了个包，把上个月的老脚本搞崩了？

用好 Python 自带的 `.venv`（独立虚拟环境）和 `requirements.txt`（依赖采购单），换任何一台电脑三行命令 100% 复现！

这是《给 AI 当监工》3.2 课速查卡，Mac 和 Windows 双系统命令都整理好了，记住：**传代码时绝不传 `.venv/`，只传 `requirements.txt`！** 建议先收藏。

#Python零基础 #虚拟环境 #AI编程 #职场效率 #给AI当监工
