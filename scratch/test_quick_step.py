# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(line_buffering=True)
import json, time, requests, pymongo

print("Step 1: Loading token...", flush=True)
with open("scratch/token.json") as f:
    token_data = json.load(f)
TOKEN = token_data.get("access_token")

print("Step 2: Connecting to Mongo...", flush=True)
mongo = pymongo.MongoClient("mongodb://10.1.0.4:27018/", serverSelectionTimeoutMS=3000)
db_emp = mongo["EmployeeSvcNET8test"]
col_emp = db_emp["Employee"]
c = col_emp.count_documents({})
print(f"Connected to Mongo. Employee count: {c}", flush=True)

print("Step 3: Testing single API call...", flush=True)
BASE_URL = "https://gw8.dev.zoolwork.com"
COMPANY_ID = "3a24e5e5-302e-91bd-feaa-b07979766dfe"
LOC_DAMMAM = "3a24e666-df63-3dc7-0ea7-02ec8be341e7"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}

r = requests.get(f"{BASE_URL}/api/companies/{COMPANY_ID}/workassignments?locationId={LOC_DAMMAM}", headers=HEADERS, timeout=5)
print(f"API call done! Status: {r.status_code}", flush=True)
