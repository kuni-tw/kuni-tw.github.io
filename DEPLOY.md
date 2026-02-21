# KUNI Blog 部署指南

## 步驟 1: 執行爬蟲抓取文章

首先安裝 Python 依賴：

```bash
pip install -r requirements.txt
```

執行爬蟲腳本：

```bash
python scraper.py
```

這將會：
- 抓取所有文章和圖片
- 轉換為 Jekyll Markdown 格式
- 儲存在 `_posts/` 目錄
- 下載圖片到 `assets/images/` 目錄

## 步驟 2: 初始化 Git Repository

```bash
git init
git add .
git commit -m "Initial commit: Add blog content"
```

## 步驟 3: 推送到 GitHub

在 GitHub 上建立新的 repository，然後：

```bash
git remote add origin https://github.com/你的用戶名/你的倉庫名.git
git branch -M main
git push -u origin main
```

## 步驟 4: 啟用 GitHub Pages

1. 前往你的 GitHub repository
2. 點擊 Settings > Pages
3. 在 "Source" 下選擇 "GitHub Actions"
4. GitHub Actions 會自動部署你的網站

## 步驟 5: 訪問你的網站

幾分鐘後，你的網站將可以在以下網址訪問：
```
https://你的用戶名.github.io/你的倉庫名/
```

## 本地預覽（可選）

如果你想在本地預覽網站，需要安裝 Ruby 和 Jekyll：

```bash
# 安裝依賴
bundle install

# 啟動本地伺服器
bundle exec jekyll serve
```

然後在瀏覽器訪問 `http://localhost:4000`

## 自訂設定

編輯 `_config.yml` 來修改：
- 網站標題
- 描述
- 主題設定
- 等等

## 故障排除

### 爬蟲問題
- 如果某些文章抓取失敗，檢查網路連線
- 確認 PIXNET 網站結構是否改變

### GitHub Pages 部署問題
- 檢查 GitHub Actions 的執行日誌
- 確認 `_config.yml` 設定正確
- 確保所有圖片路徑正確

## 更新內容

當你想要更新網站內容時：

```bash
# 修改文章或添加新文章
git add .
git commit -m "Update content"
git push
```

GitHub Actions 會自動重新部署。
