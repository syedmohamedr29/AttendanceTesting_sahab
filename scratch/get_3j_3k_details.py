import re

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

def extract_defect_info(defect_id):
    pattern = rf'####\s+Defect\s+`{defect_id}`:\s+([^\n]+)(.*?)(?=####\s+Defect|\n###|\Z)'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        title = m.group(1).strip()
        body = m.group(2).strip()
        # extract severity, endpoints, visual evidence
        sev = re.search(r'\*\*Severity:\*\*\s+([^\n]+)', body)
        module = re.search(r'\*\*Module / Feature:\*\*\s+([^\n]+)', body)
        endpoints = re.search(r'\*\*Affected Endpoints:\*\*\s+([^\n]+)', body)
        evidence = re.findall(r'\[Evidence[^\]]*\]\([^)]+\)', body)
        
        # summary / problem description
        prob = re.search(r'#####\s+1\.\s+Problem Description[^\n]*\n(.*?)(?=#####|\Z)', body, re.DOTALL)
        prob_text = prob.group(1).strip()[:200] if prob else body[:200]
        
        return {
            "id": defect_id,
            "title": title,
            "severity": sev.group(1).strip() if sev else "P1 Critical",
            "module": module.group(1).strip() if module else "Shifts & Rotation",
            "endpoints": endpoints.group(1).strip() if endpoints else "",
            "evidence": evidence,
            "snippet": prob_text
        }
    return None

print("=== PART 3J DEFECTS ===")
for i in range(1, 14):
    d_id = f"DEFECT-20261112-{i:02d}"
    info = extract_defect_info(d_id)
    if info:
        print(f"{info['id']}: {info['title'][:60]} | Sev: {info['severity'][:15]} | Evid: {len(info['evidence'])}")
    else:
        print(f"{d_id}: NOT FOUND")

print("\n=== PART 3K DEFECTS ===")
for i in range(1, 5):
    d_id = f"DEFECT-20261114-{i:02d}"
    info = extract_defect_info(d_id)
    if info:
        print(f"{info['id']}: {info['title'][:60]} | Sev: {info['severity'][:15]} | Evid: {len(info['evidence'])}")
    else:
        print(f"{d_id}: NOT FOUND")
