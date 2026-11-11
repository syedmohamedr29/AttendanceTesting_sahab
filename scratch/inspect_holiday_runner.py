import sys
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['scratch/run_full_holiday_suite.py', 'scratch/execute_all_310_holiday_tests.py']:
    print(f"=== {fname} ===")
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            print(f.read()[:2000])
    except Exception as e:
        print("Error:", e)

