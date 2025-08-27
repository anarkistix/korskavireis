import json
import csv
from collections import defaultdict

def load_population_data():
    """Last befolkningsdata fra CSV-filen"""
    population_data = {}
    
    with open('population-main/data/population.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            country_code = row['Country Code']
            year = int(row['Year'])
            value = int(float(row['Value']))
            
            # Lagre siste tilgjengelige år for hvert land
            if country_code not in population_data or year > population_data[country_code]['year']:
                population_data[country_code] = {
                    'year': year,
                    'population': value
                }
    
    return population_data

def load_countries_data():
    """Last eksisterende landdata"""
    with open('countries_data.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def save_countries_data(data):
    """Lagre oppdatert landdata"""
    with open('countries_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def main():
    print("Laster befolkningsdata...")
    population_data = load_population_data()
    
    print("Laster eksisterende landdata...")
    countries_data = load_countries_data()
    
    print("Mapper befolkningsdata til land...")
    countries_with_population = 0
    
    for country in countries_data:
        iso3 = country.get('iso3')
        if iso3 and iso3 in population_data:
            country['population'] = population_data[iso3]['population']
            country['population_year'] = population_data[iso3]['year']
            countries_with_population += 1
            print(f"✓ {country['name']}: {population_data[iso3]['population']:,} ({population_data[iso3]['year']})")
        else:
            country['population'] = None
            country['population_year'] = None
            print(f"❌ {country['name']}: Ingen befolkningsdata funnet")
    
    print(f"\nLagrer oppdatert data...")
    save_countries_data(countries_data)
    
    print(f"Ferdig! {countries_with_population} av {len(countries_data)} land har befolkningsdata.")

if __name__ == "__main__":
    main()
