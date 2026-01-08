import requests
import sys

def probe(url, name):
    try:
        response = requests.get(url, timeout=5)
        print(f"{name}: {response.status_code}")
    except Exception as e:
        print(f"{name}: Error {e}")

if __name__ == "__main__":
    probe('http://localhost:8000/api/health', "Health")
    probe('http://localhost:8000/api/enrich', "Enrich") # Expect 405 Method Not Allowed or 422 Unprocessable Entity if route exists
    probe('http://localhost:8000/test', "Test")
