#!/bin/bash

# Function to display the menu
display_menu() {
    echo "----------------------------------"
    echo "        IPv6 Network Tools"
    echo "----------------------------------"
    echo "1. Show NDP Cache with Detailed Info"
    echo "2. Ping IPv6 Address (ping6)"
    echo "3. Exit"
    echo "----------------------------------"
}

# Function to explain IPv6 NDP Cache
explain_ipv6_ndp() {
    echo "Showing NDP Cache with Detailed Information..."

    # Display the NDP cache
    ndp -a

    # Parse the NDP cache output to provide detailed explanation
    echo
    echo "Detailed Information for IPv6 Entries:"
    
    # Use awk to extract relevant parts and explain them
    ndp -a | while read -r line; do
        # Example parsing for IPv6 Address, MAC Address, and Interface
        if [[ $line =~ ([a-f0-9:]+)[[:space:]]+([0-9a-fA-F]{2}([:][0-9a-fA-F]{2}){5})[[:space:]]+([a-zA-Z0-9]+) ]]; then
            ipv6_address=${BASH_REMATCH[1]}
            mac_address=${BASH_REMATCH[2]}
            interface=${BASH_REMATCH[3]}
            
            echo "IPv6 Address: $ipv6_address"
            echo "Associated MAC Address: $mac_address"
            echo "Interface: $interface"

            # Provide an explanation of the MAC address and IPv6 address
            echo "Explanation:"
            echo "  - The IPv6 address is a unique identifier for the device in the network."
            echo "  - The MAC address is the physical address of the device's network interface."
            echo "  - In IPv6, the MAC address can be embedded within the IPv6 address, typically in the 'Interface Identifier' part."
            echo "    For example, the last 64 bits of the address are often derived from the MAC address."
            echo "    This helps in identifying the device across networks, making it useful for troubleshooting and network management."

            # (Optional) Add more detailed analysis, such as EUI-64, or common IPv6 standards here
            echo "Standard Explanation (EUI-64):"
            echo "  - If the IPv6 address follows the EUI-64 format, the MAC address is transformed to create the Interface Identifier."
            echo "  - This is typically achieved by inserting the hex value 'FFFE' in the middle of the MAC address."
            echo "  - Example transformation: If MAC is '00:1A:2B:3C:4D:5E', the IPv6 Interface Identifier would be '001A:2BFF:FE3C:4D5E'."
            echo

        fi
    done

    read -p "Press Enter to continue..."
}

# Loop for the menu
while true; do
    display_menu
    read -p "Please choose an option (1-3): " choice
    
    case $choice in
        1)
            explain_ipv6_ndp
            ;;
        2)
            read -p "Enter IPv6 Address to ping: " ipv6_address
            echo "Pinging IPv6 address $ipv6_address..."
            ping6 "$ipv6_address"
            read -p "Press Enter to continue..."
            ;;
        3)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please select 1, 2, or 3."
            read -p "Press Enter to try again..."
            ;;
    esac
done
