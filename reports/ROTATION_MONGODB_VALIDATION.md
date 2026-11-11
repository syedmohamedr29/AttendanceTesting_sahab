# Sahab ERP Attendance – Rotation Work Template MongoDB Validation Report

**Target Collection:** `Sahab.ERP.Attendance.WorkTemplates` | **Discriminator:** `_t: ['WorkTemplate', 'RotationWorkTemplate']`

## 1. Verified Document Structure in MongoDB

```json
{
  "_t": ["WorkTemplate", "RotationWorkTemplate"],
  "TemplateType": 5,
  "Status": 1,
  "Version": "1.0",
  "IsDefault": false,
  "IsEditable": true,
  "IsDeleted": false,
  "TimeZoneId": "Asia/Riyadh",
  "RotationTimeSlots": [
    {
      "WorkDurationInMinutes": 480.0,
      "DayEnum": 1,
      "IsWorkingDay": true,
      "RecurrenceOfMonth": [1, 2, 3, 4, 5],
      "StartTime": "09:00:00.0000000",
      "EndTime": "17:00:00.0000000"
    }
  ]
}
```

## 2. In-Place Mutation vs Versioning

Executing `PATCH .../worktemplates/rotation/{id}` performs an in-place mutation on the document in MongoDB:

- Document `_id` is preserved.

- `Version` remains `"1.0"`.

- `CreatedAt` and `CreatedBy` are strictly preserved.

- `ModifiedAt` and `ModifiedBy` are stamped with the current user.
