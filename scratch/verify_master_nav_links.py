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

anchors = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)["\']', text))

broken = []
for title, link in links:
    aid = link[1:]
    found = aid in anchors or f'id="{aid}"' in text or f'name="{aid}"' in text
    if not found:
        broken.append((title, link))
        print(f"  BROKEN: {title[:45]} -> {link}")
    else:
        print(f"  OK: {title[:45]:<45} -> {link[:45]}")

if not broken:
    print("ALL MASTER NAVIGATION LINKS VERIFIED 100% WORKING!")
else:
    print(f"ERROR: {len(broken)} broken links found!")
