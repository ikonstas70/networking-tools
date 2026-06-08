import subprocess

base_ip = "10.178.226.200"
base_port = 2301
number_of_sessions = 10

# Build AppleScript command
applescript = 'tell application "Terminal"\n'
applescript += 'activate\n'

for i in range(number_of_sessions):
    port = base_port + i
    command = f'telnet {base_ip} {port}'
    if i == 0:
        # First session uses new window
        applescript += f'do script "{command}"\n'
    else:
        # Subsequent sessions open in new tabs
        applescript += f'do script "{command}" in (make new tab at the end of tabs of front window)\n'

applescript += 'end tell'

# Run AppleScript through osascript
subprocess.run(["osascript", "-e", applescript])
