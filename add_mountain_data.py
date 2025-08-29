#!/usr/bin/env python3
"""
Script to add mountain data to countries_data.json
Extracts highest point data from Wikipedia elevation extremes
"""

import json
import re
import requests
from bs4 import BeautifulSoup

def extract_mountain_data():
    """Extract mountain data from Wikipedia elevation extremes page"""
    
    url = "https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country"
    
    print("🌍 Henter fjelldata fra Wikipedia...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main table
        table = soup.find('table', {'class': 'wikitable'})
        if not table:
            print("❌ Kunne ikke finne tabellen")
            return {}
        
        mountain_data = {}
        
        # Process table rows
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 3:
                # Extract country name
                country_cell = cells[0]
                country_link = country_cell.find('a')
                if country_link:
                    country_name = country_link.get_text(strip=True)
                else:
                    country_name = country_cell.get_text(strip=True)
                
                # Extract highest point
                highest_point_cell = cells[1]
                highest_point_link = highest_point_cell.find('a')
                if highest_point_link:
                    highest_point_name = highest_point_link.get_text(strip=True)
                else:
                    highest_point_name = highest_point_cell.get_text(strip=True)
                
                # Extract elevation
                elevation_cell = cells[2]
                elevation_text = elevation_cell.get_text(strip=True)
                
                # Parse elevation (extract meters)
                elevation_match = re.search(r'(\d+(?:,\d+)*)\s*m', elevation_text)
                if elevation_match:
                    elevation_meters = int(elevation_match.group(1).replace(',', ''))
                else:
                    elevation_meters = None
                
                # Clean up country name (remove flag emoji and extra spaces)
                country_name = re.sub(r'^[^\w\s]*', '', country_name).strip()
                
                if country_name and highest_point_name and elevation_meters:
                    mountain_data[country_name] = {
                        'mountain_name': highest_point_name,
                        'elevation_meters': elevation_meters,
                        'elevation_feet': int(elevation_meters * 3.28084)  # Convert to feet
                    }
                    print(f"✅ {country_name}: {highest_point_name} ({elevation_meters}m)")
        
        print(f"\n📊 Funnet fjelldata for {len(mountain_data)} land")
        return mountain_data
        
    except Exception as e:
        print(f"❌ Feil ved henting av data: {e}")
        return {}

def update_countries_data(mountain_data):
    """Update countries_data.json with mountain information"""
    
    print("\n📝 Oppdaterer countries_data.json...")
    
    try:
        # Load existing data
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        
        updated_count = 0
        
        for country in countries:
            country_name = country.get('name', '')
            
            # Try exact match first
            if country_name in mountain_data:
                mountain_info = mountain_data[country_name]
                country['highest_mountain'] = mountain_info['mountain_name']
                country['highest_elevation_meters'] = mountain_info['elevation_meters']
                country['highest_elevation_feet'] = mountain_info['elevation_feet']
                updated_count += 1
                print(f"✅ Oppdatert {country_name}: {mountain_info['mountain_name']}")
                continue
            
            # Try partial matches for common variations
            for wiki_name, mountain_info in mountain_data.items():
                if (country_name.lower() in wiki_name.lower() or 
                    wiki_name.lower() in country_name.lower()):
                    country['highest_mountain'] = mountain_info['mountain_name']
                    country['highest_elevation_meters'] = mountain_info['elevation_meters']
                    country['highest_elevation_feet'] = mountain_info['elevation_feet']
                    updated_count += 1
                    print(f"✅ Oppdatert {country_name} (match: {wiki_name}): {mountain_info['mountain_name']}")
                    break
        
        # Save updated data
        with open('countries_data.json', 'w', encoding='utf-8') as f:
            json.dump(countries, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Oppdatert {updated_count} land med fjelldata")
        print(f"💾 Lagret til countries_data.json")
        
        return updated_count
        
    except Exception as e:
        print(f"❌ Feil ved oppdatering: {e}")
        return 0

def main():
    print("🏔️ LEGGER TIL FJELLDATA I KORSAKAVIREIS")
    print("=" * 50)
    
    # Extract mountain data from Wikipedia
    mountain_data = extract_mountain_data()
    
    if not mountain_data:
        print("❌ Kunne ikke hente fjelldata")
        return
    
    # Update countries_data.json
    updated_count = update_countries_data(mountain_data)
    
    print(f"\n🎉 FERDIG!")
    print(f"📊 Oppdatert {updated_count} land med fjelldata")
    print(f"🏔️ Nye felter: highest_mountain, highest_elevation_meters, highest_elevation_feet")

if __name__ == "__main__":
    main()
