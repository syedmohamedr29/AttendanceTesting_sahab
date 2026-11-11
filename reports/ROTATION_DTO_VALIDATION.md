# Sahab ERP Attendance – Rotation Work Template DTO & Schema Validation Matrix

**Execution Date:** `2026-11-10`

## 1. Request DTO Schema Analysis (`RotationWorkTemplateDto`)

| Field Name | Type | Required | Validator Rule | Confirmed Behavior |
| :--- | :--- | :---: | :--- | :--- |
| `templateName` | Localized Dictionary | Yes | Cannot be null | ❌ Accepts empty strings `{'en':'','ar':''}` (`DEFECT-20261110-20`) |
| `shortCode` | String | Yes | Max 7 alphanumeric chars, unique | ✅ Strictly enforced with `Cit.Attendance:1106` |
| `templateType` | Enum | Yes | Must be `Rotation` (5) | ⚠️ Accepts `Fixed` and overrides to `Rotation` (`DEFECT-20261110-21`) |
| `totalWorkDurationInMinutes` | Double/Int | Yes | Sum of daily working durations | ✅ Enforced on working days |
| `totalWorkingDays` | Integer | Yes | Count of `isWorkingDay == true` | ✅ Validated between 1 and 7 |
| `totalDaysOff` | Integer | Yes | Count of `isWorkingDay == false` | ✅ Enforced between 0 and 6 |
| `rotationTimeSlots` | Array of 7 Slots | Yes | Must have exactly 7 weekday slots | ✅ Enforced with `Cit.Attendance:2032` and `Cit.Attendance:2033` |
| `rotationTimeSlots[].dayEnum` | Enum (`Sun`..`Sat`) | Yes | Each day appears exactly once | ✅ Enforces unique dayEnum per week |
| `rotationTimeSlots[].isWorkingDay` | Boolean | Yes | True for work days, false for off | ✅ Correctly enforced |
| `rotationTimeSlots[].workDurationInMinutes` | Double | Yes | >0 on work days, 0 on days off | ✅ Enforced (>0 and <=1439 min) |
| `rotationTimeSlots[].startTime` / `endTime` | Time String | Yes | Valid format HH:mm:ss | ✅ Overnight supported |
| `rotationTimeSlots[].recurrenceOfMonth` | Enum Array | Yes | `First` through `Fifth` | ✅ Enforced via ASP.NET Core enum binding |