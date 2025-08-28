#!/usr/bin/env python3
import json
import os

def update_flag_files():
    """Oppdaterer flagFile-feltene i countries_data.json for å bruke de nye flaggene"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    # Liste over nye flagg som er tilgjengelige
    new_flags = [
        'dm', 'dz', 'eh', 'fr', 'ga', 'gw', 'hm', 'hn', 
        'je', 'jp', 'ph', 'rw', 'sd', 'se', 'sr', 'ss'
    ]
    
    print(f"🔄 Oppdaterer flagFile for {len(new_flags)} land...")
    
    updated_count = 0
    
    for country in countries:
        # Sjekk om landet har et nytt flagg
        if country.get('iso_code') in new_flags:
            old_flag = country.get('flagFile', '')
            new_flag = f"{country['iso_code']}.png"
            
            if old_flag != new_flag:
                country['flagFile'] = new_flag
                print(f"✅ {country['name']} ({country['iso_code']}): {old_flag} -> {new_flag}")
                updated_count += 1
            else:
                print(f"⏭️  {country['name']} ({country['iso_code']}): allerede oppdatert")
    
    # Lagre oppdatert data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Oppdatering fullført!")
    print(f"✅ {updated_count} land oppdatert")
    print(f"📁 Fil lagret: countries_data.json")
    
    # Vis statistikk
    total_countries = len(countries)
    countries_with_flags = sum(1 for c in countries if c.get('flagFile'))
    
    print(f"\n📊 Statistikk:")
    print(f"🌍 Totalt antall land: {total_countries}")
    print(f"🏁 Land med flagg: {countries_with_flags}")
    print(f"📈 Dekning: {countries_with_flags/total_countries*100:.1f}%")

if __name__ == "__main__":
    if not os.path.exists('countries_data.json'):
        print("❌ countries_data.json ikke funnet!")
        exit(1)
    
    update_flag_files()
