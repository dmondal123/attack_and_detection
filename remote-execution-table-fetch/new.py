import subprocess

def create_conda_environment(env_name, python_version):
    try:
        # Command to create Conda environment with specified Python version
        create_env_cmd = f'conda create -y -n {env_name} python={python_version}'

        # Execute the command using subprocess
        subprocess.run(create_env_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"Conda environment '{env_name}' created successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error creating Conda environment: {e}")

def execute_script_remotely(host, port, username, key_filepath, local_script_path, remote_script_path, conda_env):
    try:
        # Create Conda environment if it doesn't exist
        create_conda_environment(conda_env, "3.10.14")

        # Construct the command to activate Conda environment and execute script remotely
        activate_cmd = f'source ~/.zshrc && conda activate {conda_env} && '
        scp_command = f'scp {local_script_path} {username}@{host}:{remote_script_path}'
        ssh_command = f'ssh {username}@{host} "{activate_cmd} python3 {remote_script_path}"'

        # Execute SCP command to transfer the script
        subprocess.run(scp_command, shell=True, check=True)

        # Execute SSH command to activate environment and run script remotely
        result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)

        # Print the output and error (if any)
        print("Output:")
        print(result.stdout)
        print("Error:")
        print(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Error executing remote script: {e}")

if __name__ == "__main__":
    # Configuration
    host = "172.18.84.102"  # Replace with the IP address of Laptop A
    port = 22  # Default SSH port
    username = "interview"  # Replace with the SSH username on Laptop A
    key_filepath = "/Users/interview/.ssh/id_rsa"  # Replace with the path to the private key on Laptop B
    local_script_path = "/Users/interview/Downloads/attack/results/test_sql7.py"  # Replace with the path to the script on Laptop B
    remote_script_path = "/Users/interview/Desktop/test_sql7.py"  # Replace with the desired path on Laptop A
    conda_env = "app"  # Conda environment name

    # Execute the script remotely
    execute_script_remotely(host, port, username, key_filepath, local_script_path, remote_script_path, conda_env)
