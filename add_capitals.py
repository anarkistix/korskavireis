#!/usr/bin/env python3
import json
import os

def add_capitals_data():
    """Legger til hovedstadsdata for alle land"""
    
    # Les capitals.geojson
    with open('capitals.geojson', 'r', encoding='utf-8') as f:
        capitals_data = json.load(f)
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"🌍 Legger til hovedstadsdata for {len(countries)} land...")
    print("=" * 60)
    
    # Lag en mapping fra landnavn til hovedstad
    capitals_mapping = {}
    for feature in capitals_data['features']:
        properties = feature['properties']
        country_name = properties.get('country')
        
        # Sjekk om 'city' feltet eksisterer
        if 'city' not in properties:
            print(f"⚠️  Hopper over {country_name}: Ingen 'city' felt")
            continue
            
        capital_name = properties['city']
        iso3 = properties.get('iso3')
        coordinates = feature['geometry']['coordinates']
        
        if country_name:
            capitals_mapping[country_name] = {
                'capital': capital_name,
                'iso3': iso3,
                'coordinates': coordinates
            }
    
    print(f"📋 Lastet {len(capitals_mapping)} hovedstader fra capitals.geojson")
    
    updated_count = 0
    missing_capitals = []
    
    for country in countries:
        country_name = country['name']
        
        if country_name in capitals_mapping:
            capital_data = capitals_mapping[country_name]
            country['capital'] = capital_data['capital']
            country['capital_coordinates'] = {
                'lon': capital_data['coordinates'][0],
                'lat': capital_data['coordinates'][1]
            }
            updated_count += 1
            print(f"✅ {country_name}: {capital_data['capital']}")
        else:
            missing_capitals.append(country_name)
            print(f"❌ {country_name}: Ingen hovedstad funnet")
    
    # Lagre oppdatert data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("🎉 Oppdatering fullført!")
    print(f"✅ {updated_count} land oppdatert med hovedstadsdata")
    print(f"❌ {len(missing_capitals)} land uten hovedstadsdata")
    
    if missing_capitals:
        print(f"\n📋 Land uten hovedstadsdata:")
        for country in missing_capitals[:10]:  # Vis kun første 10
            print(f"   - {country}")
        if len(missing_capitals) > 10:
            print(f"   ... og {len(missing_capitals) - 10} flere")
    
    # Vis eksempel på oppdatert data
    print("\n📋 EKSEMPEL - OPPDATERT LAND:")
    print("-" * 50)
    for i, country in enumerate(countries[:3], 1):
        print(f"{i}. {country['name']}")
        if 'capital' in country:
            print(f"   Hovedstad: {country['capital']}")
            print(f"   Koordinater: {country['capital_coordinates']['lat']:.2f}, {country['capital_coordinates']['lon']:.2f}")
        else:
            print(f"   Hovedstad: Ikke tilgjengelig")
        print()

if __name__ == "__main__":
    add_capitals_data()
