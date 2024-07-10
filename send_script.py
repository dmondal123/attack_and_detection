import paramiko
import os

def execute_script_remotely(host, port, username, key_filepath, local_script_path, remote_script_path):
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Load the private key
        private_key = paramiko.RSAKey.from_private_key_file(key_filepath)
        
        # Connect to the remote host using the private key
        ssh_client.connect(hostname=host, port=port, username=username, pkey=private_key)
        
        # Create an SFTP session from the SSH connection
        sftp = ssh_client.open_sftp()
        
        # Upload the script to the remote host
        sftp.put(local_script_path, remote_script_path)
        sftp.close()
        
        # Execute the script on the remote host
        stdin, stdout, stderr = ssh_client.exec_command(f'python3 {remote_script_path}')
        
        # Print the output and error (if any)
        print("Output:")
        print(stdout.read().decode())
        print("Error:")
        print(stderr.read().decode())
        
    finally:
        # Close the SSH connection
        ssh_client.close()

if __name__ == "__main__":
    # Configuration
    host = "192.168.x.x"  # Replace with the IP address of Laptop A
    port = 22  # Default SSH port
    username = "your_username"  # Replace with the SSH username on Laptop A
    key_filepath = "/path/to/private/key"  # Replace with the path to the private key on Laptop B
    local_script_path = "/path/to/test_sql7.py"  # Replace with the path to the script on Laptop B
    remote_script_path = "/remote/path/test_sql7.py"  # Replace with the desired path on Laptop A

    # Execute the script remotely
    execute_script_remotely(host, port, username, key_filepath, local_script_path, remote_script_path)
