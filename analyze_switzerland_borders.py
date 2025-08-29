#!/usr/bin/env python3
"""
Analyze Switzerland's borders using geodatasource country-borders dataset
"""

import csv
from collections import defaultdict

def analyze_switzerland_borders():
    """Analyze Switzerland's border countries"""
    
    print("🇨🇭 ANALYSERER SVEITS' GRENSER")
    print("=" * 40)
    
    # Dictionary to store border relationships
    borders = defaultdict(list)
    
    try:
        with open('country-borders.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                country_code = row['country_code']
                country_name = row['country_name']
                border_code = row['country_border_code']
                border_name = row['country_border_name']
                
                # Store both directions of the border relationship
                borders[country_code].append({
                    'code': border_code,
                    'name': border_name
                })
        
        # Find Switzerland's borders
        switzerland_code = 'CH'
        if switzerland_code in borders:
            switzerland_borders = borders[switzerland_code]
            
            print(f"✅ Sveits (CH) har {len(switzerland_borders)} naboland:")
            print()
            
            for i, border in enumerate(switzerland_borders, 1):
                print(f"   {i}. {border['name']} ({border['code']})")
            
            print()
            print("📊 Statistikk:")
            print(f"   Totalt antall naboland: {len(switzerland_borders)}")
            
            # Get unique border countries (in case of duplicates)
            unique_borders = set()
            for border in switzerland_borders:
                unique_borders.add(border['code'])
            
            print(f"   Unike naboland: {len(unique_borders)}")
            
            # Check if Switzerland appears as a border for other countries
            countries_bordering_switzerland = []
            for country_code, country_borders_list in borders.items():
                for border in country_borders_list:
                    if border['code'] == switzerland_code:
                        countries_bordering_switzerland.append(country_code)
                        break
            
            print(f"   Land som grenser til Sveits: {len(countries_bordering_switzerland)}")
            
            if countries_bordering_switzerland:
                print("   Land som har Sveits som nabo:")
                for country_code in countries_bordering_switzerland:
                    # Find country name
                    country_name = None
                    for code, borders_list in borders.items():
                        if code == country_code:
                            # Get country name from first border entry
                            if borders_list:
                                # This is a bit of a workaround, but it works
                                country_name = borders_list[0].get('name', country_code)
                            break
                    print(f"     - {country_name} ({country_code})")
            
        else:
            print("❌ Sveits ikke funnet i datasettet")
            
    except Exception as e:
        print(f"❌ Feil ved analyse: {e}")

if __name__ == "__main__":
    analyze_switzerland_borders()
