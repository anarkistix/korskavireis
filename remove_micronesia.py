#!/usr/bin/env python3
"""
Remove Micronesia since it doesn't have an image
"""

import json

def remove_micronesia():
    """Remove Micronesia from the game"""
    print("🗑️ Removing Micronesia (no image available)...")
    
    # Load country data
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    # Filter out Micronesia
    filtered_countries = []
    removed_count = 0
    
    for country in countries_data:
        if country['name'] == 'Micronesia':
            print(f"🗑️ Removing {country['name']} (no image available)")
            removed_count += 1
        else:
            filtered_countries.append(country)
    
    # Save updated data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_countries, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Removed {removed_count} countries")
    print(f"📊 Remaining countries: {len(filtered_countries)}")
    print(f"💾 Saved to countries_data.json")

if __name__ == '__main__':
    remove_micronesia()
