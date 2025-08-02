#!/usr/bin/env python3
"""
Test script untuk API Batik Classification
"""

import requests
import json
import os
from pathlib import Path

# Konfigurasi
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("🔍 Testing model info...")
    try:
        response = requests.get(f"{API_BASE_URL}/model-info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model info:")
            print(f"   Model type: {data.get('model_type')}")
            print(f"   Total classes: {data.get('total_classes')}")
            print(f"   Framework: {data.get('framework')}")
            if 'available_classes' in data:
                print(f"   Sample classes: {data['available_classes'][:5]}...")
            return True
        else:
            print(f"❌ Model info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Model info error: {e}")
        return False

def test_root_endpoint():
    """Test root endpoint"""
    print("🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint: {data}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_api_docs():
    """Test API docs endpoint"""
    print("🔍 Testing API docs...")
    try:
        response = requests.get(f"{API_BASE_URL}/api-docs")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API docs: {data}")
            return True
        else:
            print(f"❌ API docs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API docs error: {e}")
        return False

def test_prediction_with_sample_image():
    """Test prediction with a sample image (if available)"""
    print("🔍 Testing prediction endpoint...")
    
    # Cari file gambar untuk testing
    image_extensions = ['.jpg', '.jpeg', '.png']
    sample_image = None
    
    for ext in image_extensions:
        for file in Path('.').glob(f'*{ext}'):
            if file.name != 'test_image.jpg':  # Skip test files
                sample_image = file
                break
        if sample_image:
            break
    
    if not sample_image:
        print("⚠️ No sample image found for testing prediction")
        return False
    
    try:
        with open(sample_image, 'rb') as f:
            files = {'file': (sample_image.name, f, 'image/jpeg')}
            response = requests.post(f"{API_BASE_URL}/predict", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction successful:")
            print(f"   File: {data.get('filename')}")
            print(f"   Top prediction: {data.get('top_prediction', {}).get('class_name', 'N/A')}")
            print(f"   Confidence: {data.get('top_prediction', {}).get('confidence_percentage', 'N/A')}%")
            
            # Show all predictions
            if 'predictions' in data:
                print(f"   All predictions:")
                for pred in data['predictions'][:3]:  # Show top 3
                    print(f"     {pred['rank']}. {pred['class_name']} ({pred['confidence_percentage']}%)")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting API tests...")
    print("=" * 50)
    
    tests = [
        test_root_endpoint,
        test_health_check,
        test_model_info,
        test_api_docs,
        test_prediction_with_sample_image
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print("-" * 30)
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the API configuration.")
    
    return passed == total

if __name__ == "__main__":
    main() 