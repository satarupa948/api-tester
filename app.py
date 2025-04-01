import streamlit as st
import subprocess
import os
import json

# Function to run the scripts
def run_script(script_name):
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    return result.stdout, result.stderr

# Streamlit UI
st.title("API Load Tester and Report Generator")

# Sidebar for API Test Configuration
st.sidebar.header("API Test Configuration")
api_url = st.sidebar.text_input("API URL", "https://jsonplaceholder.typicode.com/posts")

# Method selection
method = st.sidebar.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE", "PATCH"])

# Authentication options
auth_type = st.sidebar.selectbox("Authentication Type", ["No Auth", "Basic Auth", "Bearer Token"])
username = ""
password = ""
token = ""

# Basic Auth (if selected)
if auth_type == "Basic Auth":
    username = st.sidebar.text_input("Username", "")
    password = st.sidebar.text_input("Password", "", type="password")

# Bearer Token (if selected)
if auth_type == "Bearer Token":
    token = st.sidebar.text_input("Bearer Token", "")

# Body input (only for POST, PUT, PATCH)
body = ""
if method in ["POST", "PUT", "PATCH"]:
    body = st.sidebar.text_area("Request Body (JSON format)", '{"title": "foo", "body": "bar", "userId": 1}')
else:
    st.sidebar.write("Body input is not required for the selected HTTP method.")

# Headers input
headers = st.sidebar.text_area("Custom Headers (JSON format)", '{"Content-Type": "application/json"}')

# Timeout and Retry Settings
timeout = st.sidebar.number_input("Timeout (seconds)", min_value=1, value=5)
retries = st.sidebar.number_input("Number of Retries", min_value=0, value=3)

# New fields: Number of requests and concurrent workers
num_requests = st.sidebar.number_input("Total Number of Requests", min_value=1, value=100)
concurrent_workers = st.sidebar.number_input("Number of Concurrent Workers", min_value=1, value=10)

# Button to start the test
if st.sidebar.button("Start Load Test"):
    st.info("Running API load test... Please wait.")
    
    # Save config to a temporary config file to pass to load_tester.py
    config_content = f"""
API_URL = "{api_url}"
METHOD = "{method}"
AUTH_TYPE = "{auth_type}"
USERNAME = "{username}"
PASSWORD = "{password}"
TOKEN = "{token}"
BODY = '''{body}'''
HEADERS = '''{headers}'''
TIMEOUT = {timeout}
RETRIES = {retries}
NUM_REQUESTS = {num_requests}
CONCURRENT_WORKERS = {concurrent_workers}
    """
    
    with open("config.py", "w") as config_file:
        config_file.write(config_content)
    
    # Step 1: Run API Load Test
    output, error = run_script("load_tester.py")
    if error:
        st.error(f"Error during load test: {error}")
    else:
        st.success("API Load Test completed successfully!")
        # st.text(output)
        
        # Step 2: Analyze the results
        st.info("Analyzing the results...")
        analyze_output, analyze_error = run_script("analyze_results.py")
        if analyze_error:
            st.error(f"Error during analysis: {analyze_error}")
        else:
            # st.success("Analysis complete!")
            # st.text(analyze_output)
            
            # Step 3: Generate AI-powered report and display it as markdown
            st.info("Generating AI-powered report...")
            report_output, report_error = run_script("generate_report.py")
            if report_error:
                st.error(f"Error during report generation: {report_error}")
            else:
                # st.success("Report generated successfully!")
                
                # Display the report as markdown
                st.markdown(report_output)
                
                # Display the generated graphs
                st.info("Displaying generated graphs...")

                # Example: Displaying a saved image from the local directory
                latency_distribution = "latency_distribution.png"  # Path to the saved image
                if os.path.exists(latency_distribution):
                    st.image(latency_distribution, caption="Latency Distribution", use_container_width=True)
                else:
                    st.error("Graph image not found!")

                success_failure_pie = "success_failure_pie.png"
                if os.path.exists(success_failure_pie):
                    st.image(success_failure_pie, caption="Success-Failure Rate", use_container_width=True)
                else:
                    st.error("Graph image not found!")
                    
                    
                # Provide a button to download the test CSV report
                csv_report_path = "load_test_results.csv"
                if os.path.exists(csv_report_path):
                    with open(csv_report_path, "rb") as csv_file:
                        st.download_button(
                            label="Download Test Report (CSV)",
                            data=csv_file,
                            file_name="test_results.csv",
                            mime="text/csv"
                        )
                else:
                    st.error("CSV report not found!")
