# Sahab ERP Attendance – Rotation Work Template Equivalence Partitioning & Boundary Value Analysis

**Execution Date:** `2026-11-10`

| Test ID | Boundary Tested | Input Value | Expected Status | Actual Status | Result | Error Code / Boundary Observed |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `ROT-B01` | RecurrenceOfMonth index [0] | `2400` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` |
| `ROT-B02` | RecurrenceOfMonth index [6] | `2400` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` |
| `ROT-B03` | DayEnum numeric 0 | `2400` | `400` | `400` | ✅ PASS | `Cit.Attendance:2033` |
| `ROT-B04` | DayEnum numeric 8 | `2400` | `400` | `400` | ✅ PASS | `Cit.Attendance:2032` |
| `ROT-B05` | 0 duration on all working days | `0` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` |
| `ROT-B06` | 1441m (>24h) daily duration | `7205` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` |
| `ROT-B07` | Continuous 10,080m weekly duration | `10080` | `[200, 400]` | `400` | ✅ PASS | `Cit.Attendance:Validation` |
| `ROT-B08` | TotalWorkingDays = 8 | `2400` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` |
| `ROT-B09` | TotalDaysOff = -1 | `2400` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` |
| `ROT-B10` | TotalDaysOff = 8 | `0` | `400` | `400` | ✅ PASS | `Cit.Attendance:2034` |
| `ROT-B11` | Int32 overflow duration | `2147483648` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` |