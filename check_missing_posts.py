#!/usr/bin/env python3
"""
檢查 sitemap 中有哪些文章尚未下載
"""

import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup

def get_sitemap_posts():
    """從 sitemap 獲取所有文章 ID"""
    url = "https://kuni.pixnet.net/blog/sitemap-posts.xml"
    print(f"正在下載 sitemap: {url}")
    
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'xml')
    post_ids = []
    
    for loc in soup.find_all('loc'):
        url = loc.text
        match = re.search(r'/posts/(\d{10})', url)
        if match:
            post_ids.append(match.group(1))
    
    return set(post_ids)

def get_downloaded_posts():
    """獲取已下載的文章 ID"""
    posts_dir = Path('_posts')
    post_ids = []
    
    for md_file in posts_dir.glob('*.md'):
        match = re.search(r'(\d{10})', md_file.name)
        if match:
            post_ids.append(match.group(1))
    
    return set(post_ids)

def main():
    print("=" * 80)
    print("檢查缺失的文章")
    print("=" * 80)
    
    # 獲取 sitemap 中的所有文章
    sitemap_posts = get_sitemap_posts()
    print(f"✓ Sitemap 中的文章數: {len(sitemap_posts)}")
    
    # 獲取已下載的文章
    downloaded_posts = get_downloaded_posts()
    print(f"✓ 已下載的文章數: {len(downloaded_posts)}")
    
    # 找出缺失的文章
    missing_posts = sitemap_posts - downloaded_posts
    print(f"\n⚠️  缺失的文章數: {len(missing_posts)}")
    
    if missing_posts:
        # 按 ID 排序
        sorted_missing = sorted(missing_posts)
        
        print(f"\n缺失文章 ID 範圍:")
        print(f"  最早: {sorted_missing[0]}")
        print(f"  最新: {sorted_missing[-1]}")
        
        # 儲存到檔案
        output_file = 'missing_posts.txt'
        with open(output_file, 'w') as f:
            for post_id in sorted_missing:
                f.write(f"https://kuni.pixnet.net/blog/posts/{post_id}\n")
        
        print(f"\n✓ 已將缺失文章 URL 儲存到: {output_file}")
        
        # 顯示前 20 個缺失的文章
        print(f"\n前 20 個缺失的文章 ID:")
        for post_id in sorted_missing[:20]:
            print(f"  - {post_id}")
        
        if len(missing_posts) > 20:
            print(f"  ... 還有 {len(missing_posts) - 20} 篇")
    
    # 檢查是否有多餘的文章（不在 sitemap 中）
    extra_posts = downloaded_posts - sitemap_posts
    if extra_posts:
        print(f"\n⚠️  發現 {len(extra_posts)} 篇不在 sitemap 中的文章:")
        for post_id in sorted(extra_posts):
            print(f"  - {post_id}")
    
    print("\n" + "=" * 80)
    
    return len(missing_posts)

if __name__ == '__main__':
    missing_count = main()
    exit(0 if missing_count == 0 else 1)
