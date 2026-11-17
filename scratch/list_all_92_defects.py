# -*- coding: utf-8 -*-
import json
import re

# Let's inspect the files that defined rows 41 to 92
files = [
    'scratch/update_confluence_part3i.py',
    'scratch/append_part3j_3k_confluence.py',
    'scratch/add_part3n_confluence.py',
    'scratch/add_part3p_confluence.py',
    'scratch/add_part3q_confluence.py'
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as fp:
            c = fp.read()
            matches = re.findall(r'["\']row["\']:\s*(\d+),\s*["\']id["\']:\s*["\']([^"\']+)["\']', c)
            print(f"{f}: found {len(matches)} rows -> {matches}")
    except Exception as e:
        print(f"Error reading {f}: {e}")
