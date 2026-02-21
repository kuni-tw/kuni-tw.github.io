#!/usr/bin/env python3
"""
等待下載完成並執行完整檢查
"""

import time
import subprocess
from pathlib import Path

def count_posts():
    """統計文章數"""
    posts_dir = Path('_posts')
    return len(list(posts_dir.glob('*.md')))

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
                return True
        return False
    except:
        return False

def wait_for_completion():
    """等待下載完成"""
    target = 1189
    print("等待下載完成...")
    print("按 Ctrl+C 可以中斷等待\n")
    
    last_count = 0
    no_change_count = 0
    
    while True:
        current_count = count_posts()
        is_running = check_process()
        
        # 顯示進度
        progress = (current_count / target) * 100
        print(f"\r當前: {current_count}/{target} 篇 ({progress:.1f}%) | 進程: {'運行中' if is_running else '已停止'}", end='', flush=True)
        
        # 檢查是否完成
        if current_count >= target:
            print("\n\n✅ 已達到目標文章數！")
            break
        
        # 檢查進程是否停止
        if not is_running:
            # 如果數量沒有變化，確認已停止
            if current_count == last_count:
                no_change_count += 1
                if no_change_count >= 3:  # 連續3次檢查沒有變化
                    print(f"\n\n⚠️  下載進程已停止，但尚未完成 (差 {target - current_count} 篇)")
                    break
            else:
                no_change_count = 0
        
        last_count = current_count
        time.sleep(5)  # 每5秒檢查一次
    
    return current_count

def run_final_check():
    """執行完整檢查"""
    print("\n" + "=" * 80)
    print("執行完整檢查...")
    print("=" * 80 + "\n")
    
    # 執行完整性檢查
    subprocess.run(['python3', 'check_completeness.py'])
    
    print("\n" + "=" * 80)
    print("檢查外部圖片...")
    print("=" * 80 + "\n")
    
    # 檢查外部圖片
    subprocess.run(['python3', 'check_external_images.py'])

def main():
    try:
        final_count = wait_for_completion()
        print("\n")
        
        # 執行完整檢查
        run_final_check()
        
        print("\n" + "=" * 80)
        print("✅ 所有檢查完成！")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n已中斷！")
        print("可以手動執行以下命令進行檢查:")
        print("  python3 check_completeness.py")
        print("  python3 check_external_images.py")

if __name__ == '__main__':
    main()
