#!/usr/bin/env python3
"""
Enkel test for å vise GeoJSON-data fra Stefie/geojson-world
Bruker bare standardbibliotekene
"""

import json
import os

def analyze_geojson():
    """Analyserer GeoJSON-dataene og finner Norge"""
    
    print("🌍 Analyserer GeoJSON-data fra Stefie/geojson-world")
    print("=" * 50)
    
    try:
        # Sjekk om filen eksisterer
        if not os.path.exists('countries.geojson'):
            print("❌ countries.geojson ikke funnet")
            print("💡 Last ned fra: https://github.com/Stefie/geojson-world")
            return False
        
        # Last GeoJSON-data
        with open('countries.geojson', 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
        
        print(f"✅ Lastet {len(geojson_data['features'])} land")
        
        # Finn Norge basert på cca2-kode
        norway_found = False
        norway_data = None
        
        for feature in geojson_data['features']:
            properties = feature['properties']
            cca2 = properties.get('cca2', '').upper()
            
            # Sjekk om landet er Norge (NO)
            if cca2 == 'NO':
                norway_found = True
                norway_data = {
                    'cca2': cca2,
                    'properties': properties,
                    'geometry_type': feature['geometry']['type']
                }
                break
        
        print(f"🇳🇴 Norge funnet: {norway_found}")
        
        if norway_found:
            print(f"🇳🇴 Norge data:")
            print(f"  - ISO-kode: {norway_data['cca2']}")
            print(f"  - Geometri-type: {norway_data['geometry_type']}")
            print(f"  - Alle egenskaper: {list(norway_data['properties'].keys())}")
        else:
            print("❌ Norge ikke funnet i dataene")
            print("🔍 Sjekker alle tilgjengelige land...")
            
            # Vis alle tilgjengelige land
            all_countries = []
            for feature in geojson_data['features']:
                cca2 = feature['properties'].get('cca2', '').upper()
                if cca2:
                    all_countries.append(cca2)
            
            all_countries.sort()
            print(f"📋 Alle tilgjengelige land ({len(all_countries)}):")
            for i, country in enumerate(all_countries):
                if i % 10 == 0:
                    print(f"  {i+1:3d}-{min(i+10, len(all_countries)):3d}: ", end="")
                print(f"{country} ", end="")
                if (i + 1) % 10 == 0:
                    print()
            print()
        
        # Analyser alle land
        print(f"\n📊 Statistikk:")
        print(f"  - Totalt antall land: {len(geojson_data['features'])}")
        
        # Sjekk hvilke egenskaper som finnes
        all_properties = set()
        for feature in geojson_data['features']:
            all_properties.update(feature['properties'].keys())
        
        print(f"  - Unike egenskaper: {len(all_properties)}")
        print(f"  - Egenskaper: {sorted(list(all_properties))}")
        
        # Vis noen eksempler på landkoder
        print(f"\n📋 Eksempler på landkoder (første 20):")
        for i, feature in enumerate(geojson_data['features'][:20]):
            cca2 = feature['properties'].get('cca2', '').upper()
            print(f"  {i+1:2d}. {cca2}")
        
        # Sjekk geometri-typer
        geometry_types = {}
        for feature in geojson_data['features']:
            geom_type = feature['geometry']['type']
            geometry_types[geom_type] = geometry_types.get(geom_type, 0) + 1
        
        print(f"\n🗺️ Geometri-typer:")
        for geom_type, count in geometry_types.items():
            print(f"  - {geom_type}: {count} land")
        
        return True
        
    except Exception as e:
        print(f"❌ Feil ved analyse: {e}")
        return False

def create_simple_visualization():
    """Lager en enkel HTML-visualisering"""
    
    print(f"\n🌐 Lager enkel HTML-visualisering...")
    
    html_content = """
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verdenskart Test - GeoJSON Analyse</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .info-box {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #2196f3;
        }
        .success {
            background: #e8f5e8;
            border-left-color: #4caf50;
        }
        .warning {
            background: #fff3e0;
            border-left-color: #ff9800;
        }
        pre {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌍 Verdenskart Test - GeoJSON Analyse</h1>
        
        <div class="info-box success">
            <h3>✅ Test Resultat</h3>
            <p>Denne siden viser resultatet av analysen av GeoJSON-data fra <a href="https://github.com/Stefie/geojson-world" target="_blank">Stefie/geojson-world</a>.</p>
        </div>
        
        <div class="info-box">
            <h3>📋 Instruksjoner for å teste</h3>
            <p>For å teste det interaktive kartet:</p>
            <ol>
                <li>Åpne <code>test_world_map.html</code> i en nettleser</li>
                <li>Kartet vil vise alle land i grå farge</li>
                <li>Norge vil være markert i rød farge (hvis funnet)</li>
                <li>Hover over landene for å se dem lysere</li>
                <li>Klikk på land for å se navn i konsollen</li>
            </ol>
        </div>
        
        <div class="info-box warning">
            <h3>⚠️ Merk</h3>
            <p>Dette er en test for å verifisere at GeoJSON-dataene fungerer korrekt. 
            For å se det faktiske kartet, bruk <code>test_world_map.html</code> filen.</p>
        </div>
        
        <h3>🔗 Lenker</h3>
        <ul>
            <li><a href="test_world_map.html" target="_blank">Interaktivt verdenskart</a></li>
            <li><a href="https://github.com/Stefie/geojson-world" target="_blank">Stefie/geojson-world repository</a></li>
        </ul>
    </div>
</body>
</html>
"""
    
    with open('test_results.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML-fil lagret som: test_results.html")
    return True

if __name__ == "__main__":
    success = analyze_geojson()
    if success:
        create_simple_visualization()
        print(f"\n✅ Test fullført!")
        print(f"📁 Filer opprettet:")
        print(f"  - test_world_map.html (interaktivt kart)")
        print(f"  - test_results.html (resultat-side)")
        print(f"  - countries.geojson (GeoJSON-data)")
    else:
        print(f"\n❌ Test feilet")
