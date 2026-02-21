# 📦 GitHub Pages 部署指南

## ✅ 已完成

1. ✅ Git 倉庫已初始化
2. ✅ 網站框架和 1,189 篇文章已提交
3. ✅ GitHub Actions 工作流程已設置
4. ✅ .gitignore 已配置

**目前狀態：** 網站框架已準備就緒（5.5MB），圖片待處理（15GB）

---

## 📋 部署步驟

### 步驟 1：在 GitHub 創建倉庫

1. 前往 GitHub：https://github.com/new
2. 輸入倉庫名稱（建議：`blog` 或 `kuni-blog`）
3. 選擇 **Public**（GitHub Pages 免費版需要公開倉庫）
4. **不要**勾選「Initialize this repository with a README」
5. 點擊「Create repository」

### 步驟 2：連接遠端倉庫並推送

```bash
# 設置遠端倉庫（替換成您的 GitHub 使用者名稱和倉庫名稱）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 確認設置
git remote -v

# 推送第一次提交（網站框架 + 文章）
git push -u origin main
```

### 步驟 3：啟用 GitHub Pages

1. 前往倉庫的 **Settings** > **Pages**
2. 在「Build and deployment」下：
   - Source: 選擇「GitHub Actions」
3. GitHub Actions 會自動偵測到 `.github/workflows/jekyll.yml` 並開始建置
4. 等待 2-3 分鐘，網站會發布到：
   - `https://YOUR_USERNAME.github.io/YOUR_REPO/`

### 步驟 4：處理圖片（15GB）

⚠️ **重要：** GitHub 有以下限制：
- 單個檔案 < 100MB
- 倉庫建議 < 1GB
- 推送大小 < 2GB

**選項 A：分批上傳圖片（需多次推送）**

```bash
# 使用提供的腳本分批上傳
./upload_images.sh

# 按照提示操作，每批約 50-100 個目錄
# 總共需要約 6-12 批
```

**選項 B：使用 Git LFS（建議，但有配額限制）**

```bash
# 1. 安裝 Git LFS
brew install git-lfs
git lfs install

# 2. 追蹤圖片檔案
git lfs track "assets/images/**/*.jpg"
git lfs track "assets/images/**/*.png"
git lfs track "assets/images/**/*.gif"

# 3. 添加和提交
git add .gitattributes
git commit -m "Setup Git LFS for images"

# 4. 取消圖片的 gitignore
# 編輯 .gitignore，將 # assets/images/ 這行刪除

# 5. 添加所有圖片
git add assets/images/
git commit -m "Add all images via Git LFS"

# 6. 推送
git push origin main
```

**注意：** GitHub LFS 免費額度：
- 儲存空間：1GB
- 每月流量：1GB

15GB 圖片會超出免費額度，需要付費或考慮其他方案。

**選項 C：使用外部圖床（推薦長期方案）**

將圖片上傳到：
- Cloudflare R2（免費 10GB）
- Imgur
- GitHub Release
- 其他 CDN 服務

然後批次修改文章中的圖片連結。

---

## 🔍 驗證部署

部署完成後：

1. 訪問您的網站：`https://YOUR_USERNAME.github.io/YOUR_REPO/`
2. 檢查文章是否正常顯示
3. 檢查圖片載入狀況

---

## 📝 後續維護

### 添加新文章

```bash
# 1. 將新文章放到 _posts/ 目錄
# 2. 添加並提交
git add _posts/新文章.md
git commit -m "Add new post: 文章標題"

# 3. 推送
git push origin main

# GitHub Actions 會自動重新建置網站
```

### 本地預覽

```bash
# 安裝依賴
bundle install

# 啟動本地伺服器
bundle exec jekyll serve

# 訪問 http://localhost:4000
```

---

## 🛠️ 檔案清單

已建立的輔助腳本：

- `upload_images.sh` - 分批上傳圖片腳本
- `batch_commit.sh` - 簡易批次提交腳本
- `GIT_UPLOAD_STRATEGY.md` - 詳細上傳策略說明

---

## ⚠️ 常見問題

### Q: 推送時出現「file size exceeds 100 MB」錯誤

A: GitHub 不接受超過 100MB 的單個檔案。檢查並刪除或使用 Git LFS。

### Q: 推送太慢或失敗

A: 15GB 太大，建議使用 `upload_images.sh` 分批上傳，每批 500MB 左右。

### Q: GitHub Pages 顯示 404

A: 
1. 確認已在 Settings > Pages 啟用
2. 檢查 GitHub Actions 是否成功執行
3. 等待幾分鐘讓 DNS 生效

### Q: 圖片無法顯示

A: 
1. 如果還沒上傳圖片，文章中的圖片會暫時無法顯示
2. 上傳圖片後會自動修復

---

## 🎯 建議的工作流程

### 立即執行（今天）

1. ✅ 創建 GitHub 倉庫
2. ✅ 推送網站框架和文章
3. ✅ 驗證網站可以訪問

### 短期（本週）

4. 決定圖片處理方案：
   - 如果願意付費：使用 Git LFS
   - 如果要免費：使用外部圖床或分批上傳
5. 開始處理圖片

### 長期（未來）

6. 設定自動備份
7. 優化圖片大小（壓縮）
8. 考慮使用 CDN 加速

---

## 📞 需要幫助？

執行以下命令查看當前狀態：

```bash
# 查看 Git 狀態
git status

# 查看遠端倉庫
git remote -v

# 查看提交歷史
git log --oneline

# 查看倉庫大小
du -sh .git
```
