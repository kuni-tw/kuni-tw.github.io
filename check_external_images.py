#!/usr/bin/env python3
"""
列出仍使用外部圖片的文章
"""

import os
import re
from pathlib import Path

def check_images_in_markdown(md_file):
    """檢查 markdown 文章中的圖片引用"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有圖片引用
    markdown_images = re.findall(r'!\[.*?\]\((.*?)\)', content)
    html_images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    
    all_images = markdown_images + html_images
    
    # 找出外部圖片
    external_images = []
    for img in all_images:
        if img.startswith('http://') or img.startswith('https://'):
            external_images.append(img)
    
    return external_images

def main():
    posts_dir = Path('_posts')
    
    print("仍使用外部圖片的文章:")
    print("=" * 80)
    
    for md_file in sorted(posts_dir.glob('*.md')):
        external_imgs = check_images_in_markdown(md_file)
        
        if external_imgs:
            print(f"\n📄 {md_file.name}")
            for idx, img in enumerate(external_imgs, 1):
                print(f"   {idx}. {img}")

if __name__ == '__main__':
    main()
