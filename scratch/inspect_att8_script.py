import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/execute_and_reverify_attendance8.py', 'r', encoding='utf-8') as f:
    text = f.read()

print(text[:1500])

