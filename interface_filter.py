import json
import os
import sys

# Additional ports to always exclude
EXCLUDED_PORTS = {"pv", "CPU", "for"}

def refine_json_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"❌ Skipped (not a list): {input_path}")
        return

    # Step 1: Collect ports associated with VLAN 100
    vlan_100_ports = {entry["port"] for entry in data if entry.get("vlan") == "100"}

    # Step 2: Combine with excluded ports
    ports_to_remove = vlan_100_ports.union(EXCLUDED_PORTS)

    # Step 3: Filter out any entries that use those ports
    filtered = [entry for entry in data if entry.get("port") not in ports_to_remove]

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, indent=2)

    print(f"✔ {os.path.basename(input_path)} → {os.path.basename(output_path)} (removed {len(data) - len(filtered)} entries)")

def batch_refine_json(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            in_path = os.path.join(input_dir, filename)
            out_path = os.path.join(output_dir, filename)
            refine_json_file(in_path, out_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python refine_vlan100_ports.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    batch_refine_json(input_folder, output_folder)
