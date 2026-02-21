#!/bin/bash
# 替換所有 HTML 文件中的圖片連結為 GitHub raw URL

set -e

echo "🔄 開始替換圖片連結..."
echo "=================================="
echo ""

# GitHub raw URL 前綴
GITHUB_RAW_URL="https://raw.githubusercontent.com/kuni-tw/images/www"

# 統計
TOTAL_FILES=0
TOTAL_REPLACEMENTS=0

# 查找所有年份目錄下的 HTML 文件
for year in 20{07..25}; do
    if [ -d "$year" ]; then
        echo "📁 處理 $year 年的文章..."
        
        # 查找該年份的所有 HTML 文件
        FILES=$(find "$year" -name "index.html" -type f 2>/dev/null || true)
        
        for file in $FILES; do
            if [ -f "$file" ]; then
                # 檢查文件是否包含需要替換的圖片連結
                if grep -q 'src="/assets/images/' "$file" 2>/dev/null; then
                    # 計算替換次數
                    COUNT=$(grep -o 'src="/assets/images/' "$file" | wc -l | tr -d ' ')
                    
                    # 使用 sed 替換（macOS 兼容版本）
                    sed -i '' "s|src=\"/assets/images/|src=\"${GITHUB_RAW_URL}/assets/images/|g" "$file"
                    
                    TOTAL_FILES=$((TOTAL_FILES + 1))
                    TOTAL_REPLACEMENTS=$((TOTAL_REPLACEMENTS + COUNT))
                    
                    if [ $((TOTAL_FILES % 50)) -eq 0 ]; then
                        echo "   已處理 $TOTAL_FILES 個文件，替換 $TOTAL_REPLACEMENTS 處..."
                    fi
                fi
            fi
        done
    fi
done

# 處理首頁和其他頂層 HTML 文件
echo "📄 處理頂層 HTML 文件..."
for file in *.html; do
    if [ -f "$file" ]; then
        if grep -q 'src="/assets/images/' "$file" 2>/dev/null; then
            COUNT=$(grep -o 'src="/assets/images/' "$file" | wc -l | tr -d ' ')
            sed -i '' "s|src=\"/assets/images/|src=\"${GITHUB_RAW_URL}/assets/images/|g" "$file"
            TOTAL_FILES=$((TOTAL_FILES + 1))
            TOTAL_REPLACEMENTS=$((TOTAL_REPLACEMENTS + COUNT))
        fi
    fi
done

echo ""
echo "✅ 替換完成！"
echo "=================================="
echo "📊 統計："
echo "   - 處理文件數：$TOTAL_FILES"
echo "   - 替換圖片數：$TOTAL_REPLACEMENTS"
echo ""
echo "🔍 驗證範例："
echo "--------------------------------"
# 隨機選一個文件驗證
SAMPLE_FILE=$(find 2017 -name "index.html" -type f 2>/dev/null | head -1)
if [ -n "$SAMPLE_FILE" ]; then
    echo "文件：$SAMPLE_FILE"
    echo "圖片連結範例："
    grep -o "src=\"${GITHUB_RAW_URL}/assets/images/[^\"]*\"" "$SAMPLE_FILE" | head -3 || echo "（無圖片）"
fi
echo ""
