"""
🔰 Imports
python
Copy
Edit
import xml.etree.ElementTree as ET
import re
xml.etree.ElementTree: Built-in library to parse and traverse XML documents.

re: Regular expressions module for cleaning MAC address formatting.

🔧 Function: Normalize MAC Address Format
python
Copy
Edit
def normalize_mac(mac):
    mac = mac.upper().replace("-", ":")
    mac = re.sub(r'[^0-9A-F:]', '', mac)
    return mac
Purpose: Standardize MAC address format for reliable comparison.

Converts MAC to uppercase.

Replaces dashes (-) with colons (:).

Removes anything that’s not a hex digit or colon (extra whitespace, stray characters, etc.).

📥 Read MAC List from File
python
Copy
Edit
with open("mac_list.txt") as f:
    mac_list = set(normalize_mac(line.strip()) for line in f if line.strip())
Opens mac_list.txt and reads each line.

strip() removes whitespace.

normalize_mac() is applied to each MAC.

set(...) is used to remove duplicates and allow fast membership lookup.

📝 Example: If file contains:

mathematica
Copy
Edit
00:18:08:00:53:CC
00-1A-2B-3C-4D-5E
They will both be normalized to a common format like:

mathematica
Copy
Edit
00:18:08:00:53:CC
00:1A:2B:3C:4D:5E
📂 Parse the Nmap XML File
python
Copy
Edit
tree = ET.parse("myscan.xml")
root = tree.getroot()
Loads the Nmap XML scan file (myscan.xml) into memory.

tree.getroot() gives access to the top-level <nmaprun> element.

📊 Loop Through Each Host Entry in the Scan
python
Copy
Edit
results = []

for host in root.findall("host"):
    ip = None
    mac = None
root.findall("host"): Finds each scanned device.

Initializes ip and mac as None for each device.

📡 Extract IP and MAC Addresses for the Host
python
Copy
Edit
    for addr in host.findall("address"):
        addr_type = addr.get("addrtype")
        addr_val = addr.get("addr")

        if addr_type == "ipv4":
            ip = addr_val
        elif addr_type == "mac":
            mac = normalize_mac(addr_val)
Each <host> can have multiple <address> elements.

Checks if the address is an IPv4 or MAC.

If MAC is found, it’s normalized for comparison.

If both IP and MAC are found, they're stored.

✅ Match MAC with List & Collect Result
python
Copy
Edit
    if mac and mac in mac_list:
        results.append((mac, ip))
If the current host's MAC exists in the input list, append it (with IP) to the results.

🖨️ Print Results or Notify if None Found
python
Copy
Edit
if results:
    for mac, ip in results:
        print(f"{mac} => {ip}")
else:
    print("No matching MAC addresses found.")
If matches were found, prints each MAC => IP.

If none found, shows a fallback message."""
import xml.etree.ElementTree as ET
import re

# Helper to normalize MAC addresses (keep uppercase, use colons)
def normalize_mac(mac):
    mac = mac.upper().replace("-", ":")
    mac = re.sub(r'[^0-9A-F:]', '', mac)
    return mac

# Load MACs from list
with open("mac_list.txt") as f:
    mac_list = set(normalize_mac(line.strip()) for line in f if line.strip())

# Parse Nmap XML
tree = ET.parse("myscan.xml")
root = tree.getroot()

# Collect results
results = []

for host in root.findall("host"):
    ip = None
    mac = None

    for addr in host.findall("address"):
        addr_type = addr.get("addrtype")
        addr_val = addr.get("addr")

        if addr_type == "ipv4":
            ip = addr_val
        elif addr_type == "mac":
            mac = normalize_mac(addr_val)

    if mac and mac in mac_list:
        results.append((mac, ip))

# Output
if results:
    for mac, ip in results:
        print(f"{mac} => {ip}")
else:
    print("No matching MAC addresses found.")
