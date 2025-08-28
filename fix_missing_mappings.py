#!/usr/bin/env python3
"""
Fix missing ISO mappings and update country data
"""

import json

# Additional ISO mappings for missing countries
additional_mappings = {
    'Syria': 'sy',
    'Antigua and Barbuda': 'ag',
    'Russia': 'ru',
    'Iran': 'ir',
    'East Timor': 'tl',
    'Tanzania': 'tz',
    'Brunei': 'bn',
    'Taiwan': 'tw',
    'Laos': 'la',
    'South Korea': 'kr',
    'Micronesia': 'fm',
    'Eswatini': 'sz',
    'United Kingdom': 'gb',
    'North Korea': 'kp',
    'Moldova': 'md',
    'United States': 'us',
    'Ivory Coast': 'ci',
    'Bosnia and Herzegovina': 'ba'
}

# Load current country data
with open('countries_data.json', 'r', encoding='utf-8') as f:
    countries_data = json.load(f)

print(f"📊 Found {len(countries_data)} countries in data")

# Update countries with ISO codes
updated_count = 0
for country in countries_data:
    country_name = country['name']
    
    # Check if we have a mapping for this country
    if country_name in additional_mappings:
        iso_code = additional_mappings[country_name]
        country['iso_code'] = iso_code
        print(f"✓ Added ISO code for {country_name}: {iso_code}")
        updated_count += 1

# Save updated data
with open('countries_data.json', 'w', encoding='utf-8') as f:
    json.dump(countries_data, f, indent=2, ensure_ascii=False)

print(f"\n📊 Updated {updated_count} countries with ISO codes")
print(f"💾 Saved to countries_data.json")
