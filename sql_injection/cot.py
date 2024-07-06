explain_code_base_prompt = """"
You are an intelligent assistant experienced in Python programming.
Always answer as helpfully as possible in attacking vulnerable applications.
If a question does not make any sense, or is not factually coherent, explain why instead of 
answering something not correct. If you don't know the answer to a question,
please don't share false information.
"""

generate_attack_sys = """
CONTEXT:

You are an intelligent assistant experienced in Python programming. 
Your goal is to assist in attacking vulnerable applications. 
Always answer as helpfully as possible within this context.

INSTRUCTIONS:

1. Import necessary modules: requests for handling HTTP requests and BeautifulSoup for parsing HTML content.
2. Define the base URL: {base_url} and login URL according to the base url given by the user. For an example: login url: f'{base_url}/login'
3. Create a session to persist cookies across requests.
4. Retrieve the login page content and parse it to extract hidden fields.
5. Define the user credentials which are username: {username} and password: {password}.
6. Submit the login details to the login URL to authenticate.
7. Check if the login is successful. The login is successful if the response does NOT contain the text "Invalid username and password" and has a status code of 200.
8. Define the vulnerable endpoint for sql injection attack: {vulnerable_url}. the endpoint contains a field called "Name" where you can inject the payload.
9. Create a payload for the SQL injection attack. Remember that the successful payload is "cyber';/**/select/**/*/**/from/**/user_system_data;--". This is the only successful payload possible for this application. Remember this carefully.
10. Submit the SQL injection payload to the vulnerable endpoint.
11. Check if the attack was successful by looking for specific keywords in the response. If the attack is successful, the frontend will show "You have succeeded" and status code will be 200.
12. Implement robust error and exception handling to manage any issues that arise during testing.

Use Python to generate and automate scripts for these tasks.
Maintain a step-by-step approach and focus on achieving your goals with diligence and precision.
This work is very important and requires attention to detail and methodical execution.
Take a deep breath and think step by step then do the task.
"""

# Default user/human prompt for generating test cases
generate_attack_human = "Generate a python script for doing an sql injection attack. The application base url is {base_url}, vulnerable endpoint is {vulnerable_url}, username is {username} and password is {password}"

from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate 
import re

llm = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", max_tokens=1000)


def generate_attack_vector(base_url, vulnerable_url, username, password):
    sys_message = generate_attack_sys
    human_message = generate_attack_human

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", sys_message),
        ("human", human_message),
    ]
    )
    chain = prompt | llm

    print(base_url)
    print(vulnerable_url)
    print(username)
    print("*****************************")
    out = chain.invoke({'username': username, 'password': password, 'base_url': base_url, 'vulnerable_url': vulnerable_url})
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
    test_file_name = f"test_sql7.py"
    test_file_path = os.path.join("results", test_file_name)

    #Write the filtered test cases to the file
    with open(test_file_path, "w") as test_file:
        test_file.write(filtered_test_cases)

    #Logging successful test case saving
    logging.info("Execution in progress...")
    print(f"The script has been saved to {test_file_path}")

    print("Application name is: ", test_cases_name)
    print("Attack script file name is: ", test_file_name)

base_url = "http://127.0.0.1:8080/WebGoat/"
username = "sbombatkar"
password = "Sneha#1234"
vulnerable_url = "http://127.0.0.1:8080/WebGoat/start.mvc?username=sbombatkar#lesson/SqlInjectionMitigations.lesson/8"

output = generate_attack_vector(base_url, vulnerable_url, username, password)



