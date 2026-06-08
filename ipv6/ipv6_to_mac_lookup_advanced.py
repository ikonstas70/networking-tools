import subprocess
import re
from tabulate import tabulate

def get_mac_address(ipv6_address):
    try:
        # Run the command to get neighbor cache information
        result = subprocess.run(
            ["ndp", "-a"], capture_output=True, text=True, check=True
        )
        
        # Extract the MAC address for the provided IPv6 address
        pattern = re.compile(rf"({ipv6_address}).*?(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})\s+", re.MULTILINE)
        match = pattern.search(result.stdout)
        
        if match:
            return match.group(2)  # Return the MAC address
        else:
            return None
    except (subprocess.CalledProcessError, AttributeError) as e:
        print(f"Error: {e}")
        return None

def print_info(ipv6_address, mac_address):
    table = [["IPv6 Address", ipv6_address], ["MAC Address", mac_address]]
    print("\n" + tabulate(table, headers=["Field", "Value"], tablefmt="grid"))

def get_valid_ipv6_and_mac_addresses():
    try:
        # Run the command to get neighbor cache information
        result = subprocess.run(
            ["ndp", "-a"], capture_output=True, text=True, check=True
        )
        
        # Regex to extract full IPv6 addresses and corresponding MAC addresses
        pattern = re.compile(r"(([0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4}|::1).*?(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})\s+", re.MULTILINE)
        matches = pattern.findall(result.stdout)
        
        # Extract the full IPv6 address and MAC address from the matches
        valid_addresses = [{"IPv6 Address": match[0], "MAC Address": match[2]} for match in matches]
        return valid_addresses
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return []

def main():
    print("IPv6 and MAC Address Extractor")
    print("===============================")
    
    while True:
        print("\nMenu:")
        print("1. Enter an IPv6 address to query for MAC address.")
        print("2. Run 'ndp -a' to get all valid IPv6 addresses and choose one.")
        print("3. Get all MAC addresses from 'ndp -a' command for valid IPv6 addresses.")
        print("4. Exit.")
        
        choice = input("Choose an option (1/2/3/4): ").strip()
        
        if choice == '1':
            ipv6_address = input("Enter an IPv6 address (or type 'exit' to quit): ").strip()
            
            if ipv6_address.lower() == 'exit':
                print("Exiting the script.")
                break

            # Validate the input IPv6 address format
            ipv6_regex = re.compile(r"(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|::1)")  # Improved regex
            if not ipv6_regex.match(ipv6_address):
                print("Invalid IPv6 format. Please enter a valid IPv6 address.")
                continue
            
            mac_address = get_mac_address(ipv6_address)
            
            if mac_address:
                print_info(ipv6_address, mac_address)
            else:
                print(f"Could not extract a valid MAC address for the IPv6 address: {ipv6_address}")
        
        elif choice == '2':
            # Get all valid IPv6 addresses from the 'ndp -a' command
            ipv6_addresses = get_valid_ipv6_and_mac_addresses()
            
            if ipv6_addresses:
                print("\nList of valid IPv6 addresses:")
                for idx, entry in enumerate(ipv6_addresses, 1):
                    print(f"{idx}. {entry['IPv6 Address']}")
                
                # Ask the user to choose an address
                try:
                    selection = int(input("\nEnter the number of the IPv6 address you want to query (or type '0' to cancel): "))
                    
                    if selection == 0:
                        print("Operation cancelled.")
                        continue
                    
                    if 1 <= selection <= len(ipv6_addresses):
                        ipv6_address = ipv6_addresses[selection - 1]['IPv6 Address']
                        mac_address = ipv6_addresses[selection - 1]['MAC Address']
                        print_info(ipv6_address, mac_address)
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                print("No valid IPv6 addresses found.")
        
        elif choice == '3':
            # Get all valid IPv6 addresses and MAC addresses from the 'ndp -a' command
            valid_addresses = get_valid_ipv6_and_mac_addresses()
            
            if valid_addresses:
                print("\nList of valid IPv6 and MAC addresses:")
                for entry in valid_addresses:
                    print(f"IPv6 Address: {entry['IPv6 Address']} | MAC Address: {entry['MAC Address']}")
            else:
                print("No valid IPv6 addresses found.")
        
        elif choice == '4':
            print("Exiting the script.")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
