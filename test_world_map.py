#!/usr/bin/env python3
"""
Test-script for å vise verdenskart med Norge i rød farge
Bruker data fra Stefie/geojson-world
"""

import json
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import shape
import pandas as pd

def create_world_map():
    """Lager et verdenskart med Norge i rød farge"""
    
    print("🌍 Laster GeoJSON-data...")
    
    try:
        # Last GeoJSON-data
        with open('countries.geojson', 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
        
        print(f"✅ Lastet {len(geojson_data['features'])} land")
        
        # Konverter til GeoDataFrame
        features = []
        for feature in geojson_data['features']:
            # Hent landets egenskaper
            properties = feature['properties']
            geometry = shape(feature['geometry'])
            
            # Sjekk om landet er Norge
            country_name = properties.get('name') or properties.get('NAME') or properties.get('country', '')
            is_norway = (
                'norway' in country_name.lower() or
                'norge' in country_name.lower() or
                'nor' in country_name.lower() or
                properties.get('iso_a3') == 'NOR' or
                properties.get('iso3') == 'NOR'
            )
            
            features.append({
                'name': country_name,
                'geometry': geometry,
                'is_norway': is_norway,
                'iso_a3': properties.get('iso_a3'),
                'iso3': properties.get('iso3')
            })
        
        # Opprett GeoDataFrame
        gdf = gpd.GeoDataFrame(features)
        gdf.set_crs(epsg=4326, inplace=True)
        
        print(f"✅ Konvertert til GeoDataFrame med {len(gdf)} land")
        
        # Sjekk om Norge ble funnet
        norway_found = gdf['is_norway'].any()
        print(f"🇳🇴 Norge funnet: {norway_found}")
        
        if norway_found:
            norway_data = gdf[gdf['is_norway']]
            print(f"🇳🇴 Norge data: {norway_data['name'].iloc[0]}")
        
        # Opprett kart
        print("🎨 Lager kart...")
        
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))
        
        # Tegn alle land i grå
        gdf.plot(ax=ax, color='#cccccc', edgecolor='white', linewidth=0.3)
        
        # Tegn Norge i rød hvis funnet
        if norway_found:
            norway_gdf = gdf[gdf['is_norway']]
            norway_gdf.plot(ax=ax, color='#ff4444', edgecolor='white', linewidth=0.5)
            print("🔴 Norge tegnet i rød farge")
        
        # Kart-innstillinger
        ax.set_title('🌍 Verdenskart - Norge i Rød', fontsize=20, pad=20)
        ax.set_xlabel('Lengdegrad')
        ax.set_ylabel('Breddegrad')
        
        # Fjern akser
        ax.set_axis_off()
        
        # Legg til informasjon
        info_text = f"Totalt antall land: {len(gdf)}\nNorge funnet: {norway_found}"
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
                verticalalignment='top', fontsize=12,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Lagre kartet
        output_file = 'world_map_norway_red.png'
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"💾 Kart lagret som: {output_file}")
        
        # Vis kartet
        plt.show()
        
        # Vis noen eksempler på landnavn
        print("\n📋 Eksempler på landnavn:")
        for i, row in gdf.head(10).iterrows():
            print(f"  - {row['name']} (ISO: {row['iso_a3'] or row['iso3']})")
        
        return True
        
    except FileNotFoundError:
        print("❌ Feil: countries.geojson ikke funnet")
        print("💡 Last ned filen fra: https://github.com/Stefie/geojson-world")
        return False
        
    except Exception as e:
        print(f"❌ Feil ved opprettelse av kart: {e}")
        return False

def check_dependencies():
    """Sjekker om nødvendige biblioteker er installert"""
    try:
        import geopandas
        import matplotlib
        import shapely
        print("✅ Alle nødvendige biblioteker er installert")
        return True
    except ImportError as e:
        print(f"❌ Manglende bibliotek: {e}")
        print("💡 Installer med: pip install geopandas matplotlib shapely")
        return False

if __name__ == "__main__":
    print("🌍 Verdenskart Test - Norge i Rød")
    print("=" * 40)
    
    if check_dependencies():
        success = create_world_map()
        if success:
            print("\n✅ Test fullført!")
        else:
            print("\n❌ Test feilet")
    else:
        print("\n❌ Kan ikke kjøre test - manglende avhengigheter")
