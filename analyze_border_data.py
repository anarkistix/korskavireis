#!/usr/bin/env python3
"""
Analyze border data to identify incorrectly marked islands
"""
import json

def analyze_border_data():
    # Load countries data
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print("🔍 ANALYSERER NABOLAND-DATA")
    print("=" * 50)
    
    # Check specific countries
    test_countries = [
        "Norway", "Switzerland", "Germany", "France", "Italy", 
        "Spain", "Poland", "Austria", "Belgium", "Netherlands"
    ]
    
    print("\n📋 TEST AV SPESIFIKKE LAND:")
    for country_name in test_countries:
        country = next((c for c in countries if c['name'] == country_name), None)
        if country:
            print(f"\n{country_name}:")
            print(f"  - is_island: {country.get('is_island', 'Ikke satt')}")
            print(f"  - borders: {country.get('borders', 'Ingen data')}")
            print(f"  - borders_no: {country.get('borders_no', 'Ingen data')}")
        else:
            print(f"\n{country_name}: IKKE FUNNET")
    
    # Count islands vs non-islands
    islands = [c for c in countries if c.get('is_island')]
    non_islands_with_borders = [c for c in countries if not c.get('is_island') and c.get('borders')]
    non_islands_without_borders = [c for c in countries if not c.get('is_island') and not c.get('borders')]
    
    print(f"\n📊 STATISTIKK:")
    print(f"  - Totalt antall land: {len(countries)}")
    print(f"  - Markert som øy: {len(islands)}")
    print(f"  - Ikke øy med naboland: {len(non_islands_with_borders)}")
    print(f"  - Ikke øy uten naboland: {len(non_islands_without_borders)}")
    
    # List all islands
    print(f"\n🏝️ ALLE LAND MARKERT SOM ØY ({len(islands)}):")
    for country in islands:
        print(f"  - {country['name']}")
    
    # Check for countries that should be islands but aren't marked
    print(f"\n🔍 LAND SOM KAN VÆRE ØYER (ingen naboland):")
    potential_islands = [c for c in countries if not c.get('is_island') and not c.get('borders')]
    for country in potential_islands:
        print(f"  - {country['name']}")
    
    # Check for countries with borders but marked as islands
    print(f"\n⚠️ LAND MED NABOLAND MEN MARKERT SOM ØY:")
    incorrect_islands = [c for c in countries if c.get('is_island') and c.get('borders')]
    for country in incorrect_islands:
        print(f"  - {country['name']}: {country.get('borders')}")

if __name__ == "__main__":
    analyze_border_data()
