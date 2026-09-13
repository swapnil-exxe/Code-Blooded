import os
from pathlib import Path

kb_dir = Path("/Users/swapnil/Documents/PS102/docs/knowledge_base")
kb_dir.mkdir(parents=True, exist_ok=True)

print(f"Knowledge base directory created at {kb_dir}")
