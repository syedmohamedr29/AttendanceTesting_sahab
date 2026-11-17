# coding: utf-8
import os
import sys

out_path = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\AM_Scheduler_Roster_Master_QA_Test_Suite.md"

import build_master_qa_suite
import sec_01_to_04
import sec_05_to_10
import sec_11_to_15
import sec_16_to_22

print("Imported all sections successfully.")

with open(out_path, "w", encoding="utf-8") as f:
    # Write header & TOC
    build_master_qa_suite.write_header()

with open(out_path, "a", encoding="utf-8") as f:
    f.write(sec_01_to_04.get_content())
    f.write(sec_05_to_10.get_content())
    f.write(sec_11_to_15.get_content())
    f.write(sec_16_to_22.get_content())

with open(out_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Master QA Suite assembled successfully!")
print(f"File path: {out_path}")
print(f"Total lines: {len(lines)}")
print(f"Total characters: {sum(len(l) for l in lines)}")
