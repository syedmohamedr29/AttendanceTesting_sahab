import json
import requests

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

r = requests.get(f"{base_url}/rest/api/content/{page_id}/child/attachment?limit=100", auth=auth)
existing = [att["title"] for att in r.json().get("results", [])]

check_files = [
    "evidence_51_location_default_worktemplate_ar_name_empty_compass.png",
    "evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png",
    "evidence_53_cdwt_patch_sets_haspendinglocsync_true_not_auto_overwrite_compass.png",
    "evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png",
    "evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png",
    "evidence_56_flexi_split_location_validation_bypasses_and_db_results.png",
    "evidence_57_worktemplate_delete_lifecycle_and_bypasses.png",
    "evidence_58_rotation_worktemplate_lifecycle_and_defects.png"
]

for cf in check_files:
    print(f"{cf}: on Confluence = {cf in existing}")
