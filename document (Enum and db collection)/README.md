# Attendance 2: QA Handover

Reference documents for testing the Attendance 2 service (`SP.AttendanceSvc`) on DEV.

## What is deployed

| | |
|---|---|
| Environment | DEV |
| Release | `dev300-1.0.2`, built from `main` (includes the roster publish-periods work) |
| Deployed | 22 Oct 2026; DEV database migrated the same day |
| Base URL | `https://attendance2.dev.zoolwork.com` |
| Swagger | `https://attendance2.dev.zoolwork.com/swagger` |

Staging and COMM-IT production are **not** on this release.

## Documents

| Requested item | Where | Status |
|---|---|---|
| Services list | [Services-List.md](Services-List.md) | Ready |
| Enum list | [Enum-List.md](Enum-List.md) | Ready |
| Database collections | [Database-Collections.md](Database-Collections.md) | Ready |
| API list and documentation | Swagger UI (link above). Every endpoint has a one-line summary and a short description, grouped by module | Summaries arrive with the next DEV build (after `dev300-1.0.2`) |
| Functional documentation | To follow in this folder | In progress |
| Test cases | To follow in this folder | In progress |

## Using Swagger

1. Open the Swagger link and click **Authorize**.
2. Paste a JWT for your test tenant, without the `Bearer ` prefix.
3. Open a group (for example **Roster Boards**), expand an endpoint and use **Try it out**.
4. Fill `companyId` and, where the endpoint asks for it, `locationId`.

Groups follow the module list in [Services-List.md](Services-List.md#2-functional-modules).
