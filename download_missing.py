#!/usr/bin/env python3
"""
批量下載缺失的文章
支援斷點續傳、進度追蹤和錯誤記錄
"""

import os
import sys
import time
from pathlib import Path
from scraper import PixnetScraper

def load_urls_from_file(filename):
    """從檔案載入 URL 列表"""
    with open(filename, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls

def get_already_downloaded():
    """取得已下載的文章 ID"""
    posts_dir = Path('_posts')
    downloaded = set()
    
    for md_file in posts_dir.glob('*.md'):
        # 從檔名中提取 post ID (最後的10位數字)
        import re
        match = re.search(r'(\d{10})\.md$', md_file.name)
        if match:
            downloaded.add(match.group(1))
    
    return downloaded

def extract_post_id(url):
    """從 URL 提取 post ID"""
    return url.rstrip('/').split('/')[-1]

def main():
    print("=" * 80)
    print("批量下載缺失文章")
    print("=" * 80)
    
    # 載入缺失的文章 URL
    urls_file = 'missing_posts.txt'
    if not os.path.exists(urls_file):
        print(f"錯誤: 找不到 {urls_file}")
        print("請先執行 check_missing_posts.py 生成缺失文章列表")
        return 1
    
    print(f"\n正在載入: {urls_file}")
    all_urls = load_urls_from_file(urls_file)
    print(f"✓ 載入 {len(all_urls)} 個 URL")
    
    # 檢查哪些已經下載
    print("\n檢查已下載的文章...")
    already_downloaded = get_already_downloaded()
    print(f"✓ 已下載: {len(already_downloaded)} 篇")
    
    # 過濾出尚未下載的
    urls_to_download = []
    for url in all_urls:
        post_id = extract_post_id(url)
        if post_id not in already_downloaded:
            urls_to_download.append(url)
    
    if not urls_to_download:
        print("\n✓ 所有文章都已下載完成！")
        return 0
    
    print(f"✓ 需要下載: {len(urls_to_download)} 篇")
    print(f"✓ 已跳過: {len(all_urls) - len(urls_to_download)} 篇 (已存在)")
    
    # 顯示下載資訊
    print("\n" + "=" * 80)
    print(f"將要下載 {len(urls_to_download)} 篇文章")
    print("預估時間: {:.1f} 分鐘 (假設每篇 2 秒)".format(len(urls_to_download) * 2 / 60))
    print("=" * 80)
    print("\n自動開始下載...")
    
    # 開始下載
    scraper = PixnetScraper()
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    failed_urls = []
    
    start_time = time.time()
    
    print("\n" + "=" * 80)
    print("開始下載...")
    print("=" * 80)
    
    for i, url in enumerate(urls_to_download, 1):
        post_id = extract_post_id(url)
        elapsed = time.time() - start_time
        avg_time = elapsed / i if i > 0 else 0
        remaining = (len(urls_to_download) - i) * avg_time
        
        print(f"\n[{i}/{len(urls_to_download)}] (剩餘約 {remaining/60:.1f} 分鐘)")
        print(f"URL: {url}")
        
        try:
            # 抓取文章
            article = scraper.scrape_article(url)
            
            if article:
                # 轉換並儲存為 Markdown
                scraper.convert_to_markdown(article, url)
                success_count += 1
            else:
                print(f"  ✗ 抓取失敗")
                fail_count += 1
                failed_urls.append((url, "抓取失敗"))
        
        except Exception as e:
            print(f"  ✗ 發生錯誤: {e}")
            fail_count += 1
            failed_urls.append((url, str(e)))
        
        # 避免過度請求 - 每次請求間隔 1-2 秒
        if i < len(urls_to_download):
            time.sleep(1.5)
        
        # 每 50 篇顯示進度摘要
        if i % 50 == 0:
            print("\n" + "-" * 80)
            print(f"進度摘要: 已處理 {i}/{len(urls_to_download)}")
            print(f"  成功: {success_count} | 失敗: {fail_count}")
            print(f"  已用時間: {elapsed/60:.1f} 分鐘")
            print("-" * 80)
    
    # 總結
    total_time = time.time() - start_time
    print("\n" + "=" * 80)
    print("下載完成！")
    print("=" * 80)
    print(f"總共處理: {len(urls_to_download)} 篇")
    print(f"成功: {success_count} 篇")
    print(f"失敗: {fail_count} 篇")
    print(f"總耗時: {total_time/60:.1f} 分鐘")
    print(f"平均速度: {total_time/len(urls_to_download):.2f} 秒/篇")
    print("=" * 80)
    
    # 儲存失敗的 URL
    if failed_urls:
        failed_file = 'failed_downloads.txt'
        with open(failed_file, 'w') as f:
            f.write("# 下載失敗的文章\n")
            f.write(f"# 生成時間: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for url, reason in failed_urls:
                f.write(f"{url}\n# 原因: {reason}\n\n")
        
        print(f"\n⚠️  失敗的 URL 已儲存至: {failed_file}")
        print("可以稍後重新執行此腳本，會自動跳過已下載的文章")
    
    return 0 if fail_count == 0 else 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n已中斷！進度已保存，可稍後繼續執行")
        sys.exit(130)
