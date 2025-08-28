#!/usr/bin/env python3
"""
Add missing imageFile fields for countries
"""

import json

def add_missing_imagefiles():
    """Add missing imageFile fields"""
    print("🔧 Adding missing imageFile fields...")
    
    # Load country data
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    # ISO mapping for countries that might be missing imageFile
    iso_mapping = {
        'Norway': 'no.png'
    }
    
    added_count = 0
    for country in countries_data:
        country_name = country['name']
        
        # Check if country is missing imageFile
        if 'imageFile' not in country and country_name in iso_mapping:
            correct_image = iso_mapping[country_name]
            country['imageFile'] = correct_image
            print(f"✓ Added imageFile for {country_name}: {correct_image}")
            added_count += 1
    
    # Save updated data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Added {added_count} missing imageFile fields")
    print(f"💾 Saved to countries_data.json")

if __name__ == '__main__':
    add_missing_imagefiles()
