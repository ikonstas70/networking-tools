import subprocess
import time

session_name = "telnet_session"
ip = "10.178.226.200"
start_port = 2301
num_sessions = 10

# Start new detached tmux session with first telnet (2301)
subprocess.run([
    "tmux", "new-session", "-d", "-s", session_name,
    f"telnet {ip} {start_port}"
])

# Create remaining 9 panes (2302 to 2310)
for i in range(1, num_sessions):
    port = start_port + i
    # Every 5 panes, split vertically (new row)
    if i % 5 == 0:
        subprocess.run([
            "tmux", "split-window", "-t", session_name,
            "-v",
            f"telnet {ip} {port}"
        ])
    else:
        subprocess.run([
            "tmux", "split-window", "-t", session_name,
            "-h",
            f"telnet {ip} {port}"
        ])
    time.sleep(0.2)

# Arrange panes in tiled layout
subprocess.run([
    "tmux", "select-layout", "-t", session_name, "tiled"
])

# Do NOT enable synchronized input by default
# Attach to the tmux session
subprocess.run([
    "tmux", "attach-session", "-t", session_name
])
