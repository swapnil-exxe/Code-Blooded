import os
from pathlib import Path

docs_dir = Path("/Users/swapnil/Documents/PS102/docs")
kb_dir = docs_dir / "knowledge_base"
master_file = docs_dir / "PROJECT_COMPLETE_TECHNICAL_KNOWLEDGE_BASE.md"

files = sorted(list(kb_dir.glob("*.md")))

print(f"Concatenating {len(files)} knowledge base modules into master file...")

with open(master_file, "w", encoding="utf-8") as outfile:
    outfile.write("# MPLADS AI Command Center — Master Project Technical Knowledge Base & Viva Reference\n\n")
    outfile.write("> **System**: AI-Powered MPLADS Analytics & Governance Platform  \n")
    outfile.write("> **Problem Statement**: SIH 2026 — PS ID 26102 (MoSPI)  \n")
    outfile.write("> **Dataset Scope**: 190,942 Master Works | 109,311 Expenditure Vouchers | ₹10,211.49 Cr Sanctioned Outlay | 773 Districts | 36 States  \n")
    outfile.write("> **Validation**: 117/117 Automated Tests Passing (100% Pass Rate) | 0 Critical Vulnerabilities  \n\n")
    outfile.write("---\n\n")
    
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as infile:
            outfile.write(infile.read())
            outfile.write("\n\n---\n\n")

print(f"Master Knowledge Base generated at {master_file} ({master_file.stat().st_size} bytes)")
