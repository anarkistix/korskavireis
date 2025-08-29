#!/usr/bin/env python3
"""
Check specific countries that seem incorrectly marked as islands
"""
import json

def check_specific_countries():
    # Load countries data
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    # Countries to check
    check_countries = [
        "Iran", "Angola", "Haiti", "Dominican Republic", "Philippines", "Madagascar"
    ]
    
    print("🔍 SJEKKER SPESIFIKKE LAND")
    print("=" * 50)
    
    for country_name in check_countries:
        country = next((c for c in countries if c['name'] == country_name), None)
        if country:
            print(f"\n{country_name}:")
            print(f"  - is_island: {country.get('is_island', 'Ikke satt')}")
            print(f"  - borders: {country.get('borders', 'Ingen data')}")
            print(f"  - borders_no: {country.get('borders_no', 'Ingen data')}")
            print(f"  - continent: {country.get('continent', 'Ikke satt')}")
            print(f"  - region: {country.get('region', 'Ikke satt')}")
        else:
            print(f"\n{country_name}: IKKE FUNNET")
    
    # Check if these countries should have borders
    print(f"\n🌍 GEOGRAFISK ANALYSE:")
    print("Iran: Burde ha grenser til Irak, Afghanistan, Pakistan, Turkmenistan, etc.")
    print("Angola: Burde ha grenser til Namibia, Zambia, DR Congo, etc.")
    print("Haiti: Burde ha grense til Dominican Republic (samme øy)")
    print("Dominican Republic: Burde ha grense til Haiti (samme øy)")
    print("Philippines: Øy-nasjon, men har maritime grenser")
    print("Madagascar: Øy, men har maritime grenser")

if __name__ == "__main__":
    check_specific_countries()
