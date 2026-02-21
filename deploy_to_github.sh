#!/bin/bash
# GitHub Pages 完整部署流程
# 包含創建倉庫、初次推送、分批上傳圖片

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║     GitHub Pages 部署助手                              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 步驟 1: 創建 GitHub 倉庫
echo "【步驟 1】創建 GitHub 倉庫"
echo "────────────────────────────────────────────────────────"
echo ""
echo "請先在瀏覽器中完成以下操作："
echo ""
echo "  1. 前往：https://github.com/new"
echo "  2. Repository name: kuni-blog (或您喜歡的名稱)"
echo "  3. 設為 Public (GitHub Pages 免費版需要公開倉庫)"
echo "  4. ❌ 不要勾選「Initialize this repository with...」"
echo "  5. 點擊「Create repository」"
echo ""
read -p "完成後按 Enter 繼續..."
echo ""

# 步驟 2: 設定遠端倉庫
echo "【步驟 2】設定遠端倉庫"
echo "────────────────────────────────────────────────────────"
echo ""

# 獲取使用者資訊
GIT_USERNAME=$(git config user.name || echo "")
if [ -z "$GIT_USERNAME" ]; then
    read -p "請輸入您的 GitHub 使用者名稱: " GITHUB_USER
else
    read -p "請輸入您的 GitHub 使用者名稱 [$GIT_USERNAME]: " GITHUB_USER
    GITHUB_USER=${GITHUB_USER:-$GIT_USERNAME}
fi

read -p "請輸入您的倉庫名稱 [kuni-blog]: " REPO_NAME
REPO_NAME=${REPO_NAME:-kuni-blog}

REPO_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo ""
echo "將設定遠端倉庫為：$REPO_URL"
read -p "確認無誤？(y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "設定遠端倉庫..."
git remote add origin "$REPO_URL"
git branch -M main

echo "✓ 遠端倉庫已設定"
echo ""

# 步驟 3: 推送網站框架
echo "【步驟 3】推送網站框架和文章"
echo "────────────────────────────────────────────────────────"
echo ""
echo "即將推送："
echo "  • 1,189 篇文章"
echo "  • 網站配置檔案"
echo "  • GitHub Actions 工作流程"
echo "  • 大小：約 5.6MB"
echo ""
read -p "是否推送？(y/n): " push_confirm
if [ "$push_confirm" != "y" ]; then
    echo "已取消 - 遠端倉庫已設定，可稍後手動執行：git push -u origin main"
    exit 0
fi

echo ""
echo "推送中..."
if git push -u origin main; then
    echo ""
    echo "✓ 網站框架推送成功！"
else
    echo ""
    echo "❌ 推送失敗"
    echo ""
    echo "常見問題："
    echo "  • 倉庫名稱或使用者名稱錯誤"
    echo "  • 需要身份驗證 (請使用 Personal Access Token)"
    echo ""
    echo "可以稍後手動執行：git push -u origin main"
    exit 1
fi

echo ""

# 步驟 4: 啟用 GitHub Pages
echo "【步驟 4】啟用 GitHub Pages"
echo "────────────────────────────────────────────────────────"
echo ""
echo "請在瀏覽器中完成以下操作："
echo ""
echo "  1. 前往：https://github.com/$GITHUB_USER/$REPO_NAME/settings/pages"
echo "  2. 在「Build and deployment」下："
echo "     Source: 選擇「GitHub Actions」"
echo "  3. 等待 2-3 分鐘讓 GitHub Actions 建置網站"
echo ""
echo "網站將發布到："
echo "  🌐 https://$GITHUB_USER.github.io/$REPO_NAME/"
echo ""
read -p "完成後按 Enter 繼續..."
echo ""

# 步驟 5: 詢問是否上傳圖片
echo "【步驟 5】上傳圖片"
echo "────────────────────────────────────────────────────────"
echo ""
echo "圖片統計："
echo "  • 目錄數：582 個"
echo "  • 檔案數：9,471 個"
echo "  • 總大小：15GB"
echo ""
echo "⚠️  注意：15GB 圖片需要分批上傳"
echo ""
echo "選項："
echo "  1) 現在開始分批上傳圖片"
echo "  2) 稍後手動上傳（執行 ./upload_images.sh）"
echo "  3) 跳過圖片上傳"
echo ""
read -p "請選擇 (1/2/3): " upload_choice

case $upload_choice in
    1)
        echo ""
        echo "啟動圖片上傳腳本..."
        sleep 2
        exec ./upload_images.sh
        ;;
    2)
        echo ""
        echo "稍後可執行以下命令上傳圖片："
        echo "  ./upload_images.sh"
        ;;
    3)
        echo ""
        echo "已跳過圖片上傳"
        ;;
    *)
        echo "無效選擇，已跳過圖片上傳"
        ;;
esac

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║     🎉 部署完成！                                      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "您的網站："
echo "  🌐 https://$GITHUB_USER.github.io/$REPO_NAME/"
echo ""
echo "下一步："
echo "  • 訪問網站確認文章可以正常顯示"
echo "  • 如果尚未上傳圖片，執行：./upload_images.sh"
echo ""
