import requests
from concurrent.futures import ThreadPoolExecutor

#  FRONTEND_URL = "http://10.131.103.92:4000"
BACKEND_URL = "http://10.131.103.92:5000/users"

def hit_frontend(_):
    """Fire-and-forget request to frontend (like curl -s > /dev/null)."""
    try:
        requests.get(FRONTEND_URL, timeout=10)
    except:
        pass

def hit_backend(_):
    """Request backend and print status, time, and pod handling the request."""
    try:
        r = requests.get(BACKEND_URL, timeout=10)
        pod = r.headers.get("X-Pod-Name", "unknown")
        print(f"status:{r.status_code},Time:{r.elapsed.total_seconds():.3f}s,Pod:{pod}")
    except:
        print(f"status:ERR,Time:N/A,Pod:N/A")

def main():
    total = int(input("Enter number of requests: "))

    # Frontend requests
    print(f"Sending {total} fire-and-forget requests to frontend...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        list(executor.map(hit_frontend, range(total)))

    # Backend requests
    print(f"\nSending {total} requests to backend (showing pod handling each request)...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        list(executor.map(hit_backend, range(total)))

if __name__ == "__main__":
    main()
