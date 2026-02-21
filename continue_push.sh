#!/bin/bash
# 小批次推送腳本 - 每批 20 個目錄

set -e

echo "🚀 繼續分批推送剩餘圖片"
echo "=================================="
echo ""

# 配置 Git
git config http.postBuffer 1048576000
git config http.lowSpeedLimit 0  
git config http.lowSpeedTime 999999

# 獲取所有目錄
cd assets/images
DIRS=($(ls -d */ 2>/dev/null | sort))
TOTAL=${#DIRS[@]}
cd ../..

echo "📊 總共有 $TOTAL 個圖片目錄"
echo ""

# 從第 301 個開始（批次 5），每批 20 個
BATCH_SIZE=20
START=300  # 0-based index for directory 301
BATCH_NUM=5

while [ $START -lt $TOTAL ]; do
    END=$((START + BATCH_SIZE))
    if [ $END -gt $TOTAL ]; then
        END=$TOTAL
    fi
    
    echo "📦 批次 $BATCH_NUM: 處理圖片目錄 $((START + 1))-$END / $TOTAL"
    
    # 添加這批目錄
    for ((i=START; i<END; i++)); do
        DIR="assets/images/${DIRS[$i]}"
        if [ -d "$DIR" ]; then
            git add "$DIR" 2>/dev/null || true
        fi
    done
    
    # 提交
    if git commit -m "Deploy: Images batch $BATCH_NUM (directories $((START + 1))-$END)" 2>/dev/null; then
        echo "✅ 提交完成"
        
        # 推送
        echo "🚀 推送批次 $BATCH_NUM..."
        if git push origin gh-pages 2>&1; then
            echo "✅ 批次 $BATCH_NUM 推送成功"
        else
            echo "❌ 批次 $BATCH_NUM 推送失敗，嘗試重試..."
            sleep 5
            if git push origin gh-pages 2>&1; then
                echo "✅ 批次 $BATCH_NUM 重試成功"
            else
                echo "❌ 批次 $BATCH_NUM 重試仍失敗，停止"
                exit 1
            fi
        fi
    else
        echo "⚠️  沒有新文件需要提交"
    fi
    
    echo ""
    START=$END
    BATCH_NUM=$((BATCH_NUM + 1))
    
    # 每 5 批休息一下
    if [ $((BATCH_NUM % 5)) -eq 0 ]; then
        echo "😴 休息 10 秒..."
        sleep 10
    fi
done

echo ""
echo "✅ 所有批次推送完成！"
echo "=================================="
echo ""
echo "🌐 請確認 GitHub Pages 設置:"
echo "   https://github.com/nobodyyu/kuni-blog/settings/pages"
echo ""
echo "🎉 網站應該在此處:"
echo "   https://nobodyyu.github.io/kuni-blog/"
