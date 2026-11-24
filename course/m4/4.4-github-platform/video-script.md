# 4.4 录播参考脚本：从 0 认识 GitHub：注册与全平台板块导览

> 建议时长：10–12 分钟（浏览器边演示注册要点和全平台板块边讲，以下为口播要点与屏幕节点，不作逐字稿）。

## 中英术语读法

| 术语 | 读法 | 首次出现时的口头解释 |
|---|---|---|
| GitHub | 吉特哈布（Git-Hub） | 全球最大的代码托管、开源广场与协作平台 |
| Sign up / Sign in | 赛恩阿普 / 赛恩印 | 注册新账号 / 登录已有账号 |
| 2FA（Two-Factor Authentication） | 二-F-A（双因素认证） | 输密码之外再加一层手机验证码，防账号被盗 |
| Organization / Org | 中文说「组织账号」 | 公司、团队或官方项目用的机构号（如 `deepseek-ai`） |
| Dashboard / Home | 达什博德（工作台） | 登录后看到的个人主控台首页 |
| Trending | 喘丁（趋势榜） | GitHub 每日/每周最热门开源项目热搜榜 |
| Topics | 托皮克斯（主题标签） | 按领域分类的项目合集广场 |
| Marketplace | 玛克特普莱斯 | GitHub 插件与自动化机器人应用商店 |
| Public / Private | 公开 / 私有 | 仓库谁能看：全世界可见 vs 仅自己/授权成员可见 |
| PAT（Personal Access Token） | P-A-T（个人访问令牌） | 给终端或 AI 工具连接 GitHub 用的电子钥匙 |

---

## 0:00 – 0:50｜开场 Hook（先给没注册过的人吃定心丸）

- **屏幕画面**：浏览器打开 `https://github.com/` 和 `https://github.com/pricing`，鼠标直接圈住 `Free $0 USD`。
- **口播要点**：
  - 直接打消顾虑：「很多同学刷到 AI 开源项目，听人说去 GitHub 下，但从来没注册过账号，一看满屏英文就关掉了——怕收费、怕只有程序员才能用、怕点错按钮。」
  - 定调：个人和小团队基础版 **完全免费（`$0 USD`），支持无限个公开和私有仓库**。今天从注册讲起，10 分钟带你把 GitHub 整个平台每一个功能板块彻底摸透。

## 0:50 – 2:30｜三层空间地图 + 从 0 注册与 2FA 要点

- **屏幕画面**：先画三层关系（本地 Git ↔ GitHub 平台大厅 ↔ 单个仓库内部），再演示 `Sign up` 入口。
- **口播要点**：
  - 交代 4 步注册里最该留心的 2 个细节：
    1. 用长期私人邮箱，别用可能离职停用的公司邮箱；
    2. 用户名（Username）会永久出现在网址 `github.com/你的用户名/...` 里，起个简洁英文/拼音，绝别带手机号。
  - **重点叮嘱 2FA**：注册完第一步进 `Settings → Password and authentication` 开双因素认证，顺手把 `Recovery codes`（恢复码）存好。

## 2:30 – 4:15｜一眼分清：个人主页 vs 官方组织主页

- **屏幕画面**：两个标签页对比切屏——先看 `github.com/torvalds`（个人主页），再切 `github.com/deepseek-ai`（官方组织主页）。
- **口播要点**：
  - 个人主页带观众认 4 块：顶栏 5 标签（重点夸一下去大佬主页看 `Stars` 找宝藏）、`Pinned` 置顶、底下标志性的绿色贡献热力图「小绿点」。
  - 切到 `deepseek-ai`：指出多了 `People` 成员栏和官网/官方邮箱认证——以后辨别是不是官方工具，先点进斜杠前面的主页看一眼。

## 4:15 – 7:45｜全平台 8 大功能板块逐个带逛

- **屏幕画面**：依次打开并鼠标指认真实页面：
  1. 登录后顶部全局栏（`☰` 抽屉、`/` 搜索、`+` 新建、小铃铛 `Notifications`、右侧头像菜单）与 `Home` 工作台；
  2. `github.com/trending`（现场演示切换 `Language: Python` 和 `Date range: This week`）；
  3. 按键盘 **`/`** 键搜 `deepseek-harness`，展示左侧 `Filter by`（从 `Repositories` 切到 `Discussions` 搜报错）和右上角 `Sort by: Most stars`；
  4. 扫一眼 `github.com/topics`（点出 `Awesome Lists` 找精选大全的窍门）和 `github.com/marketplace`（认识 `Apps` / `Actions` 商店）。
- **口播要点**：
  - 讲 `Your stars` 时重点教一个好用动作：点 `Create list` 给收藏建分组（比如「AI 工具」「Excel 脚本」），告别收藏即吃灰。

## 7:45 – 9:45｜手把手演练：`+ New repository` 建第一个私有仓库 + `Settings` 安全自查

- **屏幕画面**：点右上角 `+ → New repository`（演示填入 `ai-radar`、**高亮选中 `Private` 私有**、勾选 `README` 和 `.gitignore: Python`）；再切到 `Settings → Applications` 点出 `Revoke` 一键解绑闲置授权。
- **口播要点**：
  - **关键停顿**（破除最大误解）：很多人以为在 GitHub 建仓库就会把资料公开给全世界，其实免费版就能无限建 `Private` 私有库！公司或个人工作脚本，默认永远先选 `Private`。
  - 顺带提一句 `Developer settings → Personal access tokens` 是以后给电脑或 AI 推代码用的电子钥匙，绝不能外泄。

## 9:45 – 10:45｜收尾复盘 + 下集预告

- **屏幕画面**：回到「5 分钟上手 4 步清单」（逛榜 Star 分组 → `/` 全局搜 → 辨官方号 → 建私有 `ai-radar` 库）。
- **口播要点**：
  - 一句话落地：今天把整个 GitHub 平台大厅和自己的私人库房全建好了；
  - 预告 **4.5《GitHub 仓库页导览（以 DeepSeek Harness 仓库为例）》**：下一课我们正式推开具体某一个开源仓库的大门，1 分钟看懂仓库里每个标签页、`Releases` 和 `LICENSE` 商用条款。

---

## 录制注意事项

- 演示登录后的 `Home` 工作台、`+ New repository` 和 `Settings` 时，务必使用专门的演示测试账号，不要暴露个人真实邮箱、私人私有仓库名、通知内容或任何 `Personal access token` / 2FA 二维码与恢复码。
- 如果录屏当天 `github.com/trending` 榜单项目和课件截图不同，直接按当天真实榜单演示筛选操作即可。
