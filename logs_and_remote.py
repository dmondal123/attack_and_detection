from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import paramiko
import re

app = FastAPI()

# Configuration
HOST = "192.168.x.x"  # Replace with the IP address of Laptop A
PORT = 22  # Default SSH port
USERNAME = "your_username"  # Replace with the SSH username on Laptop A
KEY_FILEPATH = "/path/to/private/key"  # Replace with the path to the private key on Laptop B
REMOTE_SCRIPT_PATH = "/remote/path/test_sql7.py"  # Replace with the desired path on Laptop A

LOG_FILE_PATH = '/Users/hgarg/Desktop/sql_injection_logs.log'
OUTPUT_FILE_PATH = '/Users/hgarg/Desktop/filtered_logs.log'
SQL_INJECTION_PATTERNS = [
    r'SqlInjectionAdvanced/attack6a',
]

class ExecuteScriptRequest(BaseModel):
    local_script_path: str

class SearchLogsRequest(BaseModel):
    log_file_path: str
    output_file_path: str
    patterns: list[str] = SQL_INJECTION_PATTERNS

def execute_script_remotely(local_script_path: str):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        private_key = paramiko.RSAKey.from_private_key_file(KEY_FILEPATH)
        ssh_client.connect(hostname=HOST, port=PORT, username=USERNAME, pkey=private_key)
        
        sftp = ssh_client.open_sftp()
        sftp.put(local_script_path, REMOTE_SCRIPT_PATH)
        sftp.close()
        
        stdin, stdout, stderr = ssh_client.exec_command(f'python3 {REMOTE_SCRIPT_PATH}')
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        return {"output": output, "error": error}
        
    finally:
        ssh_client.close()

def search_patterns(log_file, patterns):
    with open(log_file, 'r') as file:
        logs = file.readlines()
    
    matched_lines = []
    for pattern in patterns:
        regex = re.compile(pattern)
        for line in logs:
            if regex.search(line):
                matched_lines.append(line)
    
    return matched_lines

def write_to_file(lines, output_file):
    with open(output_file, 'w') as file:
        file.writelines(lines)

@app.post("/execute-script/")
def execute_script(request: ExecuteScriptRequest):
    try:
        result = execute_script_remotely(request.local_script_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search-logs/")
def search_logs(request: SearchLogsRequest):
    try:
        matched_lines = search_patterns(request.log_file_path, request.patterns)
        write_to_file(matched_lines, request.output_file_path)
        return {"message": f"Matched lines have been written to {request.output_file_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
