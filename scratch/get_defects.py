import re

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.finditer(r'### <a id="(defect-[^"]+)"></a>(.*?)(?=### <a id=|\Z)', text, re.DOTALL)
for m in matches:
    d_id = m.group(1)
    body = m.group(2)
    if any(k in d_id.lower() for k in ['20261104-01', '20261105-01', '20261110-01', '20261103-16']):
        print(f"******************** {d_id} ********************")
        print(body[:600])
        print("\n" + "="*50 + "\n")
