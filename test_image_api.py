#!/usr/bin/env python3
"""
測試新的圖片 API 端點的示例腳本
"""

import requests
import base64
from io import BytesIO
from PIL import Image

def test_predict_image_api(image_path, server_url="http://localhost:8000"):
    """
    測試 /predict-image API - 返回帶檢測框的圖片
    """
    print(f"測試 /predict-image API...")
    
    with open(image_path, 'rb') as f:
        files = {'file': (image_path, f, 'image/jpeg')}
        response = requests.post(f"{server_url}/predict-image", files=files)
    
    if response.status_code == 200:
        # 保存返回的圖片
        output_path = "detection_result.jpg"
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ 成功！帶檢測框的圖片已保存到: {output_path}")
        return True
    else:
        print(f"❌ 失敗: {response.status_code} - {response.text}")
        return False

def test_predict_image_with_json_api(image_path, server_url="http://localhost:8000"):
    """
    測試 /predict-image-with-json API - 返回 JSON 和 base64 圖片
    """
    print(f"測試 /predict-image-with-json API...")
    
    with open(image_path, 'rb') as f:
        files = {'file': (image_path, f, 'image/jpeg')}
        response = requests.post(f"{server_url}/predict-image-with-json", files=files)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 成功！檢測到 {len(result['detections'])} 個物體")
        
        # 解碼並保存 base64 圖片
        base64_data = result['image_with_boxes_base64'].split(',')[1]  # 移除 "data:image/jpeg;base64," 前綴
        image_data = base64.b64decode(base64_data)
        
        output_path = "detection_result_from_json.jpg"
        with open(output_path, 'wb') as f:
            f.write(image_data)
        print(f"✅ 帶檢測框的圖片已保存到: {output_path}")
        
        # 顯示檢測結果
        for i, detection in enumerate(result['detections']):
            print(f"  物體 {i+1}: {detection['label']} (信心度: {detection['confidence']:.2f})")
        
        return True
    else:
        print(f"❌ 失敗: {response.status_code} - {response.text}")
        return False

def test_original_api(image_path, server_url="http://localhost:8000"):
    """
    測試原來的 /predict-sync API - 只返回 JSON
    """
    print(f"測試原來的 /predict-sync API...")
    
    with open(image_path, 'rb') as f:
        files = {'file': (image_path, f, 'image/jpeg')}
        response = requests.post(f"{server_url}/predict-sync", files=files)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 成功！檢測到 {len(result['detections'])} 個物體")
        
        # 顯示檢測結果
        for i, detection in enumerate(result['detections']):
            print(f"  物體 {i+1}: {detection['label']} (信心度: {detection['confidence']:.2f})")
        
        return True
    else:
        print(f"❌ 失敗: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    # 使用說明
    print("=" * 60)
    print("YOLOv8 API 測試腳本")
    print("=" * 60)
    print()
    print("使用方法:")
    print("1. 確保 FastAPI 服務正在運行 (python3 app_queue.py)")
    print("2. 準備一張測試圖片")
    print("3. 運行此腳本: python3 test_image_api.py")
    print()
    print("新增的 API 端點:")
    print("- POST /predict-image")
    print("  返回: 帶有檢測框的圖片 (image/jpeg)")
    print()
    print("- POST /predict-image-with-json") 
    print("  返回: JSON 格式的檢測結果 + base64 編碼的帶框圖片")
    print()
    print("原有的 API 端點:")
    print("- POST /predict-sync")
    print("  返回: JSON 格式的檢測結果")
    print()
    
    # 如果有測試圖片，可以取消註解以下行進行測試
    # image_path = "test_image.jpg"  # 替換為您的測試圖片路徑
    # test_original_api(image_path)
    # test_predict_image_api(image_path)
    # test_predict_image_with_json_api(image_path)