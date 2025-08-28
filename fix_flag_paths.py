#!/usr/bin/env python3
import json

def fix_flag_paths():
    """Fjerner 'flags/' prefikset fra flagFile-feltene"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"🔄 Fikser flagg-stier for {len(countries)} land...")
    
    updated_count = 0
    
    for country in countries:
        flag_file = country.get('flagFile', '')
        if flag_file and flag_file.startswith('flags/'):
            old_flag = flag_file
            new_flag = flag_file.replace('flags/', '')
            country['flagFile'] = new_flag
            print(f"✅ {country['name']} ({country.get('iso_code', 'N/A')}): {old_flag} -> {new_flag}")
            updated_count += 1
    
    # Lagre oppdatert data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Oppdatering fullført!")
    print(f"✅ {updated_count} land oppdatert")

if __name__ == "__main__":
    fix_flag_paths()
