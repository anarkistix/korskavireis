#!/usr/bin/env python3
"""
Automatisk versjoneringssystem for KorSkaViReis
Oppdaterer version.json med ny build-informasjon
"""

import json
import subprocess
import datetime
import os
from pathlib import Path

def get_git_info():
    """Henter Git-informasjon"""
    try:
        # Hent commit hash
        commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], 
                                       text=True).strip()
        
        # Hent siste tag
        try:
            tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'], 
                                        text=True).strip()
        except subprocess.CalledProcessError:
            tag = "ingen-tag"
            
        return commit, tag
    except subprocess.CalledProcessError:
        return "ukjent", "ingen-tag"

def update_version():
    """Oppdaterer version.json med ny informasjon"""
    
    # Hent Git-informasjon
    commit, tag = get_git_info()
    
    # Generer build-timestamp
    now = datetime.datetime.now()
    build = now.strftime("%Y-%m-%d-%H-%M")
    
    # Les eksisterende version.json hvis den finnes
    version_file = Path("version.json")
    if version_file.exists():
        with open(version_file, 'r', encoding='utf-8') as f:
            version_data = json.load(f)
    else:
        version_data = {
            "version": "1.0.0",
            "build": "",
            "commit": "",
            "tag": "",
            "description": ""
        }
    
    # Oppdater med ny informasjon
    version_data.update({
        "build": build,
        "commit": commit,
        "tag": tag,
        "last_updated": now.isoformat()
    })
    
    # Skriv til fil
    with open(version_file, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Versjon oppdatert:")
    print(f"   Build: {build}")
    print(f"   Commit: {commit}")
    print(f"   Tag: {tag}")
    
    return version_data

if __name__ == "__main__":
    update_version()
