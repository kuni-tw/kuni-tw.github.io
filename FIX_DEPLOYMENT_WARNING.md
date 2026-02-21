# ⚠️ 解決部署警告

## 問題

```
Warning: Uploaded artifact size of 15547862477 bytes exceeds the allowed size of 1 GB. 
Deployment might fail.
```

這個警告表示您當前使用的是 **GitHub Actions** 部署模式，但您的網站內容（15.5GB）超過了 Actions 的 1GB 產物限制。

---

## ✅ 立即解決方法

### 步驟 1：進入設置頁面

https://github.com/nobodyyu/kuni-blog/settings/pages

### 步驟 2：修改 Source 設置

找到 **Source** 下拉選單：

❌ **目前可能是**：`GitHub Actions`  
✅ **請改為**：`Deploy from a branch`

### 步驟 3：設置分支

在 Source 改為 "Deploy from a branch" 後，會出現分支選項：

- **Branch**: `main`
- **Folder**: `/(root)`

### 步驟 4：保存

點擊 **Save** 按鈕

---

## 🎯 兩種模式對比

| 項目 | GitHub Actions | Deploy from a branch |
|------|----------------|---------------------|
| **構建產物限制** | 1GB ❌ | 無限制 ✅ |
| **您的網站大小** | 15.5GB (超過) | 15.5GB (沒問題) |
| **倉庫大小限制** | - | 100GB ✅ |
| **適合您嗎？** | ❌ 不適合 | ✅ 完美適合 |

---

## 📝 改完後會發生什麼？

1. **警告消失**：不再有 1GB 限制的警告
2. **自動構建**：GitHub Pages 直接從 main 分支構建
3. **正常部署**：約 1-2 分鐘後網站上線
4. **訪問網站**：https://nobodyyu.github.io/kuni-blog/

---

## 💡 補充說明

### 如果之前有 .github/workflows/ 文件

可以刪除或忽略，使用分支部署模式時不需要 workflow 文件。

### 為什麼分支模式沒有 1GB 限制？

- GitHub Actions 模式：需要將構建結果打包成「產物」上傳（限制 1GB）
- 分支部署模式：直接從倉庫分支讀取並構建（只受倉庫 100GB 限制）

您的 15.5GB 遠小於 100GB，完全沒問題！

---

## ⏰ 預期結果

改完設置後：
- ✅ 幾秒內：設置生效
- ✅ 1-2 分鐘：網站開始構建
- ✅ 完成後：可以訪問 https://nobodyyu.github.io/kuni-blog/
- ✅ 沒有警告：部署成功

---

**現在就去改設置吧！** 🚀
