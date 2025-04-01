import subprocess

def run_script(script_name):
    """Runs a Python script and prints output."""
    print(f"\n🚀 Running {script_name}...\n")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"❌ Error in {script_name}:\n", result.stderr)

if __name__ == "__main__":
    print("\n🔄 Starting API Load Test Process...\n")
    
    # Step 1: Run API Load Test
    run_script("load_tester.py")
    
    # Step 2: Analyze Results
    run_script("analyze_results.py")
    
    # Step 3: Generate AI-Powered Report
    run_script("generate_report.py")

    print("\n✅ All tasks completed successfully! Check 'API_Load_Test_Report.pdf'.")
