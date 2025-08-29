#!/usr/bin/env python3
"""
Script to specifically check Afghanistan's mountain data
"""

import json

def check_afghanistan_mountain():
    """Check if Afghanistan has mountain data"""
    
    print("🏔️ SJEKKER AFGHANISTAN FJELLDATA")
    print("=" * 40)
    
    try:
        # Load countries data
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        
        # Find Afghanistan
        afghanistan = None
        for country in countries:
            if country.get('name') == 'Afghanistan':
                afghanistan = country
                break
        
        if afghanistan:
            print(f"✅ Afghanistan funnet i databasen")
            print(f"   Land: {afghanistan.get('name')}")
            print(f"   ISO3: {afghanistan.get('iso3')}")
            
            # Check mountain data
            if 'highest_mountain' in afghanistan:
                print(f"   🏔️ Høyeste fjell: {afghanistan['highest_mountain']}")
                print(f"   📏 Høyde (meter): {afghanistan.get('highest_elevation_meters', 'N/A')}")
                print(f"   📏 Høyde (fot): {afghanistan.get('highest_elevation_feet', 'N/A')}")
                print(f"   ✅ Afghanistan HAR fjelldata")
            else:
                print(f"   ❌ Afghanistan mangler fjelldata")
                print(f"   Tilgjengelige felter: {list(afghanistan.keys())}")
        else:
            print(f"❌ Afghanistan ikke funnet i databasen")
            print(f"   Tilgjengelige land: {[c.get('name') for c in countries[:10]]}...")
        
        # Also check Norwegian data
        print(f"\n🇳🇴 SJEKKER NORSK AFGHANISTAN DATA:")
        try:
            with open('countries_data_no.json', 'r', encoding='utf-8') as f:
                norwegian_countries = json.load(f)
            
            afghanistan_no = None
            for country in norwegian_countries:
                if country.get('name') == 'Afghanistan':
                    afghanistan_no = country
                    break
            
            if afghanistan_no:
                print(f"✅ Afghanistan funnet i norsk databasen")
                if 'highest_mountain' in afghanistan_no:
                    print(f"   🏔️ Høyeste fjell: {afghanistan_no['highest_mountain']}")
                    print(f"   📏 Høyde (meter): {afghanistan_no.get('highest_elevation_meters', 'N/A')}")
                    print(f"   📏 Høyde (fot): {afghanistan_no.get('highest_elevation_feet', 'N/A')}")
                    print(f"   ✅ Norsk Afghanistan HAR fjelldata")
                else:
                    print(f"   ❌ Norsk Afghanistan mangler fjelldata")
            else:
                print(f"❌ Afghanistan ikke funnet i norsk databasen")
        except Exception as e:
            print(f"❌ Feil ved sjekk av norsk data: {e}")
        
    except Exception as e:
        print(f"❌ Feil ved sjekk: {e}")

if __name__ == "__main__":
    check_afghanistan_mountain()
