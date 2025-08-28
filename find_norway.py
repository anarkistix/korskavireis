#!/usr/bin/env python3
"""
Find Norway and check its imageFile field
"""

import json

def find_norway():
    """Find Norway and check its imageFile field"""
    print("🔍 Finding Norway...")
    
    # Load country data
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    for i, country in enumerate(countries_data):
        if country['name'] == 'Norway':
            print(f"✓ Found Norway at index {i}")
            print(f"Country data: {json.dumps(country, indent=2)}")
            
            if 'imageFile' in country:
                print(f"✓ Has imageFile: {country['imageFile']}")
            else:
                print("❌ Missing imageFile field")
            break
    else:
        print("❌ Norway not found")

if __name__ == '__main__':
    find_norway()
