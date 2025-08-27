import json
import matplotlib.pyplot as plt
from shapely.geometry import shape

# Last GeoJSON-data
with open('world-administrative-boundaries.geojson', 'r') as f:
    data = json.load(f)

# Finn Norge
norge_shape = None
for feature in data['features']:
    if feature['properties']['name'] == 'Norway':
        norge_shape = shape(feature['geometry'])
        break

if norge_shape:
    # Tegn opp Norges geometri som svart silhuett
    fig, ax = plt.subplots(figsize=(6,8))
    
    if norge_shape.geom_type == "MultiPolygon":
        for geom in norge_shape.geoms:
            xs, ys = geom.exterior.xy
            ax.fill(xs, ys, color="black")
    else:
        xs, ys = norge_shape.exterior.xy
        ax.fill(xs, ys, color="black")

    ax.axis("off")  # Fjern akser og labels
    plt.tight_layout()
    plt.savefig('norge_outline.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Norge tegnet og lagret som 'norge_outline.png'")
else:
    print("Fant ikke Norge i datasettet")
