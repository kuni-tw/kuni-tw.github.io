#!/usr/bin/env python3
"""
測試圖片下載功能
"""

import os
from scraper import PixnetScraper

# 清理測試用的文章和圖片
test_files = [
    '_posts/2018-01-09-GR2日誌---紫琳蒸餃大王首訪(四平店)：無肉勝過有肉！-9461311919.md',
    'assets/images/9461311919'
]

for path in test_files:
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
            print(f"已刪除測試文章: {path}")
        elif os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
            print(f"已刪除測試圖片目錄: {path}")

# 測試抓取一篇文章
scraper = PixnetScraper()
test_url = 'https://kuni.pixnet.net/blog/posts/9461311919'

print("\n" + "=" * 60)
print("測試抓取文章並下載圖片")
print("=" * 60)

article = scraper.scrape_article(test_url)
if article:
    scraper.convert_to_markdown(article, test_url)
    print("\n✓ 測試完成！")
    print(f"請檢查: _posts/ 和 assets/images/9461311919/")
else:
    print("\n✗ 測試失敗")
