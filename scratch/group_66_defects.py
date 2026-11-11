import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Get all unique defect IDs:
all_defects = sorted(list(set(re.findall(r'DEFECT-\d{8}-\d{2}', text))))
print(f"Total unique defect IDs: {len(all_defects)}")

groups = {
    "Attendance Policies (Overtime, Break, Grace Period)": [],
    "Work Templates (Fixed, Flexi, Split, CDWT, Roster)": [],
    "Holiday Calendars (Company, Location, Yearly)": [],
    "Work Plans & Assignments": [],
    "Cross-Service, Multi-Tenancy & Platform Architecture": []
}

for did in all_defects:
    # Find context of did
    pos = text.find(did)
    # search around pos
    ctx = text[max(0, pos-200):min(len(text), pos+600)].lower()
    
    if any(k in ctx for k in ['attpolicies', 'overtime', 'break policy', 'grace period', 'rateformula', 'deviationthreshold', 'bufferbeforeovertime']):
        groups["Attendance Policies (Overtime, Break, Grace Period)"].append(did)
    elif any(k in ctx for k in ['holiday', 'calendar']):
        groups["Holiday Calendars (Company, Location, Yearly)"].append(did)
    elif any(k in ctx for k in ['workplan', 'work plan', 'assignment']):
        groups["Work Plans & Assignments"].append(did)
    elif any(k in ctx for k in ['worktemplate', 'work template', 'cdwt', 'template', 'shift', 'fixed', 'flexi', 'split']):
        groups["Work Templates (Fixed, Flexi, Split, CDWT, Roster)"].append(did)
    else:
        groups["Cross-Service, Multi-Tenancy & Platform Architecture"].append(did)

total_grouped = sum(len(v) for v in groups.values())
print(f"Total Grouped: {total_grouped}")
for g, items in groups.items():
    print(f"\n{g}: {len(items)} defects")
    print(", ".join(items))
