# fix_qty.py
import json
from pathlib import Path

F = Path(__file__).with_name("assemblies.json")
data = json.loads(F.read_text())

for asm in data:
    if asm["name"].startswith("BP-"):
        asm["qty"] = 2.0
    else:
        asm["qty"] = 1.0

F.write_text(json.dumps(data, indent=2))
print("✅ assemblies.json fixed")
