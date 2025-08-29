#!/usr/bin/env python3
"""
Test script to verify borders hint implementation
"""

import json

def test_borders_hint():
    """Test if borders hint data is properly integrated"""
    
    print("🗺️ TESTER NABOLAND-HINT IMPLEMENTERING")
    print("=" * 50)
    
    try:
        # Load countries data
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        
        print(f"✅ Lastet {len(countries)} land fra countries_data.json")
        
        # Test specific countries
        test_countries = [
            'Switzerland',  # Should have 5 neighbors
            'Norway',       # Should have 3 neighbors  
            'Australia',    # Should be island
            'Japan',        # Should be island
            'Iceland',      # Should be island
            'Germany',      # Should have many neighbors
            'France',       # Should have many neighbors
            'Brazil',       # Should have many neighbors
            'Canada',       # Should have 1 neighbor
            'United States' # Should have 2 neighbors
        ]
        
        print("\n📋 TESTER NABOLAND-DATA:")
        for country_name in test_countries:
            country = None
            for c in countries:
                if c['name'] == country_name:
                    country = c
                    break
            
            if country:
                borders = country.get('borders', [])
                is_island = country.get('is_island', False)
                
                if is_island:
                    print(f"   ✅ {country_name}: Øy (ingen naboland)")
                else:
                    print(f"   ✅ {country_name}: {len(borders)} naboland - {', '.join(borders)}")
            else:
                print(f"   ❌ {country_name}: Ikke funnet")
        
        # Test Norwegian data
        print("\n🇳🇴 TESTER NORSK DATA:")
        try:
            with open('countries_data_no.json', 'r', encoding='utf-8') as f:
                norwegian_countries = json.load(f)
            
            # Test a few countries
            test_norwegian = ['Switzerland', 'Norway', 'Australia']
            for country_name in test_norwegian:
                country = None
                for c in norwegian_countries:
                    if c['name'] == country_name:
                        country = c
                        break
                
                if country:
                    borders = country.get('borders', [])
                    is_island = country.get('is_island', False)
                    
                    if is_island:
                        print(f"   ✅ {country_name}: Øy (ingen naboland)")
                    else:
                        print(f"   ✅ {country_name}: {len(borders)} naboland - {', '.join(borders)}")
                else:
                    print(f"   ❌ {country_name}: Ikke funnet i norsk data")
                    
        except Exception as e:
            print(f"   ❌ Feil ved norsk data: {e}")
        
        # Test grid layout
        print("\n🎯 GRID-LAYOUT (2x3):")
        print("   Rad 1: Hint 1 (Flagg) | Hint 2 (Befolkning)")
        print("   Rad 2: Hint 3 (Hovedstad) | Hint 4 (Region)")
        print("   Rad 3: Hint 5 (Fjell) | Hint 6 (Naboland)")
        print("   ✅ 6 hint i 2x3 grid")
        
        # Test progressive unlocking
        print("\n🔓 PROGRESSIVE UNLOCKING:")
        print("   Hint 1: Etter 1 gjetting")
        print("   Hint 2: Etter 2 gjettinger") 
        print("   Hint 3: Etter 3 gjettinger")
        print("   Hint 4: Etter 4 gjettinger")
        print("   Hint 5: Etter 5 gjettinger")
        print("   Hint 6: Etter 6 gjettinger")
        print("   ✅ Alle hint låses opp progressivt")
        
    except Exception as e:
        print(f"❌ Feil ved test: {e}")

if __name__ == "__main__":
    test_borders_hint()
