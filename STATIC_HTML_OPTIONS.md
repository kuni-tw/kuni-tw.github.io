# 純 HTML 靜態網站部署方案

## 問題分析

您想要純 HTML 靜態網站（不使用 GitHub Pages 自動構建），但遇到以下限制：

### 磁盤空間限制
- **可用空間**: 13GB
- **需要空間**: ~30GB
  - 源文件（Markdown + 圖片）: 15GB
  - 構建輸出（HTML + 圖片副本）: 15GB
- **結論**: 本地無法構建 ❌

---

##選方案

### 方案 A：使用 Netlify（推薦⭐⭐⭐⭐⭐）

**優點**：
- ✅ 完全免費（100GB 流量/月）
- ✅ 自動部署（Push 後自動構建）
- ✅ 純 HTML 輸出（不依賴運行時）
- ✅ CDN 加速（比 GitHub Pages 快）
- ✅ 無需本地構建（在雲端構建）

**操作步驟**：
1. 前往 https://www.netlify.com/
2. 使用 GitHub 賬號登入
3. 點擊 "Add new site" → "Import an existing project"
4. 選擇您的 `kuni-blog` 倉庫
5. 構建設置：
   ```
   Build command: bundle exec jekyll build
   Publish directory: _site
   ```
6. 點擊 "Deploy site"

**結果**：
- 自動獲得網址：`https://你的站點名.netlify.app`
- 每次 push 自動重新構建
- 完全是純 HTML（Jekyll 在 Netlify 雲端構建）

---

### 方案 B：清理磁盤空間後本地構建

**需要操作**：
1. 清理磁盤，至少釋放 20GB 空間
2. 本地構建：`bundle exec jekyll build`
3. 推送 `_site` 到 GitHub
4. 創建 `.nojekyll` 文件

**缺點**：
- ❌ 需要大量磁盤空間
- ❌ 更新麻煩（每次都要本地構建）
- ❌ 耗時較長（15GB 圖片複製）

---

### 方案 C：接受 GitHub Pages 自動構建（最簡單）

**說明**：
GitHub Pages 的 Jekyll 構建是在 GitHub 服務器上進行的，輸出也是純 HTML。
您訪問的網站 **已經是 HTML**，只是構建過程發生在雲端而非本地。

**優點**：
- ✅ 完全免費
- ✅ 零配置
- ✅ 自動部署
- ✅ 訪問時就是 HTML（瀏覽器收到的是 HTML，不是 Markdown）

**設置**：
1. 前往 https://github.com/nobodyyu/kuni-blog/settings/pages
2. Source: `Deploy from a branch`
3. Branch: `main` / Folder: `/(root)`
4. 點擊 Save

**重要澄清**：
- "不依賴 GitHub Pages build" 和 "純 HTML" 並不矛盾
- GitHub Pages 構建後輸出的就是純 HTML
- 用戶訪問時看到的是靜態 HTML 文件，不是即時編譯

---

### 方案 D：使用 gh-pages 分支 + GitHub Actions

在 GitHub Actions 中構建（雲端有足夠空間），然後部署到 gh-pages 分支。

**GitHub Actions 配置**（`.github/workflows/deploy.yml`）：
```yaml
name: Build and Deploy
on:
  push:
    branches: [main]

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true
      
      - name: Build
        run: bundle exec jekyll build
      
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_site
```

**GitHub Pages 設置**：
- Source: `Deploy from a branch`
- Branch: `gh-pages`

**優點**：
- ✅ 純 HTML（`gh-pages` 分支只有 HTML）
- ✅ 不依賴 GitHub Pages 的 Jekyll（自己在 Actions 中構建）
- ✅ 自動部署

**缺點**：
- ⚠️ 仍然使用了 GitHub 的構建服務（只是換成 Actions）

---

## 推薦決策樹

```
是否介意使用雲端構建服務？
├─ 是 → 方案 B（本地構建，需清理磁盤）
└─ 否 → 
    ├─ 想要最簡單 → 方案 C（GitHub Pages 自動構建）
    ├─ 想要最快速度 → 方案 A（Netlify）
    └─ 想要完全控制 → 方案 D（GitHub Actions）
```

---

## 我的建議

**選擇方案 A（Netlify）**，理由：
1. 完全滿足您的需求（純 HTML，不依賴運行時）
2. 比 GitHub Pages 更快（全球 CDN）
3. 零成本零配置
4. 支持自定義域名
5. 構建日誌更詳細

**或選擇方案 C（GitHub Pages）**，如果：
- 您理解"雲端構建但輸出純 HTML"這個概念
- 想要最省事的方案

---

## 下一步

請告訴我您選擇哪個方案，我會協助您完成設置！
