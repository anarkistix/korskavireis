#!/usr/bin/env python3
"""
Script to update countries_data_no.json with mountain data
"""

import json

def update_norwegian_mountains():
    """Update countries_data_no.json with mountain information from countries_data.json"""
    
    print("🏔️ OPPDATERER NORSKE LANDNAVN MED FJELLDATA")
    print("=" * 50)
    
    try:
        # Load English data with mountains
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            english_data = json.load(f)
        
        # Load Norwegian data
        with open('countries_data_no.json', 'r', encoding='utf-8') as f:
            norwegian_data = json.load(f)
        
        updated_count = 0
        
        # Create a mapping from English names to mountain data
        mountain_mapping = {}
        for country in english_data:
            if 'highest_mountain' in country:
                mountain_mapping[country['name']] = {
                    'highest_mountain': country['highest_mountain'],
                    'highest_elevation_meters': country['highest_elevation_meters'],
                    'highest_elevation_feet': country['highest_elevation_feet']
                }
        
        # Update Norwegian data with mountain information
        for country in norwegian_data:
            if country['name'] in mountain_mapping:
                mountain_info = mountain_mapping[country['name']]
                country['highest_mountain'] = mountain_info['highest_mountain']
                country['highest_elevation_meters'] = mountain_info['highest_elevation_meters']
                country['highest_elevation_feet'] = mountain_info['highest_elevation_feet']
                updated_count += 1
                print(f"✅ {country['name']}: {mountain_info['highest_mountain']} ({mountain_info['highest_elevation_meters']}m)")
        
        # Save updated Norwegian data
        with open('countries_data_no.json', 'w', encoding='utf-8') as f:
            json.dump(norwegian_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Oppdatert {updated_count} norske land med fjelldata")
        print(f"💾 Lagret til countries_data_no.json")
        
        return updated_count
        
    except Exception as e:
        print(f"❌ Feil ved oppdatering: {e}")
        return 0

if __name__ == "__main__":
    update_norwegian_mountains()
