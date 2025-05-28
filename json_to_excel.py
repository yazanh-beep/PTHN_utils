import json
import pandas as pd
import sys
from pathlib import Path

def convert_json_to_excel(json_file, excel_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, dict):
        print("❌ Error: JSON must be a dictionary with site names as keys.")
        return

    rows = []
    for site, entries in data.items():
        if isinstance(entries, list):
            for entry in entries:
                entry_with_site = {"site": site, **entry}
                rows.append(entry_with_site)
        else:
            print(f"⚠️ Skipped {site}: not a list of entries.")

    df = pd.DataFrame(rows)
    df.to_excel(excel_file, index=False)
    print(f"✅ Excel saved to {excel_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 json_to_excel.py input.json output.xlsx")
        sys.exit(1)

    convert_json_to_excel(sys.argv[1], sys.argv[2])
