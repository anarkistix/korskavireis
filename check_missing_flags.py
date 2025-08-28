#!/usr/bin/env python3
import json
import os

def check_missing_flags():
    """Sjekker hvilke land som mangler flagg"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"🔍 Sjekker flagg-status for {len(countries)} land...")
    print("=" * 60)
    
    missing_flags = []
    has_flags = []
    
    for country in countries:
        flag_file = country.get('flagFile')
        
        if not flag_file:
            missing_flags.append(country)
        else:
            # Sjekk om filen faktisk eksisterer
            flag_path = os.path.join('flags', flag_file)
            if os.path.exists(flag_path):
                has_flags.append(country)
            else:
                missing_flags.append(country)
    
    print(f"✅ Land med flagg: {len(has_flags)}")
    print(f"❌ Land uten flagg: {len(missing_flags)}")
    print(f"📊 Total: {len(countries)}")
    print()
    
    if missing_flags:
        print("🚩 LAND UTEN FLAGG:")
        print("-" * 40)
        for i, country in enumerate(missing_flags, 1):
            flag_file = country.get('flagFile', 'INGEN')
            print(f"{i:2d}. {country['name']:<25} | {flag_file}")
    else:
        print("🎉 Alle land har flagg!")
    
    print()
    print("📋 SAMMENDRAG:")
    print(f"   • Land med fungerende flagg: {len(has_flags)}")
    print(f"   • Land uten flagg: {len(missing_flags)}")
    print(f"   • Prosent med flagg: {len(has_flags)/len(countries)*100:.1f}%")

if __name__ == "__main__":
    check_missing_flags()
