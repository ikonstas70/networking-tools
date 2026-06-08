#!/bin/bash

# Function to check if the IPv6 address is valid
is_valid_ipv6() {
    if [[ "$1" =~ ^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$ ]]; then
        return 0  # Valid IPv6
    else
        return 1  # Invalid IPv6
    fi
}

# Display detailed information about the IPv6 entry
show_ipv6_info() {
    echo "IPv6 Address: $1"
    echo "Associated MAC Address: $2"
    echo "Interface: $3"
    echo "Explanation:"
    echo "  - The IPv6 address is a unique identifier for the device in the network."
    echo "  - The MAC address is the physical address of the device's network interface."
    echo "  - In IPv6, the MAC address can be embedded within the IPv6 address, typically in the Interface Identifier."
    echo "    For example, the last 64 bits of the address are often derived from the MAC address."
    echo "    This helps in identifying the device across networks."
    echo "Standard Explanation (EUI-64):"
    echo "  - The MAC address is transformed to create the Interface Identifier using the EUI-64 format."
    echo "  - Example: If MAC is '00:1A:2B:3C:4D:5E', the Interface Identifier would be '001A:2BFF:FE3C:4D5E'."
}

# Menu and Loop
while true; do
    clear
    echo "===== NDP - IPv6 Menu ====="
    echo "1. Show Detailed Information for IPv6 Entries"
    echo "2. Ping an IPv6 Address"
    echo "3. Exit"
    read -p "Please select an option (1/2/3): " option

    case $option in
        1)
            read -p "Enter IPv6 address to show details: " ipv6_address
            # Example data; replace with real data
            associated_mac="be:62:3c:ff:99:f3"
            interface=":f3"

            if is_valid_ipv6 "$ipv6_address"; then
                show_ipv6_info "$ipv6_address" "$associated_mac" "$interface"
            else
                echo "Invalid IPv6 address entered."
            fi
            read -p "Press Enter to return to the menu..." enter_key
            ;;
        2)
            read -p "Enter IPv6 address to ping: " ipv6_address_to_ping
            if is_valid_ipv6 "$ipv6_address_to_ping"; then
                ping6 "$ipv6_address_to_ping"
            else
                echo "Invalid IPv6 address entered."
            fi
            read -p "Press Enter to return to the menu..." enter_key
            ;;
        3)
            echo "Exiting..."
            break
            ;;
        *)
            echo "Invalid option. Please try again."
            read -p "Press Enter to continue..." enter_key
            ;;
    esac
done
