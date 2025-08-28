#!/usr/bin/env python3
import json
import os

def check_missing_population():
    """Sjekker hvilke land som mangler befolkningsdata"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"🔍 Sjekker befolkningsdata-status for {len(countries)} land...")
    print("=" * 60)
    
    missing_population = []
    has_population = []
    
    for country in countries:
        population = country.get('population')
        population_year = country.get('population_year')
        
        if not population:
            missing_population.append(country)
        else:
            has_population.append(country)
    
    print(f"✅ Land med befolkningsdata: {len(has_population)}")
    print(f"❌ Land uten befolkningsdata: {len(missing_population)}")
    print(f"📊 Total: {len(countries)}")
    print()
    
    if missing_population:
        print("🚩 LAND UTEN BEFOLKNINGSDATA:")
        print("-" * 50)
        for i, country in enumerate(missing_population, 1):
            population = country.get('population', 'INGEN')
            population_year = country.get('population_year', 'INGEN')
            print(f"{i:2d}. {country['name']:<25} | Befolkning: {population} | År: {population_year}")
    else:
        print("🎉 Alle land har befolkningsdata!")
    
    print()
    print("📋 SAMMENDRAG:")
    print(f"   • Land med befolkningsdata: {len(has_population)}")
    print(f"   • Land uten befolkningsdata: {len(missing_population)}")
    print(f"   • Prosent med befolkningsdata: {len(has_population)/len(countries)*100:.1f}%")
    
    # Vis eksempel på land med befolkningsdata
    if has_population:
        print()
        print("📊 EKSEMPEL - LAND MED BEFOLKNINGSDATA:")
        print("-" * 50)
        for i, country in enumerate(has_population[:5], 1):
            population = country.get('population', 'N/A')
            population_year = country.get('population_year', 'N/A')
            formatted_population = f"{population:,}" if population else 'N/A'
            print(f"{i}. {country['name']:<20} | {formatted_population} ({population_year})")

if __name__ == "__main__":
    check_missing_population()
