#!/usr/bin/env python3
"""
快速查看下載進度
"""

import os
import subprocess
from pathlib import Path

def count_posts():
    """統計文章數"""
    posts_dir = Path('_posts')
    return len(list(posts_dir.glob('*.md')))

def count_image_dirs():
    """統計圖片目錄數"""
    images_dir = Path('assets/images')
    return len([d for d in images_dir.glob('*') if d.is_dir()])

def check_process():
    """檢查下載進程是否在運行"""
    try:
        result = subprocess.run(
            ['ps', 'aux'], 
            capture_output=True, 
            text=True
        )
        for line in result.stdout.split('\n'):
            if 'download_missing.py' in line and 'grep' not in line:
                return True, line.strip()
        return False, None
    except:
        return False, None

def main():
    total_in_sitemap = 1189
    target_to_download = 978
    original_count = 211
    
    current_count = count_posts()
    image_dirs = count_image_dirs()
    newly_downloaded = current_count - original_count
    remaining = target_to_download - newly_downloaded
    
    progress_percent = (current_count / total_in_sitemap) * 100
    download_percent = (newly_downloaded / target_to_download) * 100 if target_to_download > 0 else 0
    
    print("=" * 60)
    print("📊 下載進度報告")
    print("=" * 60)
    print(f"\n總文章數 (sitemap):  {total_in_sitemap} 篇")
    print(f"已下載文章數:        {current_count} 篇 ({progress_percent:.1f}%)")
    print(f"本次新增:            {newly_downloaded} 篇")
    print(f"本次還需下載:        {remaining} 篇")
    print(f"本次下載進度:        {download_percent:.1f}%")
    print(f"\n圖片目錄數:          {image_dirs} 個")
    
    # 檢查進程狀態
    is_running, process_info = check_process()
    print(f"\n下載進程狀態:        ", end='')
    if is_running:
        print("✅ 運行中")
        # 預估剩餘時間（假設每篇2秒）
        if remaining > 0:
            estimated_minutes = (remaining * 2) / 60
            print(f"預估剩餘時間:        約 {estimated_minutes:.1f} 分鐘")
    else:
        print("⏸️  已停止")
        if remaining > 0:
            print("\n💡 要繼續下載，請執行: python3 download_missing.py")
        else:
            print("\n✅ 下載已完成！")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
