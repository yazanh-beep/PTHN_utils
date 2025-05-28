import json
import os
import sys

def merge_json_files(input_dir, output_file):
    merged_data = {}

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(input_dir, filename)
            key = os.path.splitext(filename)[0]  # remove .json extension

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = json.load(f)

                if not isinstance(content, list):
                    print(f"❌ Skipped (not a list): {filename}")
                    continue

                merged_data[key] = content
                print(f"✔ Merged: {filename}")

            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2)

    print(f"\n✅ Merged JSON written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_json_folder.py <input_folder> <output_file.json>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_file = sys.argv[2]

    merge_json_files(input_folder, output_file)
