#!/usr/bin/env python3
"""
Script to add mountain data for missing countries
"""

import json

def add_missing_mountain_data():
    """Add mountain data for countries that are missing it"""
    
    print("🏔️ LEGGER TIL MANGLENDE FJELLDATA")
    print("=" * 50)
    
    # Manual mountain data for missing countries
    missing_mountain_data = {
        "Vatican City": {"mountain_name": "Vatican Hill", "elevation_meters": 75, "elevation_feet": 246},
        "San Marino": {"mountain_name": "Monte Titano", "elevation_meters": 739, "elevation_feet": 2425},
        "Cape Verde": {"mountain_name": "Mount Fogo", "elevation_meters": 2829, "elevation_feet": 9281},
        "Antigua and Barbuda": {"mountain_name": "Mount Obama", "elevation_meters": 402, "elevation_feet": 1319},
        "Barbados": {"mountain_name": "Mount Hillaby", "elevation_meters": 336, "elevation_feet": 1102},
        "Dominica": {"mountain_name": "Morne Diablotins", "elevation_meters": 1447, "elevation_feet": 4747},
        "Bahamas": {"mountain_name": "Mount Alvernia", "elevation_meters": 63, "elevation_feet": 207},
        "Sao Tome and Principe": {"mountain_name": "Pico de São Tomé", "elevation_meters": 2024, "elevation_feet": 6640},
        "Vanuatu": {"mountain_name": "Mount Tabwemasana", "elevation_meters": 1879, "elevation_feet": 6165},
        "Grenada": {"mountain_name": "Mount Saint Catherine", "elevation_meters": 840, "elevation_feet": 2756},
        "East Timor": {"mountain_name": "Mount Ramelau", "elevation_meters": 2963, "elevation_feet": 9721},
        "Maldives": {"mountain_name": "Mount Villingili", "elevation_meters": 5, "elevation_feet": 16},
        "Trinidad and Tobago": {"mountain_name": "El Cerro del Aripo", "elevation_meters": 940, "elevation_feet": 3084},
        "Liechtenstein": {"mountain_name": "Grauspitz", "elevation_meters": 2599, "elevation_feet": 8527},
        "Malta": {"mountain_name": "Ta' Dmejrek", "elevation_meters": 253, "elevation_feet": 830},
        "Kiribati": {"mountain_name": "Banaba Island", "elevation_meters": 81, "elevation_feet": 266},
        "Tonga": {"mountain_name": "Kao Island", "elevation_meters": 1030, "elevation_feet": 3379},
        "Palau": {"mountain_name": "Mount Ngerchelchuus", "elevation_meters": 242, "elevation_feet": 794},
        "Nauru": {"mountain_name": "Command Ridge", "elevation_meters": 71, "elevation_feet": 233}
    }
    
    try:
        # Load existing data
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        
        updated_count = 0
        
        for country in countries:
            country_name = country.get('name', '')
            
            if country_name in missing_mountain_data:
                mountain_info = missing_mountain_data[country_name]
                country['highest_mountain'] = mountain_info['mountain_name']
                country['highest_elevation_meters'] = mountain_info['elevation_meters']
                country['highest_elevation_feet'] = mountain_info['elevation_feet']
                updated_count += 1
                print(f"✅ {country_name}: {mountain_info['mountain_name']} ({mountain_info['elevation_meters']}m)")
        
        # Save updated data
        with open('countries_data.json', 'w', encoding='utf-8') as f:
            json.dump(countries, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Oppdatert {updated_count} land med manglende fjelldata")
        print(f"💾 Lagret til countries_data.json")
        
        return updated_count
        
    except Exception as e:
        print(f"❌ Feil ved oppdatering: {e}")
        return 0

if __name__ == "__main__":
    add_missing_mountain_data()
