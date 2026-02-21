#!/bin/bash
# 分批推送腳本 - 解決 GitHub 15GB 推送限制

set -e

echo "🚀 開始分批推送到 gh-pages 分支"
echo "=================================="
echo ""

# 配置 Git
git config http.postBuffer 1048576000
git config http.lowSpeedLimit 0  
git config http.lowSpeedTime 999999

# 第一批：添加基礎結構（HTML、XML、配置，排除 assets）
echo "📦 批次 1/6: 添加網站基礎結構..."
git add .nojekyll *.html *.xml *.md 20*/ build.log *.txt *.py *.sh venv/ 2>/dev/null || true
git commit -m "Deploy: Website structure and HTML files"
echo "🚀 推送批次 1..."
git push -f origin gh-pages || { echo "❌ 批次 1 推送失敗"; exit 1; }
echo "✅ 批次 1 完成"
echo ""

# 檢查 assets/images 中的子目錄數量
cd assets/images
DIRS=($(ls -d */ 2>/dev/null | sort))
TOTAL=${#DIRS[@]}
BATCH_SIZE=100

echo "📊 assets/images 中有 $TOTAL 個目錄"
echo "每批處理 $BATCH_SIZE 個目錄"
echo ""

# 返回到 _site 目錄
cd ../..

# 分批添加 assets/images 的子目錄
BATCH_NUM=2
START=0

while [ $START -lt $TOTAL ]; do
    END=$((START + BATCH_SIZE))
    if [ $END -gt $TOTAL ]; then
        END=$TOTAL
    fi
    
    echo "📦 批次 $BATCH_NUM/$(((TOTAL + BATCH_SIZE - 1) / BATCH_SIZE + 1)): 處理圖片目錄 $((START + 1))-$END / $TOTAL"
    
    # 添加這批目錄
    for ((i=START; i<END; i++)); do
        DIR="assets/images/${DIRS[$i]}"
        if [ -d "$DIR" ]; then
            git add "$DIR" 2>/dev/null || true
        fi
    done
    
    # 提交
    git commit -m "Deploy: Images batch $BATCH_NUM (directories $((START + 1))-$END)" || true
    
    # 推送
    echo "🚀 推送批次 $BATCH_NUM..."
    git push origin gh-pages || { echo "❌ 批次 $BATCH_NUM 推送失敗"; exit 1; }
    echo "✅ 批次 $BATCH_NUM 完成"
    echo ""
    
    START=$END
    BATCH_NUM=$((BATCH_NUM + 1))
done

# 檢查是否有其他 assets 文件需要添加
echo "📦 最後批次: 添加 assets 中的其他文件..."
git add assets/ 2>/dev/null || true
git commit -m "Deploy: Remaining assets files" || echo "沒有其他文件需要提交"
git push origin gh-pages || echo "沒有需要推送的內容"

echo ""
echo "✅ 所有批次推送完成！"
echo "=================================="
echo ""
echo "🌐 請前往 GitHub 設置 Pages:"
echo "   https://github.com/nobodyyu/kuni-blog/settings/pages"
echo ""
echo "   選擇:"
echo "   - Source: Deploy from a branch"
echo "   - Branch: gh-pages"
echo "   - Folder: /(root)"
echo ""
echo "🎉 網站將在此處上線:"
echo "   https://nobodyyu.github.io/kuni-blog/"
