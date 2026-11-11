$token = (Get-Content "scratch/current_token.json" | ConvertFrom-Json).access_token
$cid = "3a249872-2d69-f931-41f6-d8db086b09b8"

Write-Host "=== CHECKING ATTENDANCE 9 DETAILS & LOCATIONS IN COMPANY SVC ==="
try {
  $r = Invoke-RestMethod -Uri "https://company8.dev.zoolwork.com/api/company/companies/getCompanyDetails?companyId=$cid" -Headers @{Authorization="Bearer $token"}
  $r | ConvertTo-Json -Depth 5
} catch {
  Write-Host "Error getCompanyDetails:" $_.Exception.Message
}

try {
  $locs = Invoke-RestMethod -Uri "https://company8.dev.zoolwork.com/api/company/workLocations/getAllWorkLocations?companyId=$cid" -Headers @{Authorization="Bearer $token"}
  Write-Host "Locations count:" $locs.Count
  $locs | ConvertTo-Json -Depth 5
} catch {
  Write-Host "Locations error:" $_.Exception.Message
}

