"""
JSON Splitter Script
1. Purpose
This script takes a single large JSON file and breaks it into multiple smaller JSON files:

If the top-level JSON is an array, each element becomes its own file named 0001.json, 0002.json, etc.

If the top-level JSON is an object (dict), each key/value pair is written to <key>.json (the key is sanitized for safe filenames).

2. Configuration & Invocation
bash
Copy
Edit
python3 split_json.py big.json output_folder
big.json: Path to your input JSON file.

output_folder: Directory where individual JSON files will be created. It will be created if it doesn’t already exist.

3. Main Steps
Load JSON

python
Copy
Edit
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
Reads and parses the entire input file into data.

Type Check

python
Copy
Edit
if isinstance(data, list):
    # handle array
elif isinstance(data, dict):
    # handle object
else:
    # error
Determines whether data is a Python list, dict, or something else.

List Handling

python
Copy
Edit
for idx, entry in enumerate(data, start=1):
    filename = f"{idx:04d}.json"
    json.dump(entry, out, indent=2, ensure_ascii=False)
Iterates through each element (entry) in the list.

Names files with zero-padded indices: 0001.json, 0002.json, …

Writes each element as pretty-printed JSON.

Dict Handling

python
Copy
Edit
for key, entry in data.items():
    safe = sanitize_filename(str(key))
    filename = f"{safe}.json"
    json.dump(entry, out, indent=2, ensure_ascii=False)
Iterates through each key/value in the dict.

Uses sanitize_filename() to replace any characters invalid in filenames (e.g., spaces or slashes) with underscores.

Writes each value as pretty-printed JSON to <safe_key>.json.

Unsupported Types

python
Copy
Edit
else:
    print(f"❌ Unsupported top-level JSON type: {type(data).__name__}")
    sys.exit(1)
If data is neither list nor dict (e.g., a string or number), the script exits with an error.

4. Helper: Filename Sanitization
python
Copy
Edit
def sanitize_filename(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9_-]', '_', name)
Replaces any character not alphanumeric, underscore, or hyphen with an underscore.

Ensures keys like "User/Data" become safe filenames like User_Data.json.

5. Error Handling & Feedback
Creates the output directory if missing:

python
Copy
Edit
os.makedirs(output_dir, exist_ok=True)
Prints a confirmation (✔ Wrote ...) for each file it writes.

On improper usage (len(sys.argv) != 3), shows a usage message and exits.

6. Example
bash
Copy
Edit
# Suppose big.json is:
# {
#   "switch1": { ... },
#   "switch2": { ... }
# }

mkdir entries
python3 split_json.py big.json entries
Output directory entries/ will contain:

pgsql
Copy
Edit
entries/
├─ switch1.json
└─ switch2.json

"""
import json
import os
import sys
import re

def sanitize_filename(name: str) -> str:
    # remove any path chars, keep alphanumerics, - and _
    return re.sub(r'[^A-Za-z0-9_-]', '_', name)

def split_json(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list):
        # array: name files numerically
        for idx, entry in enumerate(data, start=1):
            filename = f"{idx:04d}.json"
            path = os.path.join(output_dir, filename)
            with open(path, 'w', encoding='utf-8') as out:
                json.dump(entry, out, indent=2, ensure_ascii=False)
            print(f"✔ Wrote {path}")

    elif isinstance(data, dict):
        # object: one file per key
        for key, entry in data.items():
            safe = sanitize_filename(str(key))
            filename = f"{safe}.json"
            path = os.path.join(output_dir, filename)
            with open(path, 'w', encoding='utf-8') as out:
                json.dump(entry, out, indent=2, ensure_ascii=False)
            print(f"✔ Wrote {path}")

    else:
        print(f"❌ Unsupported top‐level JSON type: {type(data).__name__}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python split_json.py <big.json> <output_folder>")
        sys.exit(1)

    big_json = sys.argv[1]
    folder   = sys.argv[2]
    split_json(big_json, folder)
