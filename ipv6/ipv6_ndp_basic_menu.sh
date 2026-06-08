#!/bin/bash

# Function to display the menu
display_menu() {
    echo "----------------------------------"
    echo "        IPv6 Network Tools"
    echo "----------------------------------"
    echo "1. Show NDP Cache (ndp -a)"
    echo "2. Ping IPv6 Address (ping6)"
    echo "3. Exit"
    echo "----------------------------------"
}

# Loop for the menu
while true; do
    display_menu
    read -p "Please choose an option (1-3): " choice
    
    case $choice in
        1)
            echo "Showing NDP Cache..."
            ndp -a
            read -p "Press Enter to continue..."
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
