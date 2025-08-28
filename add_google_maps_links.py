#!/usr/bin/env python3
import json
import requests
import time

def add_google_maps_links():
    """Legger til Google Maps lenker for alle land"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"🌍 Legger til Google Maps lenker for {len(countries)} land...")
    print("=" * 60)
    
    updated_count = 0
    working_links = 0
    failed_links = 0
    
    for i, country in enumerate(countries, 1):
        country_name = country['name']
        
        # Generer Google Maps link
        # Erstatt mellomrom med + for URL-encoding
        encoded_name = country_name.replace(' ', '+')
        google_maps_url = f"https://www.google.com/maps/search/{encoded_name}"
        
        # Test om linken fungerer (HTTP 200 OK)
        try:
            response = requests.get(google_maps_url, timeout=10)
            if response.status_code == 200:
                status = "✅ FUNGERER"
                working_links += 1
            else:
                status = f"❌ HTTP {response.status_code}"
                failed_links += 1
        except Exception as e:
            status = f"❌ FEIL: {str(e)[:30]}..."
            failed_links += 1
        
        # Legg til link i country data
        country['google_maps_url'] = google_maps_url
        
        print(f"{i:3d}. {country_name:<25} | {status}")
        print(f"     {google_maps_url}")
        
        # Kort pause for å ikke overbelaste Google
        time.sleep(0.1)
    
    # Lagre oppdatert data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("🎉 Oppdatering fullført!")
    print(f"✅ {updated_count} land oppdatert")
    print(f"✅ {working_links} fungerende lenker")
    print(f"❌ {failed_links} feilede lenker")
    print(f"📊 Suksessrate: {working_links/(working_links+failed_links)*100:.1f}%")
    
    # Vis eksempel på oppdatert data
    print("\n📋 EKSEMPEL - OPPDATERT LAND:")
    print("-" * 50)
    for i, country in enumerate(countries[:3], 1):
        print(f"{i}. {country['name']}")
        print(f"   Google Maps: {country['google_maps_url']}")
        print()

if __name__ == "__main__":
    add_google_maps_links()
