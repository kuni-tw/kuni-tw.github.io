# Git 分批上傳策略

## 問題
- **圖片總大小：** 15GB
- **圖片目錄數：** 582 個
- **GitHub 限制：** 倉庫建議 < 1GB，推送限制 < 2GB

## 建議方案

### 方案一：使用 Git LFS（推薦）
將圖片檔案使用 Git LFS 管理，可以將大檔案存儲在 GitHub LFS 中。

**優點：** 
- 圖片與程式碼在同一倉庫
- GitHub Pages 仍可正常使用

**缺點：**
- GitHub LFS 免費額度：1GB 儲存 + 1GB/月流量
- 超過需付費

### 方案二：分離圖片倉庫
將圖片放在獨立的倉庫或 GitHub Release 中。

**優點：**
- 主倉庫輕量
- 可使用多個免費帳號

**缺點：**
- 需要修改文章中的圖片連結

### 方案三：分批提交（臨時方案）
將 582 個圖片目錄分成多批提交。

**優點：**
- 簡單直接

**缺點：**
- 仍可能超過 GitHub 總大小限制
- 推送可能失敗

## 執行步驟

### 如果選擇方案一（Git LFS）：

```bash
# 1. 安裝 Git LFS
brew install git-lfs  # macOS
git lfs install

# 2. 追蹤圖片檔案
git lfs track "assets/images/**/*.jpg"
git lfs track "assets/images/**/*.png"
git lfs track "assets/images/**/*.gif"

# 3. 提交 .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking"

# 4. 正常提交
git add .
git commit -m "Initial commit with images"
```

### 如果選擇方案二（分離倉庫）：

見下方腳本 `migrate_images_to_release.sh`

### 如果選擇方案三（分批提交）：

見下方腳本 `batch_commit.sh`

## 建議
對於 15GB 的圖片，最實際的方案是：
1. **短期：** 先只上傳網站框架和文章（不含圖片）
2. **長期：** 將圖片遷移到 CDN 或圖床服務
