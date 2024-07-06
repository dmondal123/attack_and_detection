generate_attack_sys = """
You are an intelligent assistant experienced in Python programming.
Always answer as helpfully as possible in attacking vulnerable applications.
If a question does not make any sense, or is not factually coherent, explain why instead of 
answering something not correct. If you don't know the answer to a question,
please don't share false information.

Steps:

- Make a function spoof_ip(target_ip, spoof_ip): This function creates an ARP packet with the specified target IP and spoofed IP. 

- Make a function get_mac(ip): This function sends an ARP request to obtain the MAC address associated with the given IP. 

- Make a function restore(destination_ip, source_ip): This function restores the original MAC addresses of the destination and source IPs. 

- Make a variable sent_packets_count: This variable keeps track of the number of spoofed packets sent.

- The script starts by setting the target IP and gateway IP addresses. It then enters a loop where it continuously sends spoofed ARP packets to the target and gateway. The packets are sent every 2 seconds using time.sleep(2).

- The script handles keyboard interrupts using except KeyboardInterrupt. When a keyboard interrupt is detected (i.e., CTRL+C is pressed), it restores the original MAC addresses of the target and gateway using the restore function and exits the loop.

Note: Use Python for generating scripts. Avoid assertion errors.

Take a deep breath and think step by step then do the task. Provide your answer and a confidence score between 0 and 1 for your task.
"""

# Default user/human prompt for generating test cases
generate_attack_human = "Generate a python script for doing an ip spoofing attack. The target ip is {target_ip} and gateway ip is {gateway_ip}"

from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate 
import re

llm = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", max_tokens=1000)


def generate_attack_vector(target_ip, gateway_ip):
    sys_message = generate_attack_sys
    human_message = generate_attack_human

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", sys_message),
        ("human", human_message),
    ]
    )
    chain = prompt | llm
    out = chain.invoke({'target_ip': target_ip, 'gateway_ip': gateway_ip})
    test_cases = out
    print(out)
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
    test_cases_name = f"test_ip"
    test_file_name = f"test_ip1.py"
    test_file_path = os.path.join("results", test_file_name)

    #Write the filtered test cases to the file
    with open(test_file_path, "w") as test_file:
        test_file.write(filtered_test_cases)

    #Logging successful test case saving
    logging.info("Execution in progress...")
    print(f"The script has been saved to {test_file_path}")

    print("Application name is: ", test_cases_name)
    print("Attack script file name is: ", test_file_name)

target_ip = "192.168.1.10"
gateway_ip = "192.168.1.1"


output = generate_attack_vector(target_ip, gateway_ip)
