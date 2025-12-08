import requests
import concurrent.futures

# Backend URL
URL = "http://10.131.103.92:5000/users"

def hit():
    """
    Send a single request to backend and return the status and pod name.
    """
    try:
        r = requests.get(URL, timeout=5)
        # X-Pod-Name should come from backend headers if middleware is added
        pod_name = r.headers.get("X-Pod-Name", "unknown")
        return r.status_code, pod_name
    except Exception:
        return "ERR", "N/A"

def main():
    total = int(input("Enter number of requests: "))
    print(f"\nSending {total} concurrent requests to backend...\n")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(hit) for _ in range(total)]
        for future in concurrent.futures.as_completed(futures):
            status, pod = future.result()
            results.append((status, pod))
            print(f"status:{status}, Pod:{pod}")

    # Summary
    print("\n--- POD HIT COUNT ---")
    pods = {}
    for _, pod in results:
        pods[pod] = pods.get(pod, 0) + 1
    for pod, count in pods.items():
        print(f"{pod}: {count} requests")

    success = sum(1 for status, _ in results if status == 200)
    fail = total - success
    print(f"\nTotal Success: {success}")
    print(f"Total Failed: {fail}")

if __name__ == "__main__":
    main()


