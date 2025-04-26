import json
import os
from pathlib import Path

def init_knowledge_base(knowledge_base_path: str):
    """Initialize the knowledge base file if it doesn't exist."""
    if not Path(knowledge_base_path).exists():
        with open(knowledge_base_path, "w") as f:
            json.dump({"plots": []}, f)