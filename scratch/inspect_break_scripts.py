import sys
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['scratch/capture_negative_break.py', 'scratch/test_break_negative.py', 'scratch/test_break_negative_array.py']:
    print(f"=== {fname} ===")
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print("Error:", e)

