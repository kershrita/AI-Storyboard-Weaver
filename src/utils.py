import json
import os
from pathlib import Path
import re
from .config import CONFIG

def sanitize_filename(name: str, max_length: int = 20) -> str:
    """Sanitize a string to be a valid folder name."""
    # Take first max_length characters
    name = name[:max_length]
    # Replace invalid characters with underscore
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Replace spaces with underscore
    name = name.replace(' ', '_')
    # Remove leading/trailing underscores
    name = name.strip('_')
    # If empty, use default name
    return name if name else "unnamed_story"

def init_knowledge_base(knowledge_base_path: str):
    """Initialize the knowledge base file in the specified path if it doesn't exist."""
    os.makedirs(os.path.dirname(knowledge_base_path), exist_ok=True)
    if not Path(knowledge_base_path).exists():
        with open(knowledge_base_path, "w") as f:
            json.dump({"plots": []}, f)