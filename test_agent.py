
import requests
import json
import time

def test_v3_enrichment():
    url = "http://localhost:8001/api/enrich/bulk"
    print(f"Calling V3 Bulk Enrichment at {url}...")
    try:
        start_time = time.time()
        response = requests.post(url)
        duration = time.time() - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Duration: {duration:.2f}s")
        
        if response.status_code == 200:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("Error Response:")
            print(response.text)
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_v3_enrichment()
