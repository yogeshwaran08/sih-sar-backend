"""
Test script for SAR Colorization Metrics API
Run the FastAPI server first: uvicorn app.main:app --reload
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_all_metrics():
    """Test getting all model metrics"""
    print("=" * 60)
    print("TEST 1: Get All Model Metrics")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/models/metrics")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success! Found {len(data['models'])} models")
        print(f"Available models: {list(data['models'].keys())}")
    else:
        print(f"✗ Failed with status code: {response.status_code}")
    print()


def test_specific_model():
    """Test getting specific model metrics"""
    print("=" * 60)
    print("TEST 2: Get Specific Model Metrics (sar-colorizer-v1)")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/models/sar-colorizer-v1/metrics")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success!")
        print(f"Model: {data['model']} {data['version']}")
        print(f"Dataset: {data['dataset']}")
        print(f"Number of epochs: {len(data['epochs'])}")
        
        # Show first epoch details
        if data['epochs']:
            epoch = data['epochs'][0]
            print(f"\nFirst Epoch Metrics:")
            print(f"  - G_total: {epoch['G_total']}")
            print(f"  - D_total: {epoch['D_total']}")
            print(f"  - PSNR: {epoch['psnr']}")
            print(f"  - SSIM: {epoch['ssim']}")
    else:
        print(f"✗ Failed with status code: {response.status_code}")
    print()


def test_latest_epoch():
    """Test getting latest epoch metrics"""
    print("=" * 60)
    print("TEST 3: Get Latest Epoch Metrics")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/models/sar-colorizer-v2/metrics/latest")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success!")
        print(f"Latest Epoch: {data['epoch']}")
        print(f"Metrics:")
        print(f"  - G_total: {data['G_total']}")
        print(f"  - D_total: {data['D_total']}")
        print(f"  - PSNR: {data['psnr']} dB")
        print(f"  - SSIM: {data['ssim']}")
        print(f"  - LPIPS: {data['lpips']}")
        print(f"  - Learning Rate: {data['lr']}")
        print(f"  - Epoch Time: {data['epochTimeMs']} ms")
    else:
        print(f"✗ Failed with status code: {response.status_code}")
    print()


def test_specific_epoch():
    """Test getting specific epoch metrics"""
    print("=" * 60)
    print("TEST 4: Get Specific Epoch Metrics (Epoch 3)")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/models/sar-colorizer-v1/metrics/epoch/3")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success!")
        print(f"Epoch: {data['epoch']}")
        print(f"Loss Metrics:")
        print(f"  - GAN Loss: {data['loss_GAN']}")
        print(f"  - Pixel Loss: {data['loss_pixel']}")
        print(f"  - Perceptual Loss: {data['loss_perceptual']}")
        print(f"Quality Metrics:")
        print(f"  - PSNR: {data['psnr']} dB")
        print(f"  - SSIM: {data['ssim']}")
        print(f"  - LPIPS: {data['lpips']}")
        print(f"Color Accuracy:")
        print(f"  - deltaE2000 Mean: {data['deltaE2000_mean']}")
        print(f"  - deltaE2000 Median: {data['deltaE2000_median']}")
    else:
        print(f"✗ Failed with status code: {response.status_code}")
    print()


def test_error_handling():
    """Test error handling for non-existent model"""
    print("=" * 60)
    print("TEST 5: Error Handling (Non-existent Model)")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/models/non-existent-model/metrics")
    
    if response.status_code == 404:
        data = response.json()
        print(f"✓ Correctly returned 404")
        print(f"Error message: {data['detail']}")
    else:
        print(f"✗ Expected 404, got: {response.status_code}")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  SAR Colorization Metrics API - Test Suite            ║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        # Test root endpoint first
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("✗ Server is not running or not accessible!")
            print("Please start the server with: uvicorn app.main:app --reload")
            exit(1)
        
        print("✓ Server is running!")
        print()
        
        # Run all tests
        test_all_metrics()
        test_specific_model()
        test_latest_epoch()
        test_specific_epoch()
        test_error_handling()
        
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
        print()
        print("Visit http://localhost:8000/docs for interactive API documentation")
        print()
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the server!")
        print("Please start the server with: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"✗ Error: {e}")
