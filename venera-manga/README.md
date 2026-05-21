# Venera 漫画源 + Alist 私有漫画库

基于 Alist WebDAV 的 Venera 漫画源方案

## 文件说明

```
venera_manga/
├── ren_alist_source.js   ← Venera 插件脚本（上传到 GitHub）
├── index.json            ← Venera 订阅入口（上传到 GitHub）
├── generate_manga_json.py ← 漫画索引生成脚本（本地运行）
└── manga/                ← 漫画源文件夹
    └── 漫画列表/
        └── [你的漫画文件夹...]
```

## 使用步骤

### 1. 配置 Alist 漫画目录

在 Alist 后台将漫画根文件夹设置为「公开访问」，获取直链路径（如 `/d/manga`）。

### 2. 修改配置

编辑 `generate_manga_json.py`，修改以下配置：

```python
ALIST_BASE = "http://107.174.210.229:5244"
MANGA_ALIST_PATH = "/d/manga"
LOCAL_DIR = "./manga"   # 改成你本地漫画文件夹路径
```

### 3. 生成索引

```bash
python generate_manga_json.py
```

脚本会自动扫描 `manga/漫画列表/` 下的每部漫画，生成：
- `info.json` — 漫画详情（标题、封面、作者、章节列表）
- `chXX/pages.json` — 每章图片直链
- `index_ui.json` — 首页大厅数据

### 4. 同步到 Alist

将 `manga/` 整个目录上传到 Alist 的 `/d/manga` 路径下。

### 5. 上传 JS 到 GitHub

将 `ren_alist_source.js` 和 `index.json` 上传到 GitHub 公开仓库，修改 `index.json` 中的 `url` 为实际 Raw 链接。

### 6. Venera 导入

在 Venera App 中添加第三方订阅，粘贴 `index.json` 的 Raw 链接即可。

## 目录结构示例

```
manga/
├── index_ui.json         ← 自动生成
└── 漫画列表/
    ├── berserk/
    │   ├── cover.jpg
    │   ├── info.json      ← 自动生成
    │   ├── ch01/
    │   │   ├── pages.json ← 自动生成
    │   │   ├── 001.jpg
    │   │   └── 002.jpg
    │   └── ch02/
    └── fire_punch/
        └── ...
```
