# GitHub Pages 設置指南

## 問題
構建產物 15.5GB 超過 GitHub Actions 的 1GB 限制，導致部署失敗。

## 解決方案
使用「分支部署」模式，不使用 GitHub Actions。

## 設置步驟

### 1. 進入設置頁面
https://github.com/nobodyyu/kuni-blog/settings/pages

### 2. Source 設置
選擇：**Deploy from a branch**

⚠️ **不要選** "GitHub Actions"

### 3. Branch 設置
- Branch: **main**
- Folder: **/(root)**

### 4. 保存
點擊 **Save** 按鈕

### 5. 等待部署
等待 1-2 分鐘後即可訪問

## 完成後訪問

https://nobodyyu.github.io/kuni-blog/

## 為什麼這樣可行？

- ✅ GitHub Pages 可以直接從分支提供靜態文件
- ✅ Jekyll 網站會自動構建（GitHub 內建支援）
- ✅ 沒有 1GB 構建產物限制
- ✅ 倉庫總大小限制是 100GB（您的 15GB 完全沒問題）
- ✅ 不需要 GitHub Actions workflow

## 注意事項

如果您已經配置了 GitHub Actions：
- 可以忽略那個警告
- 或者停用 Actions 部署，改用分支部署（按照上面步驟）

分支部署更簡單，也更適合大型靜態網站！
