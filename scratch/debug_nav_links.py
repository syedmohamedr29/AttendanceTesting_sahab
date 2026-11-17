# -*- coding: utf-8 -*-
import re

REPORT_FILE = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(REPORT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

nav_start = text.find("## 📅 Master Navigation & Table of Contents")
nav_end = text.find("## 📑 Table of Contents")
nav_text = text[nav_start:nav_end]

links = re.findall(r"\[([^\]]+)\]\((#[^\)]+)\)", nav_text)
print(f"Checking {len(links)} links in Master Navigation & Table of Contents...")

for title, link in links:
    aid = link[1:]
    # Check if there is an <a id="aid"> or heading with slug aid
    has_a = f'id="{aid}"' in text or f"id='{aid}'" in text
    print(f"{aid[:45]:<45} -> has_tag: {has_a}")
