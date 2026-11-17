# -*- coding: utf-8 -*-
import re

def verify_markdown_toc(filepath, toc_title):
    print(f"=== Verifying TOC in {filepath} ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find TOC block
    toc_pattern = rf"{re.escape(toc_title)}[\s\S]+?\n---"
    match = re.search(toc_pattern, text)
    if not match:
        print(f"TOC block '{toc_title}' not found!")
        return
    
    toc_content = match.group(0)
    links = re.findall(r'\[([^\]]+)\]\(#([^\)]+)\)', toc_content)
    print(f"Found {len(links)} links in TOC.")

    all_anchors = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)["\']', text))
    
    # Also get header slugs
    headers = re.findall(r'^(#{1,4})\s+(.+)$', text, re.MULTILINE)
    for level, h in headers:
        clean_h = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', h)
        clean_h = re.sub(r'[`*_]', '', clean_h)
        clean_h = clean_h.lower()
        clean_h = re.sub(r'[^\w\s-]', '', clean_h)
        slug = re.sub(r'\s+', '-', clean_h.strip())
        all_anchors.add(slug)
        all_anchors.add('-' + slug)

    broken = []
    for link_text, anchor in links:
        if anchor not in all_anchors and anchor.lstrip('-') not in all_anchors:
            broken.append((link_text, anchor))
        else:
            print(f"  OK: {link_text[:40]} -> #{anchor}")

    if broken:
        print(f"ERROR: {len(broken)} broken links:")
        for t, a in broken:
            print(f"  BROKEN: {t} -> #{a}")
    else:
        print(f"ALL {len(links)} LINKS VERIFIED WORKING 100%!")

verify_markdown_toc('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', '## 📑 Table of Contents')
verify_markdown_toc('Defects/Attendance2_Master_Defect_Log.md', '## 📑 Table of Contents')
