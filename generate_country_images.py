import json
import matplotlib.pyplot as plt
from shapely.geometry import shape
import os
import re

# Importer anerkjente land
from recognized_countries import RECOGNIZED_COUNTRIES, ALTERNATIVE_NAMES

# Opprett mappe for bilder hvis den ikke eksisterer
if not os.path.exists('country_images'):
    os.makedirs('country_images')

# Last GeoJSON-data
print("Laster GeoJSON-data...")
with open('world-administrative-boundaries.geojson', 'r') as f:
    data = json.load(f)

# Liste for å lagre landinformasjon
countries_data = []

print("Genererer bilder for alle land med maksimal detaljeringsgrad...")
for feature in data['features']:
    country_name = feature['properties']['name']
    iso3 = feature['properties'].get('iso3', '')
    continent = feature['properties'].get('continent', '')
    region = feature['properties'].get('region', '')
    
    # Hopp over land uten navn
    if not country_name:
        continue
    
    # Sjekk om landet er anerkjent
    normalized_name = ALTERNATIVE_NAMES.get(country_name, country_name)
    if normalized_name not in RECOGNIZED_COUNTRIES:
        print(f"Hopper over ikke-anerkjent land: {country_name}")
        continue
    
    try:
        # Lag geometri
        country_shape = shape(feature['geometry'])
        
        # Lag filnavn basert på normalisert navn (samme som i JSON)
        safe_name = re.sub(r'[^\w\s-]', '', normalized_name).strip()
        safe_name = re.sub(r'[-\s]+', '_', safe_name)
        filename = f"{safe_name.lower()}.png"
        filepath = os.path.join('country_images', filename)
        
        # Tegn landet med maksimal detaljeringsgrad og kvadratisk format
        fig, ax = plt.subplots(figsize=(12,12))
        
        if country_shape.geom_type == "MultiPolygon":
            for geom in country_shape.geoms:
                # Bruk alle punktene i geometrien
                xs, ys = geom.exterior.xy
                ax.fill(xs, ys, color="black")
                
                # Tegn også eventuelle hull (interior rings)
                for interior in geom.interiors:
                    xs, ys = interior.xy
                    ax.fill(xs, ys, color="white")
        else:
            # Bruk alle punktene i geometrien
            xs, ys = country_shape.exterior.xy
            ax.fill(xs, ys, color="black")
            
            # Tegn også eventuelle hull (interior rings)
            for interior in country_shape.interiors:
                xs, ys = interior.xy
                ax.fill(xs, ys, color="white")

        ax.axis("off")  # Fjern akser og labels
        plt.tight_layout()
        plt.savefig(filepath, dpi=600, bbox_inches='tight')
        plt.close()  # Lukk figuren for å spare minne
        
        # Lagre landinformasjon med normalisert navn
        countries_data.append({
            'name': normalized_name,  # Bruk normalisert navn
            'original_name': country_name,  # Behold originalt navn
            'iso3': iso3,
            'continent': continent,
            'region': region,
            'image_file': filename,
            'geometry': feature['geometry']
        })
        
        print(f"✓ Generert: {normalized_name} -> {filename}")
        
    except Exception as e:
        print(f"✗ Feil ved generering av {normalized_name}: {e}")
        continue

# Lagre landinformasjon til JSON-fil
with open('countries_data.json', 'w', encoding='utf-8') as f:
    json.dump(countries_data, f, ensure_ascii=False, indent=2)

print(f"\nFerdig! Generert {len(countries_data)} landbilder med maksimal detaljeringsgrad.")
print(f"Bilder lagret i: country_images/")
print(f"Landinformasjon lagret i: countries_data.json")

# Vis noen eksempler
print("\nEksempler på genererte land:")
for i, country in enumerate(countries_data[:5]):
    print(f"  {i+1}. {country['name']} ({country['iso3']}) -> {country['image_file']}")
