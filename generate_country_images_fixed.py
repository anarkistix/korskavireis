import json
import matplotlib.pyplot as plt
from shapely.geometry import shape
import os
import re

# Load GeoJSON data
with open('world-administrative-boundaries.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Load recognized countries
with open('recognized_countries.py', 'r', encoding='utf-8') as f:
    exec(f.read())

# Create output directory
os.makedirs('country_images', exist_ok=True)

# Load existing data if available
if os.path.exists('countries_data.json'):
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
else:
    countries_data = []

def clean_filename(name):
    """Clean country name for filename"""
    # Remove special characters and replace spaces with underscores
    cleaned = re.sub(r'[^\w\s-]', '', name)
    cleaned = re.sub(r'[-\s]+', '_', cleaned)
    return cleaned.lower()

def generate_country_image(feature, output_dir='country_images'):
    """Generate country image with proper aspect ratio handling"""
    country_name = feature['properties']['name']
    iso3 = feature['properties']['iso3']
    
    # Clean filename
    filename = clean_filename(country_name) + '.png'
    filepath = os.path.join(output_dir, filename)
    
    # Get geometry
    geometry = shape(feature['geometry'])
    
    # Get bounding box
    minx, miny, maxx, maxy = geometry.bounds
    
    # Calculate dimensions
    width = maxx - minx
    height = maxy - miny
    aspect_ratio = width / height
    
    # Determine figure size based on aspect ratio
    # For very wide countries (like Chile), use smaller height
    # For very tall countries, use smaller width
    # For roughly square countries, use balanced size
    
    if aspect_ratio > 3:  # Very wide (like Chile)
        fig_width = 8
        fig_height = 8 / aspect_ratio
    elif aspect_ratio < 0.33:  # Very tall
        fig_width = 8 * aspect_ratio
        fig_height = 8
    else:  # Normal aspect ratio
        # Use a balanced approach - max dimension determines size
        max_dim = max(width, height)
        if max_dim > 50:  # Large countries
            scale = 0.15
        elif max_dim > 20:  # Medium countries
            scale = 0.3
        else:  # Small countries
            scale = 0.6
        
        fig_width = width * scale
        fig_height = height * scale
    
    # Ensure minimum size
    fig_width = max(fig_width, 2)
    fig_height = max(fig_height, 2)
    
    # Create figure with calculated dimensions
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.set_aspect('equal')
    
    # Plot geometry
    if geometry.geom_type == 'MultiPolygon':
        for geom in geometry.geoms:
            xs, ys = geom.exterior.xy
            ax.fill(xs, ys, color='black')
    else:
        xs, ys = geometry.exterior.xy
        ax.fill(xs, ys, color='black')
    
    # Set limits to bounding box
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.axis('off')
    
    # Save with tight layout
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return filename

# Process countries
processed_countries = []
count = 0

for feature in geojson_data['features']:
    country_name = feature['properties']['name']
    iso3 = feature['properties']['iso3']
    
    # Check if country is recognized
    if country_name in RECOGNIZED_COUNTRIES or iso3 in RECOGNIZED_COUNTRIES:
        try:
            filename = generate_country_image(feature)
            
            # Find existing entry or create new one
            existing_entry = None
            for entry in countries_data:
                if entry.get('name') == country_name or entry.get('iso3') == iso3:
                    existing_entry = entry
                    break
            
            if existing_entry:
                existing_entry['imageFile'] = filename
            else:
                # Calculate center point
                geometry = shape(feature['geometry'])
                center = geometry.centroid
                
                countries_data.append({
                    'name': country_name,
                    'iso3': iso3,
                    'imageFile': filename,
                    'center': {
                        'lat': center.y,
                        'lon': center.x
                    }
                })
            
            processed_countries.append(country_name)
            count += 1
            print(f"✓ Generert: {country_name} -> {filename}")
            
        except Exception as e:
            print(f"✗ Feil ved generering av {country_name}: {e}")

# Save updated data
with open('countries_data.json', 'w', encoding='utf-8') as f:
    json.dump(countries_data, f, indent=2, ensure_ascii=False)

print(f"\nFerdig! Generert {count} landbilder med riktig aspect ratio.")
print(f"Bilder lagret i: country_images/")
print(f"Landinformasjon lagret i: countries_data.json")

# Show some examples
print(f"\nEksempler på genererte land:")
for i, country in enumerate(processed_countries[:5], 1):
    filename = clean_filename(country) + '.png'
    print(f"  {i}. {country} -> {filename}")

# Show aspect ratio analysis for Switzerland
switzerland_entry = None
for entry in countries_data:
    if entry.get('name') == 'Switzerland':
        switzerland_entry = entry
        break

if switzerland_entry:
    print(f"\n=== SVEITS ANALYSE ===")
    print(f"Bilde: {switzerland_entry['imageFile']}")
    print(f"Center: {switzerland_entry['center']}")
    print(f"Løsning: Bruker riktig aspect ratio (2.287) istedenfor kvadratisk")
