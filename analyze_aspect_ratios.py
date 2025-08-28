import json
import matplotlib.pyplot as plt
from shapely.geometry import shape
import pandas as pd

# Load GeoJSON data
with open('world-administrative-boundaries.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Load recognized countries
with open('recognized_countries.py', 'r', encoding='utf-8') as f:
    exec(f.read())

# Analyze aspect ratios
aspect_data = []

for feature in geojson_data['features']:
    country_name = feature['properties']['name']
    iso3 = feature['properties']['iso3']
    
    # Check if country is recognized
    if country_name in RECOGNIZED_COUNTRIES or iso3 in RECOGNIZED_COUNTRIES:
        try:
            geometry = shape(feature['geometry'])
            minx, miny, maxx, maxy = geometry.bounds
            
            width = maxx - minx
            height = maxy - miny
            aspect_ratio = width / height
            
            aspect_data.append({
                'name': country_name,
                'iso3': iso3,
                'aspect_ratio': aspect_ratio,
                'width': width,
                'height': height,
                'category': 'wide' if aspect_ratio > 2 else 'tall' if aspect_ratio < 0.5 else 'normal'
            })
        except Exception as e:
            print(f"Feil ved analyse av {country_name}: {e}")

# Convert to DataFrame for easier analysis
df = pd.DataFrame(aspect_data)

# Sort by aspect ratio
df_sorted = df.sort_values('aspect_ratio', ascending=False)

print("=== ASPECT RATIO ANALYSE ===")
print(f"Totalt antall land analysert: {len(df)}")
print()

# Show extreme cases
print("🏔️ LAND MED EKSTREMT BRED ASPECT RATIO (>2):")
print("(Disse blir strekt i y-retning med kvadratisk format)")
print()
for _, row in df_sorted[df_sorted['aspect_ratio'] > 2].head(10).iterrows():
    print(f"  {row['name']}: {row['aspect_ratio']:.2f} (bredere enn høyt)")
print()

print("📏 LAND MED EKSTREMT HØY ASPECT RATIO (<0.5):")
print("(Disse blir strekt i x-retning med kvadratisk format)")
print()
for _, row in df_sorted[df_sorted['aspect_ratio'] < 0.5].head(10).iterrows():
    print(f"  {row['name']}: {row['aspect_ratio']:.2f} (høyere enn bredt)")
print()

print("📊 STATISTIKK:")
print(f"  Land med aspect ratio > 2: {len(df[df['aspect_ratio'] > 2])}")
print(f"  Land med aspect ratio < 0.5: {len(df[df['aspect_ratio'] < 0.5])}")
print(f"  Land med normal aspect ratio: {len(df[(df['aspect_ratio'] >= 0.5) & (df['aspect_ratio'] <= 2)])}")
print()

# Show top 20 most problematic countries
print("🔥 TOP 20 LAND MED MEST PROBLEMATISK ASPECT RATIO:")
print()
for i, (_, row) in enumerate(df_sorted.head(20).iterrows(), 1):
    ratio = row['aspect_ratio']
    if ratio > 2:
        problem = f"Bred (strekt i y-retning)"
    elif ratio < 0.5:
        problem = f"Høy (strekt i x-retning)"
    else:
        problem = "Normal"
    
    print(f"  {i:2d}. {row['name']:<25} {ratio:6.2f} - {problem}")
print()

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Histogram of aspect ratios
ax1.hist(df['aspect_ratio'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
ax1.axvline(x=2, color='red', linestyle='--', label='Bred land (>2)')
ax1.axvline(x=0.5, color='orange', linestyle='--', label='Høye land (<0.5)')
ax1.set_xlabel('Aspect Ratio (bredde/høyde)')
ax1.set_ylabel('Antall land')
ax1.set_title('Fordeling av Aspect Ratios')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Top 10 most extreme cases
top_10 = df_sorted.head(10)
colors = ['red' if ratio > 2 else 'orange' if ratio < 0.5 else 'blue' for ratio in top_10['aspect_ratio']]

bars = ax2.barh(range(len(top_10)), top_10['aspect_ratio'], color=colors, alpha=0.7)
ax2.set_yticks(range(len(top_10)))
ax2.set_yticklabels(top_10['name'])
ax2.set_xlabel('Aspect Ratio')
ax2.set_title('Top 10 Land med Ekstrem Aspect Ratio')
ax2.grid(True, alpha=0.3)

# Add value labels on bars
for i, (bar, ratio) in enumerate(zip(bars, top_10['aspect_ratio'])):
    ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
             f'{ratio:.2f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('aspect_ratio_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"📈 Bilde lagret som: aspect_ratio_analysis.png")
print()
print("💡 KONKLUSJON:")
print("Mange land har ekstreme aspect ratios som gjør at de blir strekt")
print("når vi tvinger kvadratisk format. Den nye løsningen med")
print("tilpasset aspect ratio vil fikse dette for alle land.")
