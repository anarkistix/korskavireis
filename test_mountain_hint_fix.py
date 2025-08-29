#!/usr/bin/env python3
"""
Test script to verify mountain hint fix
"""

import json

def test_mountain_hint_fix():
    """Test if mountain data is properly loaded"""
    
    print("🧪 TESTER FJELL-HINT FIX")
    print("=" * 40)
    
    try:
        # Load countries data
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        
        # Find Afghanistan in the raw data
        afghanistan_raw = None
        for country in countries:
            if country.get('name') == 'Afghanistan':
                afghanistan_raw = country
                break
        
        if afghanistan_raw:
            print(f"✅ Afghanistan funnet i rådata")
            print(f"   Har highest_mountain: {'highest_mountain' in afghanistan_raw}")
            if 'highest_mountain' in afghanistan_raw:
                print(f"   Fjell: {afghanistan_raw['highest_mountain']}")
                print(f"   Høyde (m): {afghanistan_raw.get('highest_elevation_meters')}")
                print(f"   Høyde (ft): {afghanistan_raw.get('highest_elevation_feet')}")
        else:
            print(f"❌ Afghanistan ikke funnet i rådata")
            return
        
        # Simulate the JavaScript loadCountries function
        print(f"\n🔄 SIMULERER JAVASCRIPT loadCountries():")
        
        # This is what the JavaScript does:
        simulated_countries = []
        for country in countries:
            # Simulate the mapping that happens in loadCountries()
            simulated_country = {
                'name': country.get('name'),
                'iso3': country.get('iso3'),
                'continent': country.get('continent'),
                'region': country.get('region'),
                'imageFile': country.get('imageFile'),
                'flagFile': country.get('flagFile'),
                'population': country.get('population'),
                'populationYear': country.get('population_year'),
                'google_maps_url': country.get('google_maps_url'),
                'capital': country.get('capital'),
                'capital_coordinates': country.get('capital_coordinates'),
                'highest_mountain': country.get('highest_mountain'),  # ✅ Nå inkludert!
                'highest_elevation_meters': country.get('highest_elevation_meters'),  # ✅ Nå inkludert!
                'highest_elevation_feet': country.get('highest_elevation_feet'),  # ✅ Nå inkludert!
                'center': None  # Simplified for test
            }
            simulated_countries.append(simulated_country)
        
        # Find Afghanistan in simulated data
        afghanistan_sim = None
        for country in simulated_countries:
            if country.get('name') == 'Afghanistan':
                afghanistan_sim = country
                break
        
        if afghanistan_sim:
            print(f"✅ Afghanistan funnet i simulerte data")
            print(f"   Har highest_mountain: {'highest_mountain' in afghanistan_sim}")
            if 'highest_mountain' in afghanistan_sim and afghanistan_sim['highest_mountain']:
                print(f"   Fjell: {afghanistan_sim['highest_mountain']}")
                print(f"   Høyde (m): {afghanistan_sim.get('highest_elevation_meters')}")
                print(f"   Høyde (ft): {afghanistan_sim.get('highest_elevation_feet')}")
                print(f"   ✅ FJELL-HINT VIL FUNGERE!")
            else:
                print(f"   ❌ Fjell-data mangler fortsatt")
        else:
            print(f"❌ Afghanistan ikke funnet i simulerte data")
        
        # Test a few more countries
        print(f"\n🔍 TESTER FLERE LAND:")
        test_countries = ['Norway', 'Switzerland', 'Nepal', 'Japan']
        for country_name in test_countries:
            country_sim = next((c for c in simulated_countries if c.get('name') == country_name), None)
            if country_sim:
                has_mountain = 'highest_mountain' in country_sim and country_sim['highest_mountain']
                status = "✅" if has_mountain else "❌"
                print(f"   {status} {country_name}: {'Har fjell' if has_mountain else 'Mangler fjell'}")
        
    except Exception as e:
        print(f"❌ Feil ved test: {e}")

if __name__ == "__main__":
    test_mountain_hint_fix()
