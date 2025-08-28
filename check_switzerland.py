import json
import matplotlib.pyplot as plt
from shapely.geometry import shape
import numpy as np

# Load GeoJSON data
with open('world-administrative-boundaries.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Find Switzerland
switzerland = None
for feature in geojson_data['features']:
    if feature['properties']['name'] == 'Switzerland':
        switzerland = feature
        break

if switzerland:
    print("=== SVEITS ANALYSE ===")
    print(f"Land: {switzerland['properties']['name']}")
    print(f"ISO3: {switzerland['properties']['iso3']}")
    
    # Get geometry
    geometry = shape(switzerland['geometry'])
    
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
    
    # Show what Switzerland should look like
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Plot 1: Original aspect ratio (how it should look)
    ax1.set_title('Sveits - Riktig proporsjon')
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
    ax2.set_title('Sveits - Kvadratisk format (strekt)')
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
    plt.savefig('switzerland_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\nBilde lagret som: switzerland_analysis.png")
    print(f"\nKonklusjon:")
    print(f"- Sveits har aspect ratio: {aspect_ratio:.3f}")
    print(f"- Dette betyr at landet er {aspect_ratio:.1f}x bredere enn høyt")
    print(f"- Når vi tvinger kvadratisk format, blir det strekt i y-retning")
    print(f"- Løsning: Bruk original aspect ratio eller juster bounding box")
    
else:
    print("Sveits ikke funnet i GeoJSON-dataene")
