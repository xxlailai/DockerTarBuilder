class RenAlistSource {
    constructor() {
        this.name = "Ren 的私有漫画库";
        this.key = "ren_alist_private_manga";
        this.version = "1.0.0";
        this.minAppVersion = "1.0.0";

        // 核心：指向你的 Alist 根直链
        this.alistBase = "http://107.174.210.229:5244/d/manga";
    }

    // 渲染独立首页 UI 大厅
    async getExplorePage(page) {
        const url = `${this.alistBase}/index_ui.json`;
        const res = await fetch(url);
        const data = await res.json();

        return {
            type: "multiPartPage",
            parts: [
                {
                    name: "🔥 热门连载",
                    type: "fixed",
                    comics: data.hot
                },
                {
                    name: "⭐ 精选推荐",
                    type: "fixed",
                    comics: data.recommend
                }
            ]
        };
    }

    // 搜索功能（对大厅静态数据进行前端模糊搜索）
    async search(keyword, page) {
        const url = `${this.alistBase}/index_ui.json`;
        const res = await fetch(url);
        const data = await res.json();

        const allComics = data.hot || [];
        const filtered = allComics.filter(c => c.title.toLowerCase().includes(keyword.toLowerCase()));

        return {
            comics: filtered,
            hasMore: false
        };
    }

    // 漫画详情页与章节列表 UI
    async getComicDetails(id) {
        const url = `${this.alistBase}/漫画列表/${encodeURIComponent(id)}/info.json`;
        const res = await fetch(url);
        const data = await res.json();

        return {
            title: data.title,
            cover: data.cover,
            description: data.description,
            author: data.author,
            tags: data.tags,
            chapters: data.chapters
        };
    }

    // 阅读器内解析具体某一章的图片流
    async getChapterImages(comicId, chapterId) {
        const url = `${this.alistBase}/漫画列表/${encodeURIComponent(comicId)}/${encodeURIComponent(chapterId)}/pages.json`;
        const res = await fetch(url);
        const data = await res.json();

        return {
            images: data.file_list
        };
    }
}

// 注册进 Venera 沙箱
// eslint-disable-next-line no-undef
registerComicSource(new RenAlistSource());
