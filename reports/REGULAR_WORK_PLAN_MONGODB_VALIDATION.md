# Regular Work Plan — MongoDB Validation (`ERP.Attendance.WorkPlans`)

> **Database:** `Sahab` @ `10.1.0.4:27018` | **Company:** `Attendance 8` (`3a249871-7a8d-dec5-2d72-47795dd2662d`)

## Live Before / After MongoDB Snapshots (`ATT8 LOC1 Host 8d00c3e6-2652-463c-ad73-bb1e75b1de70`)

| Check ID | Operation | Expected DB Behavior | Before (`flags` / `PolIDs` / `WT`) | After (`flags` / `PolIDs` / `WT`) | Integrity Verdict |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `ATT8-BOOL-08` | All 3 policies enabled (PATCH-P02)  | `200 & DB flags=(True, True, True) Types=[1, 2, 3]` | `[True, False, False] / 1p / wt=1a80d87c(t=1)` | `[True, True, True] / 3p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-BOOL-07` | OT + Grace enabled, Break disabled  | `200 & DB flags=(False, True, True) Types=[2, 3]` | `[True, True, True] / 3p / wt=1a80d87c(t=1)` | `[False, True, True] / 2p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-BOOL-06` | Break + Grace enabled, OT disabled (POST-P08 equiv)  | `200 & DB flags=(True, False, True) Types=[1, 3]` | `[False, True, True] / 2p / wt=1a80d87c(t=1)` | `[True, False, True] / 2p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-BOOL-05` | Break + OT enabled, Grace disabled  | `200 & DB flags=(True, True, False) Types=[1, 2]` | `[True, False, True] / 2p / wt=1a80d87c(t=1)` | `[True, True, False] / 2p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-BOOL-04` | Grace Period ONLY enabled (PATCH-P04 / GRACE-01)  | `200 & DB flags=(False, False, True) Types=[3]` | `[True, True, False] / 2p / wt=1a80d87c(t=1)` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-BOOL-03` | Overtime ONLY enabled  | `200 & DB flags=(False, True, False) Types=[2]` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | `[False, True, False] / 1p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-BOOL-02` | Break ONLY enabled  | `200 & DB flags=(True, False, False) Types=[1]` | `[False, True, False] / 1p / wt=1a80d87c(t=1)` | `[True, False, False] / 1p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-BOOL-01` | All 3 policies disabled + policyIds=[] (PATCH-P03 / GRACE-03)  | `200 & DB flags=(False, False, False) Types=[]` | `[True, False, False] / 1p / wt=1a80d87c(t=1)` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-GRACE-02` | PATCH-P05 / GRACE-02: Grace=false + Grace Policy ID supplied  | `400 (or strips/blocks disabled policy ID)` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-GRACE-04` | GRACE-04: Grace=true + empty policyIds=[]  | `400 Validation Error` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-GRACE-05` | GRACE-05 (UUID format): Grace=true + invalid UUID string  | `400 Validation Error` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-GRACE-05B` | GRACE-05 (Nonexistent): Grace=true + unknown policy UUID  | `400/404 Policy Not Found` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-GRACE-06` | GRACE-06: Grace=true + Break Policy ID (wrong type!)  | `400 Wrong Policy Type` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-GRACE-07` | GRACE-07: Grace=true + foreign ATT7 policy ID  | `400/403/404 Cross-Company Policy` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-GRACE-08` | GRACE-08: Grace=true + duplicate Grace Policy ID [G, G]  | `400 Duplicate Policy ID` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | `[False, False, True] / 2p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-GRACE-INACT` | GRACE-Extra: Grace=true + Inactive Grace Policy ID  | `400 Inactive Policy` | `[False, False, True] / 2p / wt=1a80d87c(t=1)` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-GRACE-SWAP` | Grace Swap: Replace POL_GRC with POL_GRC2  | `200 DB swaps to POL_GRC2` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-BUS-FIXED` | Fixed workTemplate compatibility  | `200 (TemplateType=1 Fixed)` | `[False, False, True] / 1p / wt=1a80d87c(t=1)` | `[False, False, False] / 1p / wt=d5c7277e(t=1)` | ✅ Pass |
| `ATT8-BUS-FLEXI` | Flexible workTemplate compatibility on Regular plan  | `200 (TemplateType=2 Flexi)` | `[False, False, False] / 1p / wt=d5c7277e(t=1)` | `[False, False, False] / 1p / wt=b031ef4c(t=2)` | ✅ Pass |
| `ATT8-BUS-SPLIT` | Split workTemplate compatibility on Regular plan  | `200 (TemplateType=3 Split)` | `[False, False, False] / 1p / wt=b031ef4c(t=2)` | `[False, False, False] / 1p / wt=f5e044b1(t=3)` | ✅ Pass |
| `ATT8-BUS-ROT` | Rotation workTemplate (Type=5) on Regular plan (BUS-05 / PATCH-N28)  | `400 Incompatible Rotation template` | `[False, False, False] / 1p / wt=f5e044b1(t=3)` | `[False, False, False] / 1p / wt=c3f43025(t=5)` | ❌ Fail |
| `ATT8-BUS-ROST` | Roster workTemplate (Type=4) on Regular plan  | `400 Incompatible Roster template` | `[False, False, False] / 1p / wt=c3f43025(t=5)` | `[False, False, False] / 1p / wt=26681771(t=4)` | ❌ Fail |
| `ATT8-BUS-CROSSLOC` | WorkTemplate belonging to ATT8 LOC2 used in LOC1 plan  | `400 Cross-location template or Allowed` | `[False, False, False] / 1p / wt=26681771(t=4)` | `[False, False, False] / 1p / wt=7ecfbe95(t=1)` | ✅ Pass |
| `ATT8-BUS-CROSSCOMP` | WorkTemplate from ATT7 used on ATT8 plan  | `400/403/404 Cross-company template` | `[False, False, False] / 1p / wt=7ecfbe95(t=1)` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | ❌ Fail |
| `ATT8-BUS-DELETED` | Soft-deleted WorkTemplate used on ATT8 plan  | `400 Soft-deleted template` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | ✅ Pass |
| `ATT8-PATCH-N01` | 404/405 Missing ID in PATCH  | `404/405` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | ✅ Pass |
| `ATT8-PATCH-N02` | 400/404 Invalid PATCH ID  | `400/404` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | ✅ Pass |
| `ATT8-PATCH-N03` | 404 Nonexistent WorkPlan  | `404` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | ✅ Pass |
| `ATT8-PATCH-N04` | 400/404 Cross-company WorkPlan  | `400/404` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | ✅ Pass |
| `ATT8-PATCH-N05` | 400 Location mismatch LOC2 on LOC1 WP  | `400` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | ✅ Pass |
| `ATT8-PATCH-N06` | 400 Missing locationId  | `400` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | ✅ Pass |
| `ATT8-PATCH-N07` | 400 Invalid locationId  | `400` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | ✅ Pass |
| `ATT8-PATCH-N09` | 400 Null workPlanName  | `400` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | ❌ Fail |
| `ATT8-PATCH-N10` | 400 Empty English name  | `400` | `[False, False, False] / 1p / wt=5fe610ef(t=1)` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-PATCH-N11` | 400 Whitespace English name  | `400` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-PATCH-N13` | 400 Invalid workTemplateId  | `400` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-PATCH-N14` | 400/404 Nonexistent workTemplateId  | `400/404` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-PATCH-N19` | 400 Null policyIds  | `400` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-PATCH-N20` | 400 Invalid policyIds type string  | `400` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-PATCH-N21` | 400 String boolean  | `400` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | ✅ Pass |
| `ATT8-PATCH-N22` | 400 Explicit null boolean  | `400` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-PATCH-N26` | 400/404 Mutate deleted WorkPlan  | `400/404` | `[False, False, False] / 0p / wt=cf3ef115(t=1)` | `[False, False, False] / 0p / wt=1a80d87c(t=1)` | ❌ Fail |
| `ATT8-PATCH-N27` | 401 Unauthorized (no Bearer)  | `401` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | `[False, False, False] / 1p / wt=1a80d87c(t=1)` | ✅ Pass |