import os
import re
from collections import defaultdict

files_to_check = [
    'Defects/Attendance2_Master_Defect_Log.md',
    'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md',
    'Defects/REGULAR_WORK_PLAN_DEFECTS.md',
    'Defects/ROTATION_WORK_TEMPLATE_DEFECTS.md',
    'Defects/WORK_TEMPLATE_DEFECTS.md',
    'Defects/WORK_TEMPLATE_DELETE_DEFECTS.md'
]

print("=== 1. AUDITING DEFECT IDS ACROSS ALL FILES ===")

defect_pattern = re.compile(r'DEFECT-\d{8}-\d{2}')

file_defects = {}
all_defects = defaultdict(list)

for filepath in files_to_check:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Find all defect IDs mentioned
    matches = set(defect_pattern.findall(text))
    file_defects[filepath] = matches
    for d in matches:
        all_defects[d].append(filepath)

print(f"Total unique DEFECT-YYYYMMDD-XX IDs found: {len(all_defects)}")

# 2. Check for duplicate section definitions in Master Defect Log
print("\n=== 2. CHECKING DUPLICATE SECTION DEFINITIONS IN MASTER DEFECT LOG ===")
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_text = f.read()

# Match headings like ### <a id="..."></a>... DEFECT-YYYYMMDD-XX: or #### Defect `DEFECT-...`
master_defs = re.findall(r'(?:### <a id="[^"]+"></a>.*?|#### Defect `)(DEFECT-\d{8}-\d{2})', master_text)
def_counts = defaultdict(int)
for d in master_defs:
    def_counts[d] += 1

duplicate_defs = {k: v for k, v in def_counts.items() if v > 1}
print(f"Defect IDs with multiple definition headers in Master Log: {len(duplicate_defs)}")
for k, v in duplicate_defs.items():
    print(f"  {k}: defined {v} times")

# 3. Check for duplicate section definitions in Inconsistencies Report
print("\n=== 3. CHECKING DUPLICATE SECTION DEFINITIONS IN INCONSISTENCIES REPORT ===")
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    report_text = f.read()

report_defs = re.findall(r'(?:### <a id="[^"]+"></a>.*?|#### Defect `|### Defect `)(DEFECT-\d{8}-\d{2})', report_text)
report_counts = defaultdict(int)
for d in report_defs:
    report_counts[d] += 1

report_duplicate_defs = {k: v for k, v in report_counts.items() if v > 1}
print(f"Defect IDs with multiple definition headers in Report: {len(report_duplicate_defs)}")
for k, v in report_duplicate_defs.items():
    print(f"  {k}: defined {v} times")

# 4. Check known Aliased / Duplicate Concepts
print("\n=== 4. AUDITING CONCEPTUAL / ROOT-CAUSE DUPLICATES ===")
concepts = {
    "TenantName Empty Object": ['DEFECT-20261026-02', 'DEFECT-20261028-05', 'DEFECT-20261103-02', 'DEFECT-20261105-04', 'USER-02', 'USER-129'],
    "TenantName Exposed in DTO / Client Spoofing": ['DEFECT-20261026-04', 'DEFECT-20261028-06', 'DEFECT-20261105-02', 'USER-04', 'USER-122', 'USER-131'],
    "CreatedBy Plain Email String": ['DEFECT-20261026-03', 'DEFECT-20261103-01', 'USER-03', 'USER-130'],
    "CompanyChecklist Sync Failure": ['DEFECT-20261026-01', 'USER-01', 'USER-128'],
    "Cross-Tenant Scoping Leak (__tenant ignored)": ['DEFECT-20261104-01', 'DOC-A-04', 'ROOT-E-05'],
    "Cross-Company Scoping Fallback (200 [])": ['DEFECT-20261028-04', 'DOC-A-05', 'ROOT-E-06'],
    "CompanyName Empty Object in Mongo": ['DEFECT-20261105-01'],
    "Seeded Location WT Missing Arabic Name": ['DEFECT-20261110-01'],
    "New Location Missing CDWT (Sync Gap)": ['DEFECT-20261103-16']
}

for concept, aliases in concepts.items():
    print(f"\nConcept: '{concept}'")
    print(f"  Related / Aliased Identifiers: {aliases}")

