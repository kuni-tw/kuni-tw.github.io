# 圖片上傳完成指南

## ✅ 已完成

1. ✅ GitHub 倉庫已創建：https://github.com/nobodyyu/kuni-blog
2. ✅ 網站框架已推送（1,189 篇文章）
3. ✅ Git 遠端已設定

## 📊 當前狀態

- **倉庫地址**：https://github.com/nobodyyu/kuni-blog
- **已上傳**：網站框架 + 所有文章（2.74 MB）
- **待上傳**：582 個圖片目錄（約 15GB）

## 🚀 下一步：上傳圖片

### 方法 1：手動批次上傳（推薦）

在終端執行以下命令，分批上傳圖片：

```bash
cd /Users/aki_yu/Downloads/kuni

# 設定每批數量
BATCH_SIZE=50

# 獲取所有圖片目錄
IMAGE_DIRS=($(find assets/images -mindepth 1 -maxdepth 1 -type d | sort))
TOTAL=${#IMAGE_DIRS[@]}

# 計算批次數
BATCHES=$(( (TOTAL + BATCH_SIZE - 1) / BATCH_SIZE ))

echo "總目錄數: $TOTAL"
echo "將分成 $BATCHES 批"

# 開始第一批（可以多次執行此區塊）
BATCH=0
START=$(( BATCH * BATCH_SIZE ))
END=$(( START + BATCH_SIZE ))
if [ $END -gt $TOTAL ]; then END=$TOTAL; fi

echo "處理批次 $((BATCH + 1))/$BATCHES (目錄 $((START + 1))-$END)"

# 添加這批目錄
for (( i=START; i<END; i++ )); do
    git add "${IMAGE_DIRS[$i]}"
done

# 提交並推送
git commit -m "Add images batch $((BATCH + 1))/$BATCHES"
git push origin main
```

**繼續下一批：** 修改 `BATCH=0` 為 `BATCH=1`, `BATCH=2`... 依次執行

### 方法 2：使用循環自動上傳

```bash
cd /Users/aki_yu/Downloads/kuni

for BATCH in {0..11}; do
    echo "==== 批次 $((BATCH + 1))/12 ===="
    
    START=$(( BATCH * 50 ))
    END=$(( START + 50 ))
    
    IMAGE_DIRS=($(find assets/images -mindepth 1 -maxdepth 1 -type d | sort))
    TOTAL=${#IMAGE_DIRS[@]}
    
    if [ $END -gt $TOTAL ]; then END=$TOTAL; fi
    if [ $START -ge $TOTAL ]; then break; fi
    
    for (( i=START; i<END; i++ )); do
        git add "${IMAGE_DIRS[$i]}"
    done
    
    git commit -m "Add images batch $((BATCH + 1))"
    git push origin main
    
    sleep 3
done

echo "完成！"
```

### 方法 3：檢查進度並繼續

查看還有多少圖片目錄未上傳：

```bash
cd /Users/aki_yu/Downloads/kuni
git status --short | grep "^??" | grep "assets/images" | wc -l
```

## 🌐 GitHub Pages 設定

在上傳圖片的同時或之後，請前往：

1. **https://github.com/nobodyyu/kuni-blog/settings/pages**
2. Source 選擇：**GitHub Actions**
3. 點擊建議的 **Jekyll** workflow 並提交

網站將發布到：  
**https://nobodyyu.github.io/kuni-blog/**

## ⏱️ 預計時間

- 每批約 1-2 分鐘（取決於大小和網速）
- 總共 12 批
- 總時間：約 20-30 分鐘

## 💡 提示

- 可以隨時按 Ctrl+C 中斷，稍後繼續
- Git 會記住已上傳的內容，不會重複
- 推送失敗可以重試：`git push origin main`
