import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Read API test results
df = pd.read_csv("load_test_results.csv")

# Generate summary statistics
total_requests = len(df)
successful_requests = df["success"].sum()
failed_requests = total_requests - successful_requests
failure_rate = round((failed_requests / total_requests) * 100, 2)
avg_latency = round(df["latency"].mean(), 4)

summary_text = f"""
### API Load Test Summary:
- **Total Requests:** {total_requests}
- **Successful Requests:** {successful_requests}
- **Failed Requests:** {failed_requests}
- **Failure Rate:** {failure_rate}%
- **Average Latency:** {avg_latency} sec
"""

# AI-Powered Analysis
prompt = f"""
Analyze the following API load test results and suggest optimizations:
{summary_text}

Provide insights on:
1. Performance bottlenecks
2. Potential causes of failures
3. Optimization strategies

The report should be very minimal, no long reports
"""

# Generate AI response
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
ai_analysis = response.text

# Return the summary and AI insights as Markdown
report_markdown = f"""
{summary_text}

### AI Insights:
{ai_analysis}
"""

print(report_markdown)  # Output the markdown content for Streamlit to capture
