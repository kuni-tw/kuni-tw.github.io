#!/bin/bash
# 分批提交圖片 - 改良版
# 會先檢查大小，避免單次提交超過 GitHub 限制

set -e

echo "=========================================="
echo "圖片分批上傳腳本"
echo "=========================================="
echo ""

# 設定參數
MAX_BATCH_SIZE_MB=500  # 每批最大 500MB
GITHUB_LIMIT_MB=2000   # GitHub 推送限制約 2GB

# 檢查是否已連接遠端
if ! git remote get-url origin &> /dev/null; then
    echo "❌ 錯誤：尚未設定 GitHub 遠端倉庫"
    echo ""
    echo "請先執行："
    echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo "  git branch -M main"
    exit 1
fi

echo "✓ 遠端倉庫：$(git remote get-url origin)"
echo ""

# 獲取所有圖片目錄
IMAGE_DIRS=($(find assets/images -mindepth 1 -maxdepth 1 -type d | sort))
TOTAL_DIRS=${#IMAGE_DIRS[@]}

if [ $TOTAL_DIRS -eq 0 ]; then
    echo "❌ 沒有找到圖片目錄"
    exit 1
fi

echo "找到 $TOTAL_DIRS 個圖片目錄"
echo "=========================================="
echo ""

# 詢問要處理多少批
read -p "每批處理多少個目錄？(建議 50-100): " BATCH_SIZE
BATCH_SIZE=${BATCH_SIZE:-50}

BATCH_COUNT=$(( (TOTAL_DIRS + BATCH_SIZE - 1) / BATCH_SIZE ))

echo ""
echo "將分成 $BATCH_COUNT 批處理"
echo "每批約 $BATCH_SIZE 個目錄"
echo ""
read -p "是否繼續？(y/n): " continue
if [ "$continue" != "y" ]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "=========================================="
echo "開始處理..."
echo "=========================================="
echo ""

for (( batch=0; batch<$BATCH_COUNT; batch++ )); do
    start=$(( batch * BATCH_SIZE ))
    end=$(( start + BATCH_SIZE ))
    
    if [ $end -gt $TOTAL_DIRS ]; then
        end=$TOTAL_DIRS
    fi
    
    echo "=========================================="
    echo "批次 $((batch + 1))/$BATCH_COUNT"
    echo "目錄範圍: $((start + 1)) - $end"
    echo "=========================================="
    
    # 計算這批的大小
    batch_size=0
    batch_dirs=()
    
    for (( i=start; i<end; i++ )); do
        dir="${IMAGE_DIRS[$i]}"
        batch_dirs+=("$dir")
        
        # 計算目錄大小（MB）
        dir_size=$(du -sm "$dir" | cut -f1)
        batch_size=$((batch_size + dir_size))
    done
    
    echo "  這批總大小: ${batch_size}MB"
    
    if [ $batch_size -gt $MAX_BATCH_SIZE_MB ]; then
        echo "  ⚠️  警告：這批大小超過 ${MAX_BATCH_SIZE_MB}MB"
        read -p "  是否繼續？(y/n): " proceed
        if [ "$proceed" != "y" ]; then
            echo "  已跳過此批"
            continue
        fi
    fi
    
    # 添加檔案
    echo "  添加檔案到 Git..."
    for dir in "${batch_dirs[@]}"; do
        git add "$dir"
    done
    
    # 提交
    commit_msg="Add images batch $((batch + 1))/$BATCH_COUNT (${batch_size}MB, dirs $((start + 1))-$end)"
    git commit -m "$commit_msg"
    echo "  ✓ 已提交"
    
    # 詢問是否推送
    read -p "  是否立即推送到 GitHub？(y/n/a=全部自動): " push_choice
    
    if [ "$push_choice" = "y" ] || [ "$push_choice" = "a" ]; then
        echo "  推送中..."
        if git push origin main; then
            echo "  ✓ 推送成功"
        else
            echo "  ❌ 推送失敗"
            echo "  提交已保存在本地，稍後可重試推送"
            read -p "  是否繼續下一批？(y/n): " continue_next
            if [ "$continue_next" != "y" ]; then
                echo "已中止"
                exit 1
            fi
        fi
        
        # 如果選擇全部自動，後續都自動推送
        if [ "$push_choice" = "a" ]; then
            AUTO_PUSH=1
        fi
    else
        echo "  已跳過推送"
    fi
    
    echo ""
    
    # 短暫暫停避免 API 限制
    if [ $((batch + 1)) -lt $BATCH_COUNT ]; then
        sleep 2
    fi
done

echo "=========================================="
echo "✓ 所有批次處理完成！"
echo "=========================================="
echo ""

# 檢查是否還有未推送的提交
if [ -n "$(git log origin/main..HEAD 2>/dev/null)" ]; then
    echo "⚠️  還有 $(git log origin/main..HEAD --oneline | wc -l) 個提交尚未推送"
    echo ""
    read -p "是否現在推送所有剩餘提交？(y/n): " push_all
    if [ "$push_all" = "y" ]; then
        git push origin main
        echo "✓ 全部推送完成"
    else
        echo "提示：稍後可執行 'git push origin main' 推送"
    fi
fi

echo ""
echo "完成！"
