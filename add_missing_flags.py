#!/usr/bin/env python3
import json
import os

def add_missing_flags():
    """Legger til flagFile for land som manglet flagg"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"🔧 Legger til flagg for land som manglet...")
    
    # Liste over land som manglet flagg
    missing_countries = ['Israel', 'East Timor', 'Liberia', 'Venezuela']
    flag_mapping = {
        'Israel': 'il.png',
        'East Timor': 'tl.png', 
        'Liberia': 'lr.png',
        'Venezuela': 've.png'
    }
    
    updated_count = 0
    
    for country in countries:
        if country['name'] in missing_countries and not country.get('flagFile'):
            flag_file = flag_mapping[country['name']]
            flag_path = os.path.join('flags', flag_file)
            
            if os.path.exists(flag_path):
                country['flagFile'] = flag_file
                print(f"✅ {country['name']}: lagt til {flag_file}")
                updated_count += 1
            else:
                print(f"❌ {country['name']}: {flag_file} ikke funnet")
    
    # Lagre oppdatert data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Oppdatering fullført!")
    print(f"✅ {updated_count} land oppdatert")
    
    # Vis statistikk
    countries_with_flags = sum(1 for c in countries if c.get('flagFile') and os.path.exists(os.path.join('flags', c['flagFile'])))
    print(f"📊 Land med fungerende flagg: {countries_with_flags}/{len(countries)} ({countries_with_flags/len(countries)*100:.1f}%)")

if __name__ == "__main__":
    add_missing_flags()
