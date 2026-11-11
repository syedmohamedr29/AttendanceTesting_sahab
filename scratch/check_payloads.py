import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, './scratch')

from test_suite_builder import create_test_suite
from build_post_break import build_post_break_tcs
from build_post_grace import build_post_grace_tcs
from build_post_overtime import build_post_overtime_tcs
from build_get_tcs import build_get_tcs
from build_patch_tcs import build_patch_tcs
from build_delete_tcs import build_delete_tcs
from build_bva_ep_tcs import build_bva_ep_tcs
from build_business_tcs import build_business_tcs

all_tcs = create_test_suite() + build_post_break_tcs() + build_post_grace_tcs() + build_post_overtime_tcs() + build_get_tcs() + build_patch_tcs() + build_delete_tcs() + build_bva_ep_tcs() + build_business_tcs()

print(f"Total TCs in all builder modules: {len(all_tcs)}")

with_tenant = [t for t in all_tcs if "tenantName" in t.get("Request Payload", "") or "tenantId" in t.get("Request Payload", "")]
print(f"TCs with tenantName/tenantId in Request Payload: {len(with_tenant)}")
for t in with_tenant:
    print(t["Test Case ID"], t["Test Scenario"], t["Request Payload"][:100])

with_id = [t for t in all_tcs if '"id"' in t.get("Request Payload", "") and t["HTTP Method"] == "POST"]
print(f"POST TCs with 'id' in Request Payload: {len(with_id)}")
for t in with_id:
    print(t["Test Case ID"], t["Test Scenario"], t["Request Payload"][:100])

