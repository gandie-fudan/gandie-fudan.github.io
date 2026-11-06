# 甘叠 / Die Gan · Academic Website

中英双语数学与控制方向学术主页。当前版主要参考 [Yang Zheng 主页](https://zhengy09.github.io/) 的简介组织、衬线字体与学术排版，采用白底、深蓝配色和左侧导航。使用独立编写的静态生成器实现，并非安装了 jemdoc 或 al-folio 模板。

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
| 计划探索的方向与研究问题 | exploration（中英标题、介绍、questions） |
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
- `status`：`published`（已发表）、`accepted`（已录用）、`review`（在审）、`preprint`（预印本）、`unspecified`（确切状态未注明）。
- `kind`：`journal`（期刊）、`conference`（会议）或 `preprint`（预印本）。
- `selected`：保留以便将来恢复代表论文展示；当前首页不显示论文列表，此字段不影响现有页面。
- `links`：仅添加已核实的链接。例如 `[{"label":"DOI","url":"https://doi.org/实际的DOI"}]`；没有链接则保留 `[]`。

### Google Scholar 核对

个人主页地址在 `scholar`，最近人工核对日期在 `publications_verified_on`。论文标题优先链接到 `publisher_url`（出版社的文章详情页）；未设置时依次使用 DOI、arXiv 或其他已有链接。`links` 保留 DOI 和 Google Scholar 等补充入口。请核对题名和作者后再填写 `publisher_url`。

2026-11-06 已按本人 Google Scholar 主页和可核实的出版记录更新：30 篇已发表、4 篇已录用、2 篇在审、2 篇预印本、1 篇具体状态未注明。34 篇有对应的 Scholar 条目，28 篇有 DOI；30 篇已发表论文均设置了出版社文章链接。预印本不会自动视作已发表。期刊正式卷期年份与 Scholar 的 online-first 年份可能不同，现有正式卷期年份予以保留。

目前是本次人工核对后的静态版本，没有开启定时抓取。以后更新 Scholar 后，需要再次核对并修改 content.json，GitHub Actions 会自动构建和部署网站；仅修改 Scholar 不会自动改写本站。

### 添加或更换照片

1. 在仓库中打开 `assets` 文件夹，选择 **Add file → Upload files** 上传希望公开的照片，例如 `portrait.jpg`。
2. 将 content.json 中 `photo` 的值改为新文件路径，例如 `"photo": "assets/portrait.jpg"`。目前使用本人提供的 `assets/portrait.png`。
3. 保存后网站自动生成照片区。留空时不显示照片，也不显示占位框。

## 页面结构

- `index.html` / `index-en.html`：头像、简介、研究主题与概念图、灵巧手未来研究计划。
- `experience.html` / `experience-en.html`：教育与工作经历。
- `publications.html` / `publications-en.html`：论文完整列表、状态分类、搜索筛选。
- `projects.html` / `projects-en.html`：项目及角色。
- `patents.html` / `patents-en.html`：专利及简历记录的授权/审查状态。
- `honors.html` / `honors-en.html`：荣誉与奖励。
- `teaching.html` / `teaching-en.html`：教学与指导。
- `service.html` / `service-en.html`：学术服务。

主导航顺序为：简介、经历、论文、项目、专利、荣誉、教学、服务（About, Experience, Publications, Projects, Patents, Honors, Teaching, Service）。专利、荣誉与服务分别读取 `content.json` 中的 `patents`、`honors` 和 `service` 字段。

两种语言始终切换到对应页面。内容在 HTML 内，关闭 JavaScript 仍能阅读全部论文。

### 视觉与探索方向（2026-11-06 更新）

新版参考 Yang Zheng 主页的学术排版：桌面左侧导航、照片与个人信息并排、连续段落简介、蓝色标题和论文链接、细分隔线。英文使用 Georgia，中文使用系统宋体/衬线字体；正文18px，论文标题20px，作者和刊物17px，手机端按空间调整。照片按原比例显示，没有改变人像。所有栏目共用一份样式。网站无需加载第三方字体或图片。

简介正文在 `bio`，背景段落在 `biography_background`，需要加粗的已有短语在 `bio_emphasis`。编辑经历后请同步检查首页背景段落。

首页的“灵巧手系统辨识”根据本人表达的兴趣设置，明确标注为未来研究方向。`exploration.title` 和 `intro` 控制标题与导语，`questions` 控制三个研究主题及详细说明，`approach` 控制拟开展的研究路径。以上均有中文与英文。删除整个 `exploration` 字段即可隐藏此区域。

首页恢复两幅原有概念图：研究方向旁的 `assets/research-map.svg` 和未来研究部分的 `assets/hand-study.svg`。图片均用于说明研究思路，不表示已有设备或实验结果。首页已移除代表论文列表，完整论文仍在独立“论文”栏目。新增布局样式限定在 `.index`，其他栏目排版保持原样。

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

个人事实以所提供的简历为基础，论文链接与状态结合本人 Google Scholar 和已核实出版记录补充。不根据时间推断论文发表、项目结题或招生名额。页面不包含原始简历、电话及详细街道地址。代表论文是可调整的展示选择，不表示新增作者贡献或学术评价。

