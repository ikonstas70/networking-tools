import subprocess
import re
from tabulate import tabulate

def get_mac_address(ipv6_address):
    try:
        # Run the command to get neighbor cache information (mac address associated with ipv6 address)
        result = subprocess.run(
            ["ndp", "-a"], capture_output=True, text=True, check=True
        )
        
        # Extract the MAC address for the provided IPv6 address
        pattern = re.compile(rf"({ipv6_address}).*?([0-9a-f:]+)\s+[a-f0-9]+")
        match = pattern.search(result.stdout)
        
        if match:
            return match.group(2)
        else:
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return None

def print_info(ipv6_address, mac_address):
    table = [["IPv6 Address", ipv6_address], ["MAC Address", mac_address]]
    print("\n" + tabulate(table, headers=["Field", "Value"], tablefmt="grid"))

def main():
    print("IPv6 and MAC Address Extractor")
    print("===============================")
    
    while True:
        ipv6_address = input("Enter an IPv6 address (or type 'exit' to quit): ").strip()
        
        if ipv6_address.lower() == 'exit':
            print("Exiting the script.")
            break

        # Validate the input IPv6 address format
        ipv6_regex = re.compile(r"([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}")
        if not ipv6_regex.match(ipv6_address):
            print("Invalid IPv6 format. Please enter a valid IPv6 address.")
            continue
        
        mac_address = get_mac_address(ipv6_address)
        
        if mac_address:
            print_info(ipv6_address, mac_address)
        else:
            print(f"Could not extract a valid MAC address for the IPv6 address: {ipv6_address}")

if __name__ == "__main__":
    main()
