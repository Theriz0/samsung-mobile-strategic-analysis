import datetime
import os

def log_event(message, level="INFO"):
    # 1. Get the absolute path of the folder where this script lives (scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Go up one level to the main 'Analysis' folder
    base_dir = os.path.dirname(script_dir)
    
    # 3. Define the full path to the logs folder and file
    log_dir = os.path.join(base_dir, 'logs')
    log_path = os.path.join(log_dir, 'pipeline_history.log')
    
    # 4. Safety check: Create the logs folder if it got deleted
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # 5. Format and write the log entry
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    
    with open(log_path, 'a') as f:
        f.write(log_entry)
    
    print(f"Logged to {log_path}: {log_entry.strip()}")

if __name__ == "__main__":
    # Test it
    log_event("Manual test of the logging system")