# Sahab ERP Attendance – Rotation Work Template Business & Architecture Validation

**Execution Date:** `2026-11-10`

## 1. Core Architectural Invariants Verified

1. **Location-Only Scoping:** The Rotation template is strictly a location-scoped template. Calling POST without `locationId` fails with `Cit.Attendance:Validation LocationId is required. Rotation work templates are location-level only.`

2. **Seven-Day Weekly Structure:** Unlike Flexible templates which allow arbitrary day configurations, Rotation templates mandate exactly 7 day slots covering Sun through Sat.

3. **Cross-Company Isolation Failure (`DEFECT-20261110-19`):** Calling `POST .../rotation?locationId={foreignLocationId}` from another tenant/company succeeds with HTTP 200 OK, corrupting location references across tenants.

4. **Immutability of Short Code on PATCH:** Updating `shortCode` via PATCH is rejected with `Cit.Attendance:1107 A work template's short code cannot be changed once created.`

5. **Audit Metadata Integrity:** Unlike Fixed templates where CreatedAt was wiped out to 0001-01-01, Rotation PATCH properly preserves `CreatedAt` and updates `ModifiedAt` and `ModifiedBy`.
