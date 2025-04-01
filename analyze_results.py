import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the results from CSV
df = pd.read_csv("load_test_results.csv")

# Basic Summary
total_requests = len(df)
successful_requests = df["success"].sum()
failed_requests = total_requests - successful_requests
avg_latency = df["latency"].mean()

print(f"Total Requests: {total_requests}")
print(f"Successful Requests: {successful_requests}")
print(f"Failed Requests: {failed_requests}")
print(f"Failure Rate: {round((failed_requests / total_requests) * 100, 2)}%")
print(f"Average Latency: {round(avg_latency, 4)} sec")

# Plot Latency Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["latency"], bins=20, kde=True, color="blue")
plt.xlabel("Response Time (seconds)")
plt.ylabel("Frequency")
plt.title("API Response Time Distribution")
plt.grid(True)
plt.savefig("latency_distribution.png")
# plt.show()

# Plot Success vs Failure Rate
plt.figure(figsize=(6, 6))
plt.pie([successful_requests, failed_requests], labels=["Success", "Failure"],
        autopct="%1.1f%%", colors=["green", "red"], startangle=90)
plt.title("Success vs Failure Rate")
plt.savefig("success_failure_pie.png")
# plt.show()
