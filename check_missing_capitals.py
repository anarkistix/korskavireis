#!/usr/bin/env python3
import json

def check_missing_capitals():
    """Sjekker hvilke land som mangler hovedstadsdata"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print("🔍 Sjekker hovedstadsdata for alle land...")
    print("=" * 60)
    
    countries_with_capital = []
    countries_without_capital = []
    
    for country in countries:
        if 'capital' in country and country['capital']:
            countries_with_capital.append(country['name'])
        else:
            countries_without_capital.append(country['name'])
    
    print(f"✅ Land med hovedstad: {len(countries_with_capital)}")
    print(f"❌ Land uten hovedstad: {len(countries_without_capital)}")
    print(f"📊 Dekning: {len(countries_with_capital)/len(countries)*100:.1f}%")
    
    if countries_without_capital:
        print(f"\n📋 LAND UTEN HOVEDSTAD:")
        print("-" * 40)
        for i, country in enumerate(countries_without_capital, 1):
            print(f"{i:2d}. {country}")
    
    print(f"\n📋 EKSEMPLER - LAND MED HOVEDSTAD:")
    print("-" * 40)
    for i, country_name in enumerate(countries_with_capital[:5], 1):
        country_data = next(c for c in countries if c['name'] == country_name)
        print(f"{i}. {country_name}: {country_data['capital']}")
    
    print(f"\n📋 EKSEMPLER - LAND UTEN HOVEDSTAD:")
    print("-" * 40)
    for i, country_name in enumerate(countries_without_capital[:5], 1):
        print(f"{i}. {country_name}")

if __name__ == "__main__":
    check_missing_capitals()
