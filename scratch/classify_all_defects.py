import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

def section_lower_ep(sec):
    m = re.search(r'\*\*API Endpoints?\*\*\s*\|\s*([^\n|]+)', sec)
    return m.group(1).lower() if m else ""

# Extract all defect detail sections:
pattern = r'###\s*<a id="([^"]+)"></a>[🔴🟡🟢🟠\s]*([A-Z0-9\-]+):\s*([^\n]+)'
sections = re.findall(pattern, text)
print(f"Found {len(sections)} defect sections with anchors.")

policy_defects = []
for anchor, did, title in sections:
    idx = text.find(f'id="{anchor}"')
    next_idx = text.find('### <a id=', idx + 20)
    section_text = text[idx:next_idx] if next_idx != -1 else text[idx:idx+4000]
    
    text_lower = (title + " " + section_text).lower()
    ep = section_lower_ep(section_text)
    
    is_policy = False
    if '/attpolicies' in ep or 'attendance policy' in text_lower or 'attpolicies' in text_lower:
        is_policy = True
            
    if is_policy:
        ot = 'overtime' in text_lower
        brk = 'break' in text_lower
        grc = 'grace' in text_lower
        policy_defects.append({
            'id': did,
            'title': title.strip(),
            'ot': ot,
            'brk': brk,
            'grc': grc,
            'ep': ep
        })

print(f"\nTotal Policy Defects identified: {len(policy_defects)}")
for p in policy_defects:
    tags = []
    if p['ot']: tags.append("Overtime")
    if p['brk']: tags.append("Break")
    if p['grc']: tags.append("GracePeriod")
    print(f"- {p['id']}: [{', '.join(tags)}] | EP: {p['ep']} | {p['title']}")
