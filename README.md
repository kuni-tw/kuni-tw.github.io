# KUNI Blog Archive

這個專案用於從 PIXNET 部落格抓取文章和圖片，並轉換為 GitHub Pages 格式。

## 使用方法

1. 安裝依賴：
```bash
pip install -r requirements.txt
```

2. 執行抓取腳本：
```bash
python scraper.py
```

3. 部署到 GitHub Pages：
   - 將此 repository push 到 GitHub
   - 在 repository 設定中啟用 GitHub Pages
   - 選擇 main 分支作為來源

## 目錄結構

- `scraper.py` - 主要的爬蟲腳本
- `_posts/` - 文章目錄（Markdown 格式）
- `assets/images/` - 圖片目錄
- `_config.yml` - Jekyll 配置文件
