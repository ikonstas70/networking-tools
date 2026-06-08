# Networking Tools

**Author:** Ioannis Konstas — IT Solutions USA

Python and shell scripts for network diagnostics organized into three groups: IPv6 and Neighbor Discovery Protocol tools, network diagnostic utilities, and multi-session terminal management.

---

## `ipv6/` — IPv6 & Neighbor Discovery Protocol

Tools for IPv6 address resolution and NDP neighbor cache inspection on macOS.

| Script | Description |
|---|---|
| `ipv6_to_mac_lookup.py` | Looks up the MAC address for a given IPv6 address using the macOS NDP neighbor cache |
| `ipv6_to_mac_lookup_advanced.py` | Interactive menu to query a specific IPv6/MAC pair, list all NDP neighbors, or bulk-dump the full neighbor cache |
| `ipv6_ndp_basic_menu.sh` | Shell menu for IPv6 NDP operations — view the full neighbor cache or ping an IPv6 address |
| `ipv6_ndp_detailed_menu.sh` | Same as above but explains each NDP cache entry including EUI-64 MAC-to-IPv6 derivation |
| `ipv6_ndp_validation_menu.sh` | NDP shell menu with IPv6 address format validation before accepting input |

**Requirements:** macOS with `ndp` available; `pip install tabulate` for the Python scripts.

---

## `diagnostics/` — Network Diagnostics & WHOIS

Latency measurement, bandwidth testing, DHCP inspection, and RIPE NCC IP lookups.

| Script | Description |
|---|---|
| `ping_jitter_calculator.py` | Measures network jitter — choose DNS target, packet size, and interval; outputs avg/min/max ping, **sample standard deviation** (σ, Bessel-corrected), and a quality rating |
| `ping_jitter_bandwidth_calculator.py` | Full network quality report — avg/min/max ping, **sample standard deviation** (σ), jitter quality rating, plus live download speed, upload speed, and speedtest ping via `speedtest-cli` |
| `macos_dhcp_lease_viewer.sh` | Displays the current DHCP lease table from `/private/var/db/dhcpd_leases` on macOS |
| `ripe_ncc_whois_lookup.sh` | Queries the RIPE NCC WHOIS database for any IP address and displays the result in a dynamically sized centered box |
| `ripe_ncc_whois_lookup_v2.sh` | Same as above with an added `help` option in the prompt explaining available commands |

**Understanding the Metrics**

Running a ping test produces several numbers. Here is what each one means and why it matters:

**Average (avg)** — The mean round-trip time across all packets sent, measured in milliseconds (ms). This is the baseline latency of your connection — how long it takes for a packet to travel to the target and back under normal conditions. Lower is better. Under 20 ms is excellent for local/regional targets; under 80 ms is acceptable for most internet traffic.

**Minimum (min)** — The fastest single round-trip recorded during the test. This represents the best-case physical latency of your path — the floor below which your connection cannot go regardless of how optimal conditions are. Comparing min to avg tells you how much overhead your network adds on top of the raw physical speed.

**Maximum (max)** — The slowest single round-trip recorded. A large gap between avg and max indicates periodic congestion, interference, or packet queuing on the path. For real-time applications, the max matters as much as the average — a 200 ms spike in the middle of a VoIP call is heard as a gap in speech.

**Jitter** — The variation in latency between consecutive packets. A connection with avg=20 ms and jitter=1 ms is smooth and predictable. A connection with avg=20 ms and jitter=40 ms is unstable — packets arrive at irregular intervals, causing audio/video to stutter even when the average looks acceptable. Jitter is the most important metric for VoIP, video conferencing, and online gaming.

**Standard Deviation (σ)** — A more precise measure of consistency than jitter alone. While jitter compares consecutive packets, standard deviation measures how much all latency samples spread around the average. A low σ means your connection is stable and consistent. A high σ means latency is unpredictable — some packets are fast, others slow, with no reliable pattern. This script uses the **sample standard deviation** formula (Bessel-corrected, dividing by n-1) which gives a statistically accurate result from a finite sample of pings.

**Quality Rating** — A composite interpretation of avg, jitter, and σ together. No single metric tells the full story: a low average with high standard deviation is still a poor connection for real-time traffic. The quality rating combines all three to give a plain-language assessment of whether the connection is suitable for latency-sensitive applications.

**Download / Upload Speed** — Measured via `speedtest-cli` against the nearest Speedtest server. Download is how fast data arrives at your machine; upload is how fast your machine sends. Both matter — slow upload degrades video calls and remote desktop even when download is fast.

**Speedtest Ping** — The ping reported by the Speedtest server, which may differ from the DNS ping measured above. The difference between the two reveals whether latency varies across paths to different endpoints on the internet.

**Requirements:** `pip install speedtest-cli` for bandwidth testing.

---

## `sessions/` — Multi-Session Terminal Management

Scripts for opening multiple simultaneous Telnet sessions across different terminal multiplexers.

| Script | Description |
|---|---|
| `telnet_multi_session_tmux.py` | Opens 10 simultaneous Telnet sessions on sequential ports (2301–2310) in a tiled tmux pane layout |
| `telnet_multi_tab_applescript.py` | Opens 10 Telnet sessions as individual tabs in the macOS Terminal app using AppleScript — no tmux required |

**Requirements:** `tmux` for the tmux version; macOS Terminal app for the AppleScript version.

---

*© Ioannis Konstas — IT Solutions USA*
