import json
import os

EXCLUDED_PORTS = {"Gi1/1", "CPU", "Gi1/1/1", "Te1/1/1", "pv"}

def filter_json_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"❌ Skipped {input_path}: not a list")
        return

    filtered = [entry for entry in data if entry.get("port") not in EXCLUDED_PORTS]

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, indent=2)

    print(f"✔ {os.path.basename(input_path)} → {os.path.basename(output_path)} ({len(data) - len(filtered)} removed)")

def batch_filter_json(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            in_path = os.path.join(input_dir, filename)
            out_path = os.path.join(output_dir, filename)
            filter_json_file(in_path, out_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python batch_filter_mac_json.py input_folder output_folder")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    batch_filter_json(input_folder, output_folder)
