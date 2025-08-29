#!/usr/bin/env python3
"""
Analyze Switzerland's borders using geodatasource country-borders dataset (Fixed version)
"""

import csv

def analyze_switzerland_borders():
    """Analyze Switzerland's border countries"""
    
    print("🇨🇭 ANALYSERER SVEITS' GRENSER")
    print("=" * 40)
    
    # Dictionary to store country names
    country_names = {}
    switzerland_borders = []
    
    try:
        with open('country-borders.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                country_code = row['country_code']
                country_name = row['country_name']
                border_code = row['country_border_code']
                border_name = row['country_border_name']
                
                # Store country names
                country_names[country_code] = country_name
                
                # If this is Switzerland's border, store it
                if country_code == 'CH':
                    switzerland_borders.append({
                        'code': border_code,
                        'name': border_name
                    })
        
        if switzerland_borders:
            print(f"✅ Sveits (CH) har {len(switzerland_borders)} naboland:")
            print()
            
            for i, border in enumerate(switzerland_borders, 1):
                print(f"   {i}. {border['name']} ({border['code']})")
            
            print()
            print("📊 Statistikk:")
            print(f"   Totalt antall naboland: {len(switzerland_borders)}")
            
            # Get unique border countries
            unique_borders = set()
            for border in switzerland_borders:
                unique_borders.add(border['code'])
            
            print(f"   Unike naboland: {len(unique_borders)}")
            
            # Find countries that border Switzerland
            countries_bordering_switzerland = []
            with open('country-borders.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['country_border_code'] == 'CH':
                        countries_bordering_switzerland.append({
                            'code': row['country_code'],
                            'name': row['country_name']
                        })
            
            print(f"   Land som grenser til Sveits: {len(countries_bordering_switzerland)}")
            
            if countries_bordering_switzerland:
                print("   Land som har Sveits som nabo:")
                for country in countries_bordering_switzerland:
                    print(f"     - {country['name']} ({country['code']})")
            
            print()
            print("🗺️ Geografisk plassering:")
            print("   Sveits er et innlandsland i Sentral-Europa")
            print("   Det grenser til:")
            print("   - Nord: Tyskland")
            print("   - Øst: Østerrike og Liechtenstein") 
            print("   - Sør: Italia")
            print("   - Vest: Frankrike")
            
        else:
            print("❌ Sveits ikke funnet i datasettet")
            
    except Exception as e:
        print(f"❌ Feil ved analyse: {e}")

if __name__ == "__main__":
    analyze_switzerland_borders()
