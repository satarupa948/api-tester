import asyncio
import time
import httpx
import pandas as pd
from config import API_URL, NUM_REQUESTS, CONCURRENT_WORKERS, TIMEOUT

async def send_request(client):
    """Sends a single API request asynchronously and measures response time."""
    start_time = time.time()
    try:
        response = await client.get(API_URL, timeout=TIMEOUT)
        latency = time.time() - start_time
        return {
            "status_code": response.status_code,
            "latency": round(latency, 4),
            "success": response.status_code == 200
        }
    except httpx.RequestError:
        return {"status_code": None, "latency": None, "success": False}

async def run_load_test():
    """Executes the load test with multiple concurrent requests."""
    results = []
    async with httpx.AsyncClient() as client:
        tasks = [send_request(client) for _ in range(NUM_REQUESTS)]
        results = await asyncio.gather(*tasks)
    return results

def save_results(results):
    """Saves results to a CSV file for further analysis."""
    df = pd.DataFrame(results)
    df.to_csv("load_test_results.csv", index=False)
    print("Results saved to 'load_test_results.csv'.")

async def main():
    print(f"Running load test on {API_URL} with {NUM_REQUESTS} requests...")
    results = await run_load_test()
    save_results(results)

    # Summary
    total_requests = len(results)
    success_count = sum(1 for r in results if r["success"])
    latencies = [r["latency"] for r in results if r["latency"] is not None]
    
    avg_latency = sum(latencies) / len(latencies) if latencies else 0

    print(f"Total Requests: {total_requests}")
    print(f"Successful Requests: {success_count}")
    print(f"Failure Rate: {round(100 - (success_count / total_requests * 100), 2)}%")
    print(f"Average Latency: {round(avg_latency, 4)} sec")

if __name__ == "__main__":
    asyncio.run(main())
