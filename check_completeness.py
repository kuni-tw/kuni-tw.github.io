#!/usr/bin/env python3
"""
檢查所有文章與圖片下載是否完成
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def extract_post_id(filename):
    """從檔名中提取 post ID"""
    match = re.search(r'(\d{10})', filename)
    return match.group(1) if match else None

def check_images_in_markdown(md_file):
    """檢查 markdown 文章中的圖片引用"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有圖片引用: ![...](...) 或 <img src="...">
    markdown_images = re.findall(r'!\[.*?\]\((.*?)\)', content)
    html_images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    
    all_images = markdown_images + html_images
    
    # 分類圖片：本地 vs 外部
    local_images = []
    external_images = []
    
    for img in all_images:
        if img.startswith('http://') or img.startswith('https://'):
            external_images.append(img)
        elif img.startswith('/assets/images/'):
            local_images.append(img.lstrip('/'))
    
    return local_images, external_images

def main():
    posts_dir = Path('_posts')
    images_dir = Path('assets/images')
    
    print("=" * 80)
    print("檢查文章與圖片下載完成度")
    print("=" * 80)
    
    # 統計資料
    total_posts = 0
    posts_with_local_images = 0
    posts_with_external_images = 0
    total_local_images = 0
    total_external_images = 0
    missing_images = []
    
    # 檢查所有文章
    for md_file in sorted(posts_dir.glob('*.md')):
        total_posts += 1
        post_id = extract_post_id(md_file.name)
        
        local_imgs, external_imgs = check_images_in_markdown(md_file)
        
        if local_imgs:
            posts_with_local_images += 1
            total_local_images += len(local_imgs)
        
        if external_imgs:
            posts_with_external_images += 1
            total_external_images += len(external_imgs)
        
        # 檢查本地圖片是否存在
        for img_path in local_imgs:
            if not Path(img_path).exists():
                missing_images.append((md_file.name, img_path))
    
    # 檢查圖片目錄
    image_dirs = list(images_dir.glob('*'))
    image_dir_count = len([d for d in image_dirs if d.is_dir()])
    
    # 找出沒有對應文章的圖片目錄
    post_ids = {extract_post_id(f.name) for f in posts_dir.glob('*.md')}
    orphan_dirs = []
    for img_dir in images_dir.glob('*'):
        if img_dir.is_dir() and img_dir.name.isdigit() and len(img_dir.name) == 10:
            if img_dir.name not in post_ids:
                orphan_dirs.append(img_dir.name)
    
    # 輸出統計結果
    print(f"\n📊 統計摘要:")
    print(f"{'項目':<30} {'數量':>10}")
    print("-" * 42)
    print(f"{'總文章數':<30} {total_posts:>10}")
    print(f"{'圖片目錄數':<30} {image_dir_count:>10}")
    print(f"{'使用本地圖片的文章':<30} {posts_with_local_images:>10}")
    print(f"{'使用外部圖片的文章':<30} {posts_with_external_images:>10}")
    print(f"{'本地圖片引用總數':<30} {total_local_images:>10}")
    print(f"{'外部圖片引用總數':<30} {total_external_images:>10}")
    
    # 檢查缺失圖片
    print(f"\n🔍 檢查結果:")
    if missing_images:
        print(f"\n⚠️  發現 {len(missing_images)} 個缺失的本地圖片:")
        for post, img in missing_images[:10]:  # 只顯示前10個
            print(f"  - {post}: {img}")
        if len(missing_images) > 10:
            print(f"  ... 還有 {len(missing_images) - 10} 個")
    else:
        print("✅ 所有引用的本地圖片都已下載完成！")
    
    # 檢查孤立的圖片目錄
    if orphan_dirs:
        print(f"\n⚠️  發現 {len(orphan_dirs)} 個沒有對應文章的圖片目錄:")
        for dir_name in orphan_dirs:
            img_count = len(list((images_dir / dir_name).glob('*')))
            print(f"  - {dir_name} ({img_count} 個檔案)")
    
    # 統計圖片文件總數
    total_image_files = 0
    for img_dir in images_dir.glob('*'):
        if img_dir.is_dir():
            total_image_files += len(list(img_dir.glob('*')))
    
    print(f"\n📁 圖片檔案詳情:")
    print(f"{'圖片檔案總數':<30} {total_image_files:>10}")
    
    # 檢查是否有外部圖片未下載
    if total_external_images > 0:
        print(f"\n💡 提示:")
        print(f"  還有 {total_external_images} 個外部圖片引用未轉為本地")
        print(f"  分布在 {posts_with_external_images} 篇文章中")
    
    print("\n" + "=" * 80)
    
    # 返回檢查結果
    return {
        'total_posts': total_posts,
        'missing_images': len(missing_images),
        'external_images': total_external_images,
        'orphan_dirs': len(orphan_dirs)
    }

if __name__ == '__main__':
    results = main()
    
    # 根據結果設置退出碼
    if results['missing_images'] > 0:
        exit(1)
    else:
        exit(0)
