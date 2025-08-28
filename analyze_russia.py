import json
import matplotlib.pyplot as plt
from shapely.geometry import shape
import numpy as np

# Load GeoJSON data
with open('world-administrative-boundaries.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Find Russia
russia = None
for feature in geojson_data['features']:
    if feature['properties']['name'] == 'Russian Federation':
        russia = feature
        break

if russia:
    print("=== RUSSLAND ANALYSE ===")
    print(f"Land: {russia['properties']['name']}")
    print(f"ISO3: {russia['properties']['iso3']}")
    
    # Get geometry
    geometry = shape(russia['geometry'])
    
    # Get bounding box
    minx, miny, maxx, maxy = geometry.bounds
    print(f"\nBounding box:")
    print(f"Min lat: {miny:.6f}, Max lat: {maxy:.6f}")
    print(f"Min lon: {minx:.6f}, Max lon: {maxx:.6f}")
    
    # Calculate aspect ratio
    width = maxx - minx
    height = maxy - miny
    aspect_ratio = width / height
    print(f"\nAspect ratio (width/height): {aspect_ratio:.3f}")
    
    # Show what Russia should look like
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Plot 1: Original aspect ratio (how it should look)
    ax1.set_title('Russland - Riktig proporsjon')
    ax1.set_aspect('equal')
    
    if geometry.geom_type == 'MultiPolygon':
        for geom in geometry.geoms:
            xs, ys = geom.exterior.xy
            ax1.fill(xs, ys, color='black')
    else:
        xs, ys = geometry.exterior.xy
        ax1.fill(xs, ys, color='black')
    
    ax1.set_xlim(minx, maxx)
    ax1.set_ylim(miny, maxy)
    ax1.axis('off')
    
    # Plot 2: Square format (current approach)
    ax2.set_title('Russland - Kvadratisk format (strekt)')
    ax2.set_aspect('equal')
    
    if geometry.geom_type == 'MultiPolygon':
        for geom in geometry.geoms:
            xs, ys = geom.exterior.xy
            ax2.fill(xs, ys, color='red')
    else:
        xs, ys = geometry.exterior.xy
        ax2.fill(xs, ys, color='red')
    
    # Force square aspect ratio
    center_x = (minx + maxx) / 2
    center_y = (miny + maxy) / 2
    max_dim = max(width, height)
    half_dim = max_dim / 2
    
    ax2.set_xlim(center_x - half_dim, center_x + half_dim)
    ax2.set_ylim(center_y - half_dim, center_y + half_dim)
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig('russia_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\nBilde lagret som: russia_analysis.png")
    print(f"\nKonklusjon:")
    print(f"- Russland har aspect ratio: {aspect_ratio:.3f}")
    print(f"- Dette betyr at landet er {aspect_ratio:.1f}x bredere enn høyt")
    print(f"- Når vi tvinger kvadratisk format, blir det strekt i y-retning")
    print(f"- Russland er det største landet i verden og strekker seg over 11 tidssoner")
    print(f"- Løsning: Bruk original aspect ratio eller juster bounding box")
    
    # Check if Russia is in our current data
    try:
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            countries_data = json.load(f)
        
        russia_entry = None
        for entry in countries_data:
            if entry.get('name') == 'Russian Federation' or entry.get('iso3') == 'RUS':
                russia_entry = entry
                break
        
        if russia_entry:
            print(f"\nRussland i countries_data.json:")
            print(f"  Bilde: {russia_entry.get('imageFile', 'Ikke funnet')}")
            print(f"  Center: {russia_entry.get('center', 'Ikke funnet')}")
        else:
            print(f"\nRussland ikke funnet i countries_data.json")
            
    except FileNotFoundError:
        print(f"\ncountries_data.json ikke funnet")
    
else:
    print("Russland ikke funnet i GeoJSON-dataene")
