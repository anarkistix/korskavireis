#!/usr/bin/env python3
import json
import os

def update_flag_filenames():
    """Oppdaterer alle flagFile-feltene til å bruke nye filnavn"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"🔄 Oppdaterer flagg-filnavn for {len(countries)} land...")
    
    updated_count = 0
    not_found_count = 0
    
    for country in countries:
        flag_file = country.get('flagFile', '')
        if not flag_file:
            continue
            
        # Fjern "flags/" prefiks hvis det finnes
        if flag_file.startswith('flags/'):
            flag_file = flag_file.replace('flags/', '')
        
        # Konverter til nytt format (små bokstaver, .png)
        if flag_file.endswith('-128.png'):
            # Gammelt format: DK-128.png -> dk.png
            iso_code = flag_file.replace('-128.png', '').lower()
            new_flag = f"{iso_code}.png"
        elif flag_file.endswith('.png'):
            # Allerede i nytt format
            new_flag = flag_file
        else:
            # Ingen endring
            new_flag = flag_file
        
        # Sjekk om filen faktisk eksisterer
        flag_path = os.path.join('flags', new_flag)
        if os.path.exists(flag_path):
            if country['flagFile'] != new_flag:
                old_flag = country['flagFile']
                country['flagFile'] = new_flag
                print(f"✅ {country['name']}: {old_flag} -> {new_flag}")
                updated_count += 1
        else:
            print(f"❌ {country['name']}: {new_flag} (fil ikke funnet)")
            not_found_count += 1
    
    # Lagre oppdatert data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Oppdatering fullført!")
    print(f"✅ {updated_count} land oppdatert")
    print(f"❌ {not_found_count} land med manglende flagg")
    
    # Vis statistikk
    countries_with_flags = sum(1 for c in countries if c.get('flagFile') and os.path.exists(os.path.join('flags', c['flagFile'])))
    print(f"📊 Land med fungerende flagg: {countries_with_flags}/{len(countries)}")

if __name__ == "__main__":
    update_flag_filenames()
