#!/usr/bin/env python3
"""
完整的下載完成度檢查報告
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
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return [], []
    
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
    print("📊 文章與圖片下載完整性檢查報告")
    print("=" * 80)
    print()
    
    # 統計資料
    total_posts = 0
    posts_with_local_images = 0
    posts_with_external_images = 0
    total_local_images = 0
    total_external_images = 0
    missing_images = []
    posts_without_images = []
    
    # 檢查所有文章
    print("正在檢查所有文章...")
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
        
        # 檢查是否沒有圖片
        if not local_imgs and not external_imgs:
            posts_without_images.append(md_file.name)
        
        # 檢查本地圖片是否存在
        for img_path in local_imgs:
            if not Path(img_path).exists():
                missing_images.append((md_file.name, img_path))
    
    # 檢查圖片目錄
    print("正在檢查圖片目錄...")
    image_dirs = list(images_dir.glob('*'))
    image_dir_count = len([d for d in image_dirs if d.is_dir()])
    
    # 統計圖片文件總數
    total_image_files = 0
    empty_dirs = []
    for img_dir in images_dir.glob('*'):
        if img_dir.is_dir():
            files = list(img_dir.glob('*'))
            file_count = len(files)
            total_image_files += file_count
            if file_count == 0:
                empty_dirs.append(img_dir.name)
    
    # 找出沒有對應文章的圖片目錄
    post_ids = {extract_post_id(f.name) for f in posts_dir.glob('*.md')}
    orphan_dirs = []
    for img_dir in images_dir.glob('*'):
        if img_dir.is_dir() and img_dir.name.isdigit() and len(img_dir.name) == 10:
            if img_dir.name not in post_ids:
                file_count = len(list(img_dir.glob('*')))
                orphan_dirs.append((img_dir.name, file_count))
    
    # 輸出統計結果
    print()
    print("=" * 80)
    print("📈 統計摘要")
    print("=" * 80)
    print()
    print(f"{'項目':<35} {'數量':>15}")
    print("-" * 52)
    print(f"{'Sitemap 總文章數':<35} {'1,189':>15}")
    print(f"{'已下載文章數':<35} {total_posts:>15,}")
    print(f"{'下載完成率':<35} {(total_posts/1189*100):>14.1f}%")
    print()
    print(f"{'圖片目錄數':<35} {image_dir_count:>15,}")
    print(f"{'圖片檔案總數':<35} {total_image_files:>15,}")
    print()
    print(f"{'使用本地圖片的文章':<35} {posts_with_local_images:>15,}")
    print(f"{'使用外部圖片的文章':<35} {posts_with_external_images:>15,}")
    print(f"{'沒有圖片的文章':<35} {len(posts_without_images):>15,}")
    print()
    print(f"{'本地圖片引用總數':<35} {total_local_images:>15,}")
    print(f"{'外部圖片引用總數':<35} {total_external_images:>15,}")
    
    # 檢查結果
    print()
    print("=" * 80)
    print("🔍 檢查結果")
    print("=" * 80)
    print()
    
    # 下載完成度
    if total_posts >= 1189:
        print("✅ 所有文章已下載完成！")
    else:
        missing_count = 1189 - total_posts
        print(f"⚠️  還有 {missing_count} 篇文章未下載 (目標: 1,189 篇)")
    
    # 缺失圖片
    print()
    if missing_images:
        print(f"❌ 發現 {len(missing_images)} 個缺失的本地圖片:")
        for post, img in missing_images[:10]:
            print(f"   - {post}: {img}")
        if len(missing_images) > 10:
            print(f"   ... 還有 {len(missing_images) - 10} 個")
    else:
        print("✅ 所有引用的本地圖片都已下載完成！")
    
    # 外部圖片
    print()
    if total_external_images > 0:
        print(f"💡 還有 {total_external_images} 個外部圖片引用未轉為本地")
        print(f"   分布在 {posts_with_external_images} 篇文章中")
        print(f"   執行以下命令查看詳情: python3 check_external_images.py")
    else:
        print("✅ 沒有外部圖片引用")
    
    # 空目錄
    print()
    if empty_dirs:
        print(f"⚠️  發現 {len(empty_dirs)} 個空的圖片目錄:")
        for dir_name in empty_dirs[:5]:
            print(f"   - {dir_name}")
        if len(empty_dirs) > 5:
            print(f"   ... 還有 {len(empty_dirs) - 5} 個")
    
    # 孤立目錄
    print()
    if orphan_dirs:
        print(f"⚠️  發現 {len(orphan_dirs)} 個沒有對應文章的圖片目錄:")
        for dir_name, file_count in orphan_dirs[:5]:
            print(f"   - {dir_name} ({file_count} 個檔案)")
        if len(orphan_dirs) > 5:
            print(f"   ... 還有 {len(orphan_dirs) - 5} 個")
    
    # 沒有圖片的文章
    if len(posts_without_images) > 0:
        print()
        print(f"ℹ️  有 {len(posts_without_images)} 篇文章沒有圖片")
    
    print()
    print("=" * 80)
    
    # 總結
    if total_posts >= 1189 and len(missing_images) == 0:
        print("🎉 恭喜！所有文章和圖片都已下載完成！")
    elif total_posts >= 1189:
        print("⚠️  文章已全部下載，但有部分圖片缺失")
    else:
        print("⏳ 下載仍在進行中...")
    
    print("=" * 80)
    
    return {
        'total_posts': total_posts,
        'missing_images': len(missing_images),
        'external_images': total_external_images,
        'orphan_dirs': len(orphan_dirs),
        'complete': total_posts >= 1189 and len(missing_images) == 0
    }

if __name__ == '__main__':
    results = main()
    exit(0 if results['complete'] else 1)
