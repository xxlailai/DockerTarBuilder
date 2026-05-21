import os
import json
import urllib.parse

# ===== 核心配置区 =====
ALIST_BASE = "http://107.174.210.229:5244"
# Alist 里的漫画根目录路径（/d/manga 是直链路径）
MANGA_ALIST_PATH = "/d/manga"
# 本地漫画文件夹路径（和 Alist 挂载的源文件夹保持一致）
LOCAL_DIR = "./manga"

BASE_URL = f"{ALIST_BASE}{MANGA_ALIST_PATH}"


def generate_venera_json():
    explore_data = {
        "hot": [],
        "recommend": []
    }

    manga_list_dir = os.path.join(LOCAL_DIR, "漫画列表")
    if not os.path.exists(manga_list_dir):
        print("错误：未找到 '漫画列表' 文件夹，请检查 LOCAL_DIR 配置")
        return

    # 遍历每一部漫画
    for manga_id in os.listdir(manga_list_dir):
        manga_path = os.path.join(manga_list_dir, manga_id)
        if not os.path.isdir(manga_path):
            continue

        print(f"正在处理漫画: {manga_id}")

        # 默认元数据
        title = manga_id
        cover_url = f"{BASE_URL}/漫画列表/{urllib.parse.quote(manga_id)}/cover.jpg"

        comic_info = {
            "title": title,
            "cover": cover_url,
            "description": f"基于自建 Alist 的私有漫画: {title}",
            "author": "未知作者",
            "tags": ["自建源", "WebDAV"],
            "chapters": []
        }

        # 遍历章节
        for ch_id in sorted(os.listdir(manga_path)):
            ch_path = os.path.join(manga_path, ch_id)
            if not os.path.isdir(ch_path):
                continue

            # 处理每一章内的图片
            pages = sorted([p for p in os.listdir(ch_path) if p.lower().endswith(('jpg', 'png', 'webp', 'jpeg'))])
            page_urls = [
                f"{BASE_URL}/漫画列表/{urllib.parse.quote(manga_id)}/{urllib.parse.quote(ch_id)}/{urllib.parse.quote(p)}"
                for p in pages
            ]

            # 生成该章节的 pages.json
            pages_data = {"file_list": page_urls}
            with open(os.path.join(ch_path, "pages.json"), "w", encoding="utf-8") as f:
                json.dump(pages_data, f, ensure_ascii=False, indent=2)

            # 记录到章节列表
            comic_info["chapters"].append({
                "id": ch_id,
                "title": ch_id
            })

        # 生成这部漫画的 info.json
        with open(os.path.join(manga_path, "info.json"), "w", encoding="utf-8") as f:
            json.dump(comic_info, f, ensure_ascii=False, indent=2)

        # 整合到大厅首页数据
        manga_entry = {
            "id": manga_id,
            "title": title,
            "cover": cover_url,
            "subTitle": f"共 {len(comic_info['chapters'])} 话"
        }
        explore_data["hot"].append(manga_entry)
        explore_data["recommend"].append(manga_entry)

    # 生成总控大厅 UI 的 index_ui.json
    with open(os.path.join(LOCAL_DIR, "index_ui.json"), "w", encoding="utf-8") as f:
        json.dump(explore_data, f, ensure_ascii=False, indent=2)

    print("✨ 全套 Venera 静态 JSON 索引生成完毕！请将它们同步至 Alist。")


if __name__ == "__main__":
    generate_venera_json()
