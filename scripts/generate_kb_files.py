import sys
from pathlib import Path

kb_dir = Path("/Users/swapnil/Documents/PS102/docs/knowledge_base")
kb_dir.mkdir(parents=True, exist_ok=True)

# Helper function to write markdown files
def write_doc(filename, title, content):
    filepath = kb_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{content}\n")
    print(f"Generated: {filepath.name} ({filepath.stat().st_size} bytes)")

print("Starting Knowledge Base generation...")
