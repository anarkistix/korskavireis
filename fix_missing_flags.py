#!/usr/bin/env python3
import json
import os

def fix_missing_flags():
    """Fikser manglende flagg ved å sette flagFile til null"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"🔧 Fikser manglende flagg for {len(countries)} land...")
    
    # Liste over land som mangler flagg
    missing_flags = ['Israel', 'East Timor', 'Liberia', 'Venezuela']
    
    fixed_count = 0
    
    for country in countries:
        flag_file = country.get('flagFile', '')
        if not flag_file:
            continue
            
        # Sjekk om filen faktisk eksisterer
        flag_path = os.path.join('flags', flag_file)
        if not os.path.exists(flag_path):
            print(f"❌ {country['name']}: {flag_file} (fil ikke funnet) - fjerner flagg")
            country['flagFile'] = None
            fixed_count += 1
    
    # Lagre oppdatert data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Fiksing fullført!")
    print(f"✅ {fixed_count} land fikset")
    
    # Vis statistikk
    countries_with_flags = sum(1 for c in countries if c.get('flagFile') and os.path.exists(os.path.join('flags', c['flagFile'])))
    print(f"📊 Land med fungerende flagg: {countries_with_flags}/{len(countries)}")

if __name__ == "__main__":
    fix_missing_flags()
