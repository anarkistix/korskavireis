#!/usr/bin/env python3
import json
import os

def update_population_data():
    """Oppdaterer befolkningsdata for Vatican City og Taiwan"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"🔧 Oppdaterer befolkningsdata for Vatican City og Taiwan...")
    
    # Befolkningsdata som skal oppdateres
    population_updates = {
        'Vatican City': {
            'population': 882,
            'population_year': 2024
        },
        'Taiwan': {
            'population': 23400000,
            'population_year': 2024
        }
    }
    
    updated_count = 0
    
    for country in countries:
        if country['name'] in population_updates:
            old_population = country.get('population')
            old_year = country.get('population_year')
            
            # Oppdater data
            country['population'] = population_updates[country['name']]['population']
            country['population_year'] = population_updates[country['name']]['population_year']
            
            print(f"✅ {country['name']}:")
            print(f"   Befolkning: {old_population} → {country['population']:,}")
            print(f"   År: {old_year} → {country['population_year']}")
            updated_count += 1
    
    # Lagre oppdatert data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Oppdatering fullført!")
    print(f"✅ {updated_count} land oppdatert")
    
    # Vis statistikk
    countries_with_population = sum(1 for c in countries if c.get('population'))
    print(f"📊 Land med befolkningsdata: {countries_with_population}/{len(countries)} ({countries_with_population/len(countries)*100:.1f}%)")

if __name__ == "__main__":
    update_population_data()
