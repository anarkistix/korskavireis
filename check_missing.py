import json

# Last GeoJSON-data
with open('world-administrative-boundaries.geojson', 'r') as f:
    data = json.load(f)

# Sjekk manglende land
missing = ['Antigua and Barbuda', 'Brunei', 'Libya', 'Russia', 'Syria']
found = []

for feature in data['features']:
    name = feature['properties']['name']
    for missing_country in missing:
        if missing_country.lower() in name.lower():
            found.append((missing_country, name))

print("Fant alternativt navn for manglende land:")
for original, found_name in found:
    print(f"  {original} -> {found_name}")

# Sjekk også for "Russian Federation"
for feature in data['features']:
    name = feature['properties']['name']
    if 'russian' in name.lower():
        print(f"  Russia -> {name}")
