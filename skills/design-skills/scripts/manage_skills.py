import os
import sys
import shutil
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REGISTRY_DIR = BASE_DIR / "registry"
CATALOG_FILE = BASE_DIR / "references" / "catalog.json"
PARENT_SKILLS_DIR = BASE_DIR.parent

def list_skills():
    if not CATALOG_FILE.exists():
        print("Catalog not found.")
        return
    skills = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
    print(f"Total Design Skills Available: {len(skills)}\n")
    print(f"{'Name':<18} | {'Visual Style':<25} | {'Description'}")
    print("-" * 80)
    for s in skills:
        desc = (s['description'][:45] + "...") if len(s['description']) > 48 else s['description']
        print(f"{s['name']:<18} | {s['visual_style'][:25]:<25} | {desc}")

def info_skill(name):
    target = REGISTRY_DIR / name
    if not target.exists():
        print(f"Error: Skill '{name}' not found in registry.")
        return
    design_file = target / "DESIGN.md"
    skill_file = target / "SKILL.md"
    
    print(f"=== DESIGN SYSTEM: {name} ===")
    if design_file.exists():
        print("\n--- DESIGN TOKENS (DESIGN.md) ---")
        print(design_file.read_text(encoding="utf-8"))
    elif skill_file.exists():
        print("\n--- SKILL GUIDANCE (SKILL.md) ---")
        print(skill_file.read_text(encoding="utf-8")[:1000] + "...")

def promote_skill(name):
    source = REGISTRY_DIR / name
    if not source.exists():
        print(f"Error: Skill '{name}' not found in registry.")
        return
    dest = PARENT_SKILLS_DIR / name
    if dest.exists():
        print(f"Skill '{name}' is already promoted at {dest}")
        return
    shutil.copytree(source, dest)
    print(f"Successfully promoted '{name}' to top-level skill at: {dest}")
    print("Antigravity will now recognize this as a dedicated standalone skill.")

def demote_skill(name):
    dest = PARENT_SKILLS_DIR / name
    if not dest.exists():
        print(f"Skill '{name}' is not currently promoted.")
        return
    shutil.rmtree(dest)
    print(f"Successfully demoted/removed '{name}' from top-level skills.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_skills.py [list | info <name> | promote <name> | demote <name>]")
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    if cmd == "list":
        list_skills()
    elif cmd == "info" and len(sys.argv) >= 3:
        info_skill(sys.argv[2])
    elif cmd == "promote" and len(sys.argv) >= 3:
        promote_skill(sys.argv[2])
    elif cmd == "demote" and len(sys.argv) >= 3:
        demote_skill(sys.argv[2])
    else:
        print("Invalid arguments. Usage: python manage_skills.py [list | info <name> | promote <name> | demote <name>]")
