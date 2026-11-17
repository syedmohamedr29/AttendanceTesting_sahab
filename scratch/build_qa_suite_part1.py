# coding: utf-8
import os

out_path = r'C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\AM_Scheduler_Roster_Master_QA_Test_Suite.md'

with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# 📋 MASTER QA TEST SUITE & ARCHITECTURAL ANALYSIS: SCHEDULER (ROSTER)\n')
    f.write('**Module:** Attendance 2 — Scheduler (Roster & Planner)\n')
    f.write('**Microservices:** SP.AttendanceSvc (.NET 9), SP.EmployeeSvc | **Gateway:** gw8.dev.zoolwork.com\n')
    f.write('**Database:** MongoDB 10.1.0.4:27018 (Sahab.ERP.Attendance.*)\n')
    f.write('**Document ID:** QA-AM-SCHEDULER-20261117-V1 | **Author:** Senior QA Engineer & Automation Architect\n')
    f.write('**Environment:** DEV (ttendance2.dev.zoolwork.com) | **Date:** 17 November 2026\n\n')
    f.write('---\n\n')

print('Header written')
