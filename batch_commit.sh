#!/bin/bash
# 分批提交圖片到 Git
# 用法: ./batch_commit.sh

set -e

BATCH_SIZE=50  # 每批處理 50 個目錄
IMAGE_DIRS=($(ls -1d assets/images/*/ 2>/dev/null | sort))
TOTAL_DIRS=${#IMAGE_DIRS[@]}

if [ $TOTAL_DIRS -eq 0 ]; then
    echo "沒有找到圖片目錄"
    exit 1
fi

echo "=========================================="
echo "分批提交圖片目錄"
echo "=========================================="
echo "總目錄數: $TOTAL_DIRS"
echo "每批數量: $BATCH_SIZE"
echo "批次總數: $(( (TOTAL_DIRS + BATCH_SIZE - 1) / BATCH_SIZE ))"
echo "=========================================="
echo ""

# 計算需要多少批次
BATCH_COUNT=$(( (TOTAL_DIRS + BATCH_SIZE - 1) / BATCH_SIZE ))

for (( batch=0; batch<$BATCH_COUNT; batch++ )); do
    start=$(( batch * BATCH_SIZE ))
    end=$(( start + BATCH_SIZE ))
    
    if [ $end -gt $TOTAL_DIRS ]; then
        end=$TOTAL_DIRS
    fi
    
    echo "=========================================="
    echo "處理批次 $((batch + 1))/$BATCH_COUNT"
    echo "目錄範圍: $((start + 1)) - $end"
    echo "=========================================="
    
    # 添加這批目錄
    for (( i=start; i<end; i++ )); do
        dir="${IMAGE_DIRS[$i]}"
        echo "  添加: $dir"
        git add "$dir"
    done
    
    # 提交
    commit_msg="Add images batch $((batch + 1))/$BATCH_COUNT (dirs $((start + 1))-$end)"
    git commit -m "$commit_msg"
    
    echo "  ✓ 已提交批次 $((batch + 1))"
    echo ""
    
    # 詢問是否立即推送
    read -p "是否立即推送此批次到 GitHub? (y/n): " push_now
    if [ "$push_now" = "y" ] || [ "$push_now" = "Y" ]; then
        echo "  推送中..."
        git push origin main
        echo "  ✓ 推送完成"
    fi
    
    echo ""
done

echo "=========================================="
echo "✓ 所有批次處理完成！"
echo "=========================================="
