import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern for table rows in Master Defect Log:
# | [`DEFECT-YYYYMMDD-NN`](#anchor) | Severity | Module | Description | Endpoints | Evidence |
pattern = r'\|\s*\[`?(DEFECT-\d{8}-\d{2})`?\]\([^)]+\)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|'
matches = re.findall(pattern, text)

print(f"Total parsed defects: {len(matches)}")
module_counts = {}
for did, sev, mod, desc, ep in matches:
    mod_clean = mod.strip()
    module_counts[mod_clean] = module_counts.get(mod_clean, 0) + 1

print("\n--- DEFECT COUNT BY MODULE (Total = 66) ---")
for mod, count in sorted(module_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  * {mod:<50}: {count} defects")
