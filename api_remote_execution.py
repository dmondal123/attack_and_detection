from fastapi import FastAPI, HTTPException
import subprocess

app = FastAPI()

def create_conda_environment(env_name, python_version):
    try:
        # Command to create Conda environment with specified Python version
        create_env_cmd = f'conda create -y -n {env_name} python={python_version}'

        # Execute the command using subprocess
        result = subprocess.run(create_env_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()
        error = result.stderr.decode()

        return output, error

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error creating Conda environment: {e}")

def execute_script_remotely(host, port, username, key_filepath, local_script_path, remote_script_path, conda_env):
    try:
        # Create Conda environment if it doesn't exist
        create_output, create_error = create_conda_environment(conda_env, "3.10.14")

        # Construct the command to activate Conda environment and execute script remotely
        activate_cmd = f'source ~/.zshrc && conda activate {conda_env} && '
        scp_command = f'scp {local_script_path} {username}@{host}:{remote_script_path}'
        ssh_command = f'ssh {username}@{host} "{activate_cmd} python3 {remote_script_path}"'

        # Execute SCP command to transfer the script
        subprocess.run(scp_command, shell=True, check=True)

        # Execute SSH command to activate environment and run script remotely
        result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
        output = result.stdout
        error = result.stderr

        # Save output and error to a file
        with open("execute_script_output.txt", "w") as f:
            f.write("Conda Environment Creation Output:\n" + create_output + "\nConda Environment Creation Error:\n" + create_error)
            f.write("\nScript Execution Output:\n" + output + "\nScript Execution Error:\n" + error)

        # Return the combined output and error
        return {"create_output": create_output, "create_error": create_error, "execution_output": output, "execution_error": error}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error executing remote script: {e}")

@app.post("/run-all")
def run_all():
    host = "172.18.84.102"
    port = 22
    username = "interview"
    key_filepath = "/Users/interview/.ssh/id_rsa"
    local_script_path = "/Users/interview/Downloads/attack/results/test_sql7.py"
    remote_script_path = "/Users/interview/Desktop/test_sql7.py"
    conda_env = "app"
    result = execute_script_remotely(
        host,
        port,
        username,
        key_filepath,
        local_script_path,
        remote_script_path,
        conda_env
    )

    # Read the output from the file
    with open("execute_script_output.txt", "r") as f:
        file_content = f.read()

    return {"result": result, "file_content": file_content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
