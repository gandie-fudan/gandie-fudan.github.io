# 甘叠 / Die Gan · Academic Website

中英双语数学与控制方向学术主页。白底、深蓝配色，以简洁的教师主页结构组织研究、论文、教学和经历。设计参考 al-folio 的视觉层次、Yang Zheng 的栏目结构与 Stephen Tu 的论文分类，使用独立编写的静态生成器实现，并非安装了上述模板。

## 我只想修改内容

部署完成后，日常修改只需要登录 GitHub：

1. 打开此仓库，点击 **content.json**。
2. 点击文件右上方的铅笔按钮 **Edit this file**。
3. 找到需要修改的中文或英文文字。`zh` 是中文，`en` 是英文。只修改引号内的文字，保留逗号、括号和英文双引号。
4. 点击 **Commit changes…**，填写简短说明（例如“更新课程信息”），保存到 `master`。
5. 点击仓库的 **Actions**，等待最新的 **Build and deploy academic website** 出现绿色对勾，网站便会自动更新。不需要在电脑安装 Python、运行代码或重复上传网页。
6. 若出现红叉，原来成功发布的网站仍可访问；打开失败记录查看提示，通常是 JSON 标点错误。可以联系协作者修复或恢复到上一版，不必删除仓库。

网站为公开的静态页面。GitHub 登录用于管理源文件，不是在主页里登录。首次账号连接和部署需完成后才能使用以上更新方式。

## 内容在哪里

| 内容 | content.json 中的字段 |
|---|---|
| 姓名、职称、单位、简介、邮箱 | name、role、affiliation、bio、email |
| 个人照片 | photo |
| 四个研究主题 | research |
| 全部论文 | publications |
| 主持或参与项目 | projects 中的 role |
| 课程与指导成果 | teaching、mentoring |
| 工作、教育经历 | work、education |
| 学术服务、荣誉 | service、honors |
| 专利 | patents |

### 更新论文

`publications` 内每一组花括号是一篇论文。新增论文可以复制一组并修改，确保 `id` 不重复。

- `authors`：按论文原始作者顺序填写，星号只用于明确的通讯作者标记。
- `title`：正式论文题名。
- `venue`：期刊/会议名称、卷期页码、年份等完整信息。更新状态时也应同步修改这里的 Accepted 或 under review 等文字。
- `year`：数字年份。页面在每个状态分组内自动按年份倒序。
- `status`：`published`（已发表）、`accepted`（已录用）、`review`（在审）、`unspecified`（预印本/在审栏目内，确切状态未注明）。
- `kind`：`journal`（期刊）或 `conference`（会议）。
- `selected`：`true` 会在首页代表论文中展示，`false` 只在完整列表展示。建议首页保持 4–6 篇。
- `links`：仅添加已核实的链接。例如 `[{"label":"DOI","url":"https://doi.org/实际的DOI"}]`；没有链接则保留 `[]`。

### 添加或更换照片

1. 在仓库中打开 `assets` 文件夹，选择 **Add file → Upload files** 上传希望公开的照片，例如 `portrait.jpg`。
2. 将 content.json 中 `"photo": ""` 改为 `"photo": "assets/portrait.jpg"`。
3. 保存后网站自动生成照片区。留空时不显示照片，也不显示占位框。

## 页面结构

- `index.html` / `index-en.html`：简介、研究主题、代表论文。
- `publications.html` / `publications-en.html`：论文完整列表、状态分类、搜索筛选、专利。
- `projects.html` / `projects-en.html`：项目及角色。
- `teaching.html` / `teaching-en.html`：教学与指导。
- `experience.html` / `experience-en.html`：教育与工作经历。
- `service.html` / `service-en.html`：服务与荣誉。

两种语言始终切换到对应页面。内容在 HTML 内，关闭 JavaScript 仍能阅读全部论文。

## 首次部署设置（交接或迁移时使用）

完整仓库需包含 `content.json`、`build.py`、`validate.py`、`assets/` 和 `.github/workflows/pages.yml`。不要只上传压缩包文件本身。

1. 在自己的 GitHub 账号创建公开仓库。若希望使用 `https://用户名.github.io/`，仓库命名为 `用户名.github.io`；普通仓库名会产生带仓库名的子路径。
2. 上传上述源码文件，包括隐藏目录 `.github`。不要上传原始简历和本地审阅记录。
3. 打开 **Settings → Pages → Build and deployment → Source**，选择 **GitHub Actions**。
4. 打开 **Actions → Build and deploy academic website → Run workflow**，选择 `master` 运行一次。
5. 等待成功，回到 **Settings → Pages** 查看发布网址。以后修改内容自动发布。

官方文档：[自定义 GitHub Pages 工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

## 本地预览（可选）

有 Python 3 时运行 `python build.py`，再运行 `python validate.py`。打开 `dist/index.html` 即可离线查看。

本项目没有第三方 Python 依赖、广告、跟踪器或外部字体。Pages 只发布 `dist` 内的网页资源。仓库中的源码和 content.json 也会随公开仓库被他人查看，请勿填写私人信息。

## 内容与设计说明

个人事实依据为所提供的简历，不根据时间推断论文发表、项目结题或招生名额。简历未包含的 DOI、代码和学术平台链接未填入。页面不包含原始简历、电话及详细街道地址。代表论文是可调整的展示选择，不表示新增作者贡献或学术评价。

