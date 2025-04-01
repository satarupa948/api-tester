import time
import requests
import concurrent.futures
import pandas as pd
from config import API_URL, NUM_REQUESTS, CONCURRENT_WORKERS, TIMEOUT

def send_request():
    """Sends a single API request and measures response time."""
    start_time = time.time()
    try:
        response = requests.get(API_URL, timeout=TIMEOUT)
        latency = time.time() - start_time
        return {
            "status_code": response.status_code,
            "latency": round(latency, 4),
            "success": response.status_code == 200
        }
    except requests.exceptions.RequestException:
        return {"status_code": None, "latency": None, "success": False}

def run_load_test():
    """Executes the load test with multiple concurrent requests."""
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        future_requests = [executor.submit(send_request) for _ in range(NUM_REQUESTS)]
        
        for future in concurrent.futures.as_completed(future_requests):
            results.append(future.result())
    
    return results

def save_results(results):
    """Saves results to a CSV file for further analysis."""
    df = pd.DataFrame(results)
    df.to_csv("load_test_results.csv", index=False)
    print("Results saved to 'load_test_results.csv'.")

if __name__ == "__main__":
    print(f"Running load test on {API_URL} with {NUM_REQUESTS} requests...")
    results = run_load_test()
    save_results(results)

    # Summary
    total_requests = len(results)
    success_count = sum(1 for r in results if r["success"])
    avg_latency = sum(r["latency"] for r in results if r["latency"]) / success_count
    
    print(f"Total Requests: {total_requests}")
    print(f"Successful Requests: {success_count}")
    print(f"Failure Rate: {round(100 - (success_count / total_requests * 100), 2)}%")
    print(f"Average Latency: {round(avg_latency, 4)} sec")