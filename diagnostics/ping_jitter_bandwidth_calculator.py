import os
import subprocess
import math
import shutil
import speedtest

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def classify_jitter(jitter):
    """Classifies jitter into professional categories."""
    if jitter <= 5:
        return f"{GREEN}Excellent{RESET}"
    elif 6 <= jitter <= 20:
        return f"{YELLOW}Good{RESET}"
    elif 21 <= jitter <= 50:
        return f"{YELLOW}Fair{RESET}"
    else:
        return f"{RED}Poor{RESET}"

def get_selection(options, prompt="Choose an option: "):
    """Displays options and returns user selection."""
    print(prompt)
    for key, value in options.items():
        print(f"{key}. {value}")
    while True:
        try:
            selection = int(input(f"Choose an option (default {list(options.keys())[0]}): ") or list(options.keys())[0])
            return options.get(selection)
        except ValueError:
            print(f"{RED}Invalid input. Please enter a valid number.{RESET}")

def get_dns_options():
    """Returns a list of common DNS servers."""
    return {
        1: "8.8.8.8",  # Google DNS
        2: "1.1.1.1",  # Cloudflare DNS
        3: "9.9.9.9",  # Quad9 DNS
        4: "208.67.222.222",  # OpenDNS
        5: "custom"  # Option for custom input
    }

def get_packet_size_options():
    """Returns a list of common packet sizes."""
    return {
        1: 64,   # Default ICMP packet size
        2: 128,  # Slightly larger packet size
        3: 512,  # Medium packet size
        4: 1024, # Large packet size
        5: "custom"  # Option for custom size
    }

def get_interval_options():
    """Returns a list of common ping intervals."""
    return {
        1: 0.2,   # Fast pings
        2: 0.5,   # Medium-fast pings
        3: 1.0,   # Default interval
        4: 2.0,   # Slower pings
        5: "custom"  # Option for custom interval
    }

def test_bandwidth():
    """Test download and upload speed using speedtest-cli."""
    st = speedtest.Speedtest()
    st.get_best_server()  # Get the best server based on ping
    download_speed = st.download() / 1_000_000  # Convert from bps to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert from bps to Mbps
    ping = st.results.ping

    return download_speed, upload_speed, ping

def calculate_jitter():
    """Calculates jitter and other statistics based on user input."""
    while True:
        try:
            clear_screen()
            print("PING JITTER CALCULATOR")
            print("=" * 40)

            # DNS selection
            dns_options = get_dns_options()
            host = get_selection(dns_options, "Select a DNS target:")

            if host == "custom":
                host = input("Enter your custom DNS or host: ").strip()
            print(f"Target host selected: {host}")

            # Packet size selection
            packet_size_options = get_packet_size_options()
            packet_size = get_selection(packet_size_options, "\nSelect a packet size (in bytes):")

            if packet_size == "custom":
                packet_size = int(input("Enter a custom packet size in bytes: ").strip())
            print(f"Packet size selected: {packet_size} bytes")

            # Interval selection
            interval_options = get_interval_options()
            interval = get_selection(interval_options, "\nSelect a ping interval (in seconds):")

            if interval == "custom":
                interval = float(input("Enter a custom ping interval in seconds: ").strip())
            print(f"Ping interval selected: {interval} seconds")

            # Ping count input
            ping_count = int(input("\nEnter the number of pings (default 50): ") or 50)
            print(f"Number of pings selected: {ping_count}")

            # Prepare the ping command
            if os.name == "nt":  # Windows
                ping_command = f"ping -n {ping_count} -l {packet_size} {host}"
            else:  # Linux/Mac
                ping_command = f"ping -c {ping_count} -i {interval} -s {packet_size} {host}"

            try:
                # Run the ping command
                result = subprocess.run(ping_command, shell=True, capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"{RED}Error executing ping: {e}{RESET}")
                break

            # Extract response times
            times = []
            for line in result.stdout.splitlines():
                if "time=" in line:
                    try:
                        time = float(line.split("time=")[1].split()[0])
                        times.append(time)
                    except (IndexError, ValueError):
                        pass

            if len(times) < 2:
                print(f"{RED}Not enough data to calculate jitter. Please increase the number of pings.{RESET}")
                break

            # Calculate statistics
            count = len(times)
            avg = sum(times) / count
            sumsq = sum(t ** 2 for t in times)
            jitter = math.sqrt(sumsq / count - avg ** 2)
            min_time = min(times)
            max_time = max(times)
            std_dev = math.sqrt(sum((t - avg) ** 2 for t in times) / (count - 1)) if count > 1 else 0
            jitter_classification = classify_jitter(jitter)

            # Test bandwidth
            download_speed, upload_speed, ping = test_bandwidth()

            # Prepare results
            result_lines = [
                f"Target Host:         {host}",
                f"Ping Count:          {count}",
                f"Interval:            {interval:.2f} seconds",
                f"Packet Size:         {packet_size} bytes",
                f"Average Ping Time:   {avg:.2f} ms",
                f"Minimum Ping Time:   {min_time:.2f} ms",
                f"Maximum Ping Time:   {max_time:.2f} ms",
                f"Standard Deviation:  {std_dev:.2f} ms",
                f"Jitter:              {jitter:.2f} ms",
                f"Download Speed:      {download_speed:.2f} Mbps",
                f"Upload Speed:        {upload_speed:.2f} Mbps",
                f"Ping:                {ping} ms"
            ]

            # Dynamically calculate margins
            terminal_width = shutil.get_terminal_size().columns
            max_line_length = max(len(line) for line in result_lines + [f"Jitter Classification: {jitter_classification}"])
            max_width = min(max_line_length + 4, terminal_width - 4)

            # Generate output frame
            border = "+" + "-" * max_width + "+"
            print(border)
            print("|" + "PING JITTER RESULTS".center(max_width) + "|")
            print(border)
            for line in result_lines:
                print(f"| {line.ljust(max_width - 2)} |")
            print(border)
            print(f"| Jitter Classification: {jitter_classification.ljust(max_width - 24)} |")
            print(border)

            # Ask to repeat or quit
            repeat = input("\nDo you want to calculate again? (y/n): ").strip().lower()
            if repeat != 'y':
                clear_screen()
                print("Exiting. Thank you!")
                break

        except ValueError:
            print(f"{RED}Invalid input. Please enter valid numbers.{RESET}")
        except Exception as e:
            print(f"{RED}An unexpected error occurred: {e}{RESET}")
            break

if __name__ == "__main__":
    calculate_jitter()
