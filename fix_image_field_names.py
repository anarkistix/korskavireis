#!/usr/bin/env python3
"""
Fix incorrect image field names in country data
"""

import json

def fix_image_field_names():
    """Fix incorrect image field names"""
    print("🔧 Fixing incorrect image field names...")
    
    # Load country data
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    # ISO mapping for country names to correct image files
    iso_mapping = {
        'Nigeria': 'ng.png',
        'Micronesia': 'fm.png'
    }
    
    fixed_count = 0
    for country in countries_data:
        country_name = country['name']
        
        # Check if this country needs fixing
        if country_name in iso_mapping:
            correct_image = iso_mapping[country_name]
            
            # Fix image_file to imageFile
            if 'image_file' in country:
                del country['image_file']
                print(f"✓ Removed incorrect 'image_file' for {country_name}")
            
            # Set correct imageFile
            country['imageFile'] = correct_image
            print(f"✓ Fixed {country_name}: {correct_image}")
            fixed_count += 1
    
    # Save updated data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Fixed {fixed_count} image field names")
    print(f"💾 Saved to countries_data.json")

if __name__ == '__main__':
    fix_image_field_names()
