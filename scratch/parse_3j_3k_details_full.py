import re

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

def parse_full_defect(defect_id):
    pattern = rf'####\s+Defect\s+`{defect_id}`:\s+([^\n]+)(.*?)(?=####\s+Defect|\n###|\Z)'
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        # try without backticks
        pattern = rf'####\s+Defect\s+{defect_id}:\s+([^\n]+)(.*?)(?=####\s+Defect|\n###|\Z)'
        m = re.search(pattern, text, re.DOTALL)
    if m:
        title = m.group(1).strip()
        body = m.group(2).strip()
        sev = re.search(r'\*\*Severity:\*\*\s+([^\n]+)', body)
        module = re.search(r'\*\*Module / Feature:\*\*\s+([^\n]+)', body)
        endpoints = re.search(r'\*\*Affected Endpoints:\*\*\s+([^\n]+)', body)
        target_col = re.search(r'\*\*Target Collection:\*\*\s+([^\n]+)', body)
        evid_files = re.findall(r'evidence_\d+[^)\s]*\.(?:png|jpg)', body)
        
        # Problem description summary
        prob_m = re.search(r'#####\s+1\.\s+Problem Description[^\n]*\n(.*?)(?=#####|\Z)', body, re.DOTALL)
        prob = prob_m.group(1).strip() if prob_m else ""
        
        return {
            "id": defect_id,
            "title": title,
            "sev": sev.group(1).strip() if sev else "P1 Critical",
            "module": module.group(1).strip() if module else "Shifts & Rotation",
            "endpoints": endpoints.group(1).strip() if endpoints else "",
            "collection": target_col.group(1).strip() if target_col else "Sahab.ERP.Attendance.WorkPlans",
            "evidence": list(dict.fromkeys(evid_files)),
            "desc": prob
        }
    return None

print("=== PART 3J DEFECTS ===")
for i in range(1, 14):
    d_id = f"DEFECT-20261112-{i:02d}"
    info = parse_full_defect(d_id)
    if info:
        print(f"[{d_id}] Sev: {info['sev']} | Mod: {info['module']}")
        print(f"  Title: {info['title']}")
        print(f"  Endpoints: {info['endpoints']}")
        print(f"  Evidences: {info['evidence']}")
        print()

print("=== PART 3K DEFECTS ===")
for i in range(1, 5):
    d_id = f"DEFECT-20261114-{i:02d}"
    info = parse_full_defect(d_id)
    if info:
        print(f"[{d_id}] Sev: {info['sev']} | Mod: {info['module']}")
        print(f"  Title: {info['title']}")
        print(f"  Endpoints: {info['endpoints']}")
        print(f"  Evidences: {info['evidence']}")
        print()
    else:
        print(f"[{d_id}] Not found by parse_full_defect, searching in text...")
        pos = text.find(d_id)
        if pos != -1:
            print("  Found in text at pos:", pos)
            print("  Context:", text[pos:pos+300])
