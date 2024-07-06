import requests
from bs4 import BeautifulSoup

# Base URL of WebGoat
base_url = 'http://127.0.0.1:8080/WebGoat'

# Login URL
login_url = f'{base_url}/login'

# Login credentials
Username = 'sbombatkar'
Password = 'Sneha#1234'

# Session to persist cookies
session = requests.Session()

# Step 1: Get the login page to capture any hidden fields
login_page_response = session.get(login_url)
login_page_content = login_page_response.text

# Parse the login page to get hidden form fields
soup = BeautifulSoup(login_page_content, 'html.parser')
hidden_fields = soup.find_all("input", type="hidden")

# Create the login payload
login_payload = {field.get('name'): field.get('value') for field in hidden_fields}
login_payload['username'] = Username
login_payload['password'] = Password

# Step 2: Submit the login form
login_response = session.post(login_url, data=login_payload)

# Check if login was successful by looking for specific keywords in the response
if 'Invalid username and password' not in login_response.text and login_response.status_code == 200:
    print("Login successful")
else:
    print("Login failed")
    print("Status Code:", login_response.status_code)
    # print("Response:", login_response.text)