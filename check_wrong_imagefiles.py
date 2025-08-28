#!/usr/bin/env python3
"""
Check for wrong imageFile values
"""

import json

def check_wrong_imagefiles():
    """Check for wrong imageFile values"""
    print("🔍 Checking for wrong imageFile values...")
    
    # Load country data
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    # Check for wrong patterns
    wrong_patterns = ['norway.png', 'nigeria.png', 'switzerland.png']
    
    for country in countries_data:
        if 'imageFile' in country:
            image_file = country['imageFile']
            for pattern in wrong_patterns:
                if pattern in image_file:
                    print(f"❌ Wrong imageFile for {country['name']}: {image_file}")
    
    print("✅ Check complete")

if __name__ == '__main__':
    check_wrong_imagefiles()
