#!/usr/bin/env python3
"""
Fix incorrect image filenames in country data
"""

import json

def fix_image_filenames():
    """Fix incorrect image filenames"""
    print("🔧 Fixing incorrect image filenames...")
    
    # Load country data
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    # Fix incorrect filenames
    fixes = {
        'marshall_islands.png': 'mh.png',
        'tuvalu.png': 'tv.png'
    }
    
    fixed_count = 0
    for country in countries_data:
        if 'imageFile' in country:
            old_filename = country['imageFile']
            if old_filename in fixes:
                new_filename = fixes[old_filename]
                country['imageFile'] = new_filename
                print(f"✓ Fixed {old_filename} → {new_filename}")
                fixed_count += 1
    
    # Save updated data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Fixed {fixed_count} image filenames")
    print(f"💾 Saved to countries_data.json")

if __name__ == '__main__':
    fix_image_filenames()
