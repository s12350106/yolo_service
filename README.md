# YOLOv8 物件偵測服務

透過 FastAPI + Ultralytics YOLOv8 建立的圖片物件偵測 API，支援非同步任務佇列。

---

## 功能

* 上傳圖片，返回任務 ID
* 透過任務 ID 查詢辨識結果
* **🆕 返回帶有檢測框的圖片**
* 支援 CPU/GPU 推論
* Docker 容器化部署
* 可搭配 ngrok 讓手機 APP 呼叫外網 API

---

## 快速使用

1. **Clone 專案**

```bash
git clone https://github.com/yijean333/yolo_service.git
cd yolo_service
```

2. **用 Docker 建置並執行**

```bash
docker build -t yolo_service .
docker run -p 8000:8000 yolo_service
```

3. **用 ngrok 暴露服務**

```bash
ngrok config add-authtoken <你的-authtoken-字串> # 推薦但不必要
ngrok http http://localhost:8000
```

4. **API 簡介**

### 原有 API
* POST `/predict`：上傳圖片，回傳任務 ID（異步）
* GET `/task/{task_id}`：查詢辨識結果
* POST `/predict-sync`：上傳圖片，同步返回 JSON 檢測結果

### 🆕 新增圖片 API
* POST `/predict-image`：上傳圖片，**直接返回帶有檢測框的圖片**

更多 API 功能和詳細說明，請參考: `你的-ngrok網址/docs`

---

## API 使用範例

### 1. 獲取帶檢測框的圖片

```bash
# 上傳圖片，直接獲得帶框的圖片檔案
curl -X POST "http://localhost:8000/predict-image" \
     -H "accept: image/jpeg" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg" \
     --output detection_result.jpg
```

### 2. 使用 Python 測試

```python
import requests

# 測試帶框圖片 API
with open('test_image.jpg', 'rb') as f:
    files = {'file': ('test_image.jpg', f, 'image/jpeg')}
    response = requests.post('http://localhost:8000/predict-image', files=files)
    
    if response.status_code == 200:
        with open('result_with_boxes.jpg', 'wb') as output:
            output.write(response.content)
        print("帶檢測框的圖片已保存！")
```

---

## Android APP

APP 可以選擇使用不同的 API 端點：

1. **原有方式**：使用 `/predict` + `/task/{task_id}` 進行異步檢測
2. **🆕 新方式**：使用 `/predict-image` 直接獲取帶框圖片進行顯示

---

## 注意事項

* 請自行準備 `best.pt` 模型權重放到專案根目錄
* Docker 裡安裝的 PyTorch 與 torchvision 版本要配合
* 請替換 ngrok 網址為你自己產生的外網 URL
* 新的圖片 API 是同步處理，適合即時顯示結果
* 對於大量並發請求，建議仍使用原有的異步 API

---

## 測試腳本

使用提供的測試腳本來驗證所有 API 功能：

```bash
python3 test_image_api.py
```

