#!/usr/bin/env python3
"""
Integrate border data from country-borders CSV into countries_data.json (Fixed version)
"""

import json
import csv
from collections import defaultdict

def integrate_border_data():
    """Integrate border data into countries_data.json"""
    
    print("🗺️ INTEGRERER NABOLAND-DATA (FIKSET VERSJON)")
    print("=" * 50)
    
    try:
        # Load existing countries data
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        
        print(f"✅ Lastet {len(countries)} land fra countries_data.json")
        
        # Create ISO2 to ISO3 mapping
        iso2_to_iso3 = {}
        iso3_to_name = {}
        for country in countries:
            # Extract ISO2 from ISO3 (first 2 characters)
            iso2 = country['iso3'][:2]
            iso2_to_iso3[iso2] = country['iso3']
            iso3_to_name[country['iso3']] = country['name']
        
        print(f"✅ Opprettet mapping for {len(iso2_to_iso3)} land")
        
        # Load border data and convert to ISO3
        borders = defaultdict(list)
        with open('country-borders.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                country_code_iso2 = row['country_code']
                border_code_iso2 = row['country_border_code']
                
                # Convert to ISO3
                if country_code_iso2 in iso2_to_iso3:
                    country_code_iso3 = iso2_to_iso3[country_code_iso2]
                    if border_code_iso2 in iso2_to_iso3:
                        border_code_iso3 = iso2_to_iso3[border_code_iso2]
                        border_name = iso3_to_name.get(border_code_iso3, row['country_border_name'])
                        borders[country_code_iso3].append(border_name)
        
        print(f"✅ Konvertert naboland-data for {len(borders)} land")
        
        # Integrate border data into countries
        updated_count = 0
        for country in countries:
            iso3 = country['iso3']
            if iso3 in borders:
                # Get border countries
                border_names = borders[iso3]
                
                # Convert border names to Norwegian if possible
                border_names_norwegian = []
                for border_name in border_names:
                    # Find the Norwegian name for this border country
                    norwegian_name = None
                    for other_country in countries:
                        if other_country['name'] == border_name:
                            norwegian_name = other_country.get('name_no', border_name)
                            break
                    border_names_norwegian.append(norwegian_name or border_name)
                
                # Add border data
                country['borders'] = border_names
                country['borders_no'] = border_names_norwegian
                country['is_island'] = len(border_names) == 0
                updated_count += 1
            else:
                # No borders found - mark as island
                country['borders'] = []
                country['borders_no'] = []
                country['is_island'] = True
                updated_count += 1
        
        # Save updated data
        with open('countries_data.json', 'w', encoding='utf-8') as f:
            json.dump(countries, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Oppdatert {updated_count} land med naboland-data")
        
        # Show some examples
        print("\n📋 Eksempler på naboland-data:")
        examples = ['Switzerland', 'Norway', 'Australia', 'Japan', 'Iceland']
        for example_name in examples:
            for country in countries:
                if country['name'] == example_name:
                    borders_list = country.get('borders', [])
                    is_island = country.get('is_island', False)
                    if is_island:
                        print(f"   {example_name}: Øy (ingen naboland)")
                    else:
                        print(f"   {example_name}: {', '.join(borders_list)}")
                    break
        
        # Also update Norwegian data
        print("\n🇳🇴 OPPDATERER NORSK DATA:")
        try:
            with open('countries_data_no.json', 'r', encoding='utf-8') as f:
                norwegian_countries = json.load(f)
            
            # Update Norwegian countries with border data
            for norwegian_country in norwegian_countries:
                iso3 = norwegian_country['iso3']
                if iso3 in borders:
                    border_names = borders[iso3]
                    norwegian_country['borders'] = border_names
                    norwegian_country['is_island'] = len(border_names) == 0
                else:
                    norwegian_country['borders'] = []
                    norwegian_country['is_island'] = True
            
            with open('countries_data_no.json', 'w', encoding='utf-8') as f:
                json.dump(norwegian_countries, f, indent=2, ensure_ascii=False)
            
            print("✅ Norsk data oppdatert med naboland")
            
        except Exception as e:
            print(f"❌ Feil ved oppdatering av norsk data: {e}")
        
    except Exception as e:
        print(f"❌ Feil ved integrasjon: {e}")

if __name__ == "__main__":
    integrate_border_data()
