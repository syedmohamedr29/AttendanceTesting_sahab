import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os
import uuid
import pymongo
from bson.binary import Binary

def generate_all_rotation_reports():
    results_path = "scratch/rotation_test_suite_results.json"
    if not os.path.exists(results_path):
        print("Results file not found yet!")
        return

    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    print(f"Loaded {len(results)} rotation test results.")

    # Categorize tests
    pos_post = [t for t in results if t["category"] == "Positive POST"]
    pos_patch = [t for t in results if t["category"] == "Positive PATCH"]
    neg_tests = [t for t in results if "Negative" in t["category"]]
    bva_tests = [t for t in results if t["category"] == "BVA Boundary"]

    total = len(results)
    passed = len([t for t in results if t["passed"]])
    failed = len([t for t in results if not t["passed"]])

    print(f"Summary: Total={total}, Passed={passed}, Failed={failed}")

    # Inspect defects / failures
    defects_caught = []
    for t in results:
        # A test is a defect if:
        # 1) It failed an expected assertion (e.g. expected 400 for invalid recurrence, but got 200 OK -> Validation Bypass!)
        # 2) Or it's a known bug where the server allowed an invalid state
        if not t["passed"]:
            defects_caught.append(t)
        elif t["actual_status"] == 200 and ("Negative" in t["category"] or "BVA" in t["category"]):
            defects_caught.append(t)

    print(f"Potential defects / anomalies identified: {len(defects_caught)}")
    for d in defects_caught:
        print(f"  [{d['test_id']}] Exp={d['expected_status']} Act={d['actual_status']} | {d.get('notes')}")

if __name__ == "__main__":
    generate_all_rotation_reports()
