#!/usr/bin/env python3
"""
Check which countries are missing imageFile fields
"""

import json

def check_missing_imagefiles():
    """Check which countries are missing imageFile fields"""
    print("🔍 Checking for missing imageFile fields...")
    
    # Load country data
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    missing_count = 0
    for country in countries_data:
        if 'imageFile' not in country:
            print(f"❌ Missing imageFile for: {country['name']}")
            missing_count += 1
    
    print(f"\n📊 Countries missing imageFile: {missing_count}")

if __name__ == '__main__':
    check_missing_imagefiles()
