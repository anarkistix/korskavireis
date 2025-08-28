#!/usr/bin/env python3
import json

def add_missing_capitals():
    """Legger til hovedstadsdata for land som mangler"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"🌍 Legger til hovedstadsdata for 10 land som mangler...")
    print("=" * 60)
    
    # Hovedstadsdata som skal legges til
    capital_updates = {
        'Vatican City': {
            'capital': 'Vatikanstaten',
            'capital_coordinates': {'lat': 41.9028, 'lon': 12.4534}
        },
        'North Macedonia': {
            'capital': 'Skopje',
            'capital_coordinates': {'lat': 42.0, 'lon': 21.4333}
        },
        'East Timor': {
            'capital': 'Dili',
            'capital_coordinates': {'lat': -8.5586, 'lon': 125.5736}
        },
        'South Sudan': {
            'capital': 'Juba',
            'capital_coordinates': {'lat': 4.8594, 'lon': 31.5713}
        },
        'South Korea': {
            'capital': 'Seoul',
            'capital_coordinates': {'lat': 37.5665, 'lon': 126.9780}
        },
        'Eswatini': {
            'capital': 'Mbabane (administrativ) / Lobamba (lovgivende)',
            'capital_coordinates': {'lat': -26.3054, 'lon': 31.1367}  # Mbabane koordinater
        },
        'North Korea': {
            'capital': 'Pyongyang',
            'capital_coordinates': {'lat': 39.0194, 'lon': 125.7547}
        },
        'Congo': {
            'capital': 'Brazzaville',
            'capital_coordinates': {'lat': -4.2634, 'lon': 15.2429}
        },
        'Democratic Republic of the Congo': {
            'capital': 'Kinshasa',
            'capital_coordinates': {'lat': -4.4419, 'lon': 15.2663}
        },
        'Nauru': {
            'capital': 'Yaren (administrasjonssenter)',
            'capital_coordinates': {'lat': -0.5228, 'lon': 166.9315}
        }
    }
    
    updated_count = 0
    
    for country in countries:
        if country['name'] in capital_updates:
            old_capital = country.get('capital')
            old_coordinates = country.get('capital_coordinates')
            
            # Oppdater data
            country['capital'] = capital_updates[country['name']]['capital']
            country['capital_coordinates'] = capital_updates[country['name']]['capital_coordinates']
            
            print(f"✅ {country['name']}:")
            print(f"   Hovedstad: {old_capital or 'Ingen'} → {country['capital']}")
            print(f"   Koordinater: {old_coordinates or 'Ingen'} → {country['capital_coordinates']}")
            updated_count += 1
    
    # Lagre oppdatert data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Oppdatering fullført!")
    print(f"✅ {updated_count} land oppdatert med hovedstadsdata")
    
    # Vis statistikk
    countries_with_capital = sum(1 for c in countries if c.get('capital'))
    print(f"📊 Land med hovedstadsdata: {countries_with_capital}/{len(countries)} ({countries_with_capital/len(countries)*100:.1f}%)")
    
    # Vis eksempel på oppdatert data
    print("\n📋 EKSEMPEL - OPPDATERTE LAND:")
    print("-" * 50)
    for country_name in ['Vatican City', 'North Macedonia', 'South Korea']:
        country = next(c for c in countries if c['name'] == country_name)
        print(f"• {country['name']}: {country['capital']}")
        print(f"  Koordinater: {country['capital_coordinates']['lat']:.4f}, {country['capital_coordinates']['lon']:.4f}")

if __name__ == "__main__":
    add_missing_capitals()
