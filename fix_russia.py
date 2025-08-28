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

def clean_filename(name):
    """Clean country name for filename"""
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
    
    print(f"Genererer {country_name}:")
    print(f"  Aspect ratio: {aspect_ratio:.3f}")
    print(f"  Bredde: {width:.2f} grader")
    print(f"  Høyde: {height:.2f} grader")
    
    # Determine figure size based on aspect ratio
    # For very wide countries (like Russia), use smaller height
    if aspect_ratio > 3:  # Very wide (like Russia, Chile)
        fig_width = 8
        fig_height = 8 / aspect_ratio
        print(f"  Figur størrelse: {fig_width:.1f} x {fig_height:.1f} tommer")
    elif aspect_ratio < 0.33:  # Very tall
        fig_width = 8 * aspect_ratio
        fig_height = 8
        print(f"  Figur størrelse: {fig_width:.1f} x {fig_height:.1f} tommer")
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
        print(f"  Figur størrelse: {fig_width:.1f} x {fig_height:.1f} tommer")
    
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

# Find and regenerate Russia
russia_feature = None
for feature in geojson_data['features']:
    if feature['properties']['name'] == 'Russian Federation':
        russia_feature = feature
        break

if russia_feature:
    print("=== REGENERERER RUSSLAND ===")
    filename = generate_country_image(russia_feature)
    print(f"✓ Russland regenerert: {filename}")
    
    # Update countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    # Find Russia entry and update
    for entry in countries_data:
        if entry.get('name') == 'Russia' or entry.get('original_name') == 'Russian Federation':
            entry['imageFile'] = filename
            print(f"✓ Oppdatert countries_data.json for Russland")
            break
    
    # Save updated data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ countries_data.json oppdatert")
    
else:
    print("Russland ikke funnet i GeoJSON-dataene")
