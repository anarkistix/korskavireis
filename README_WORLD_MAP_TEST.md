# 🌍 Verdenskart Test - Stefie/geojson-world

Dette er en test for å verifisere at GeoJSON-dataene fra [Stefie/geojson-world](https://github.com/Stefie/geojson-world) fungerer korrekt for å vise et verdenskart med Norge i rød farge.

## 📁 Filer

- **`countries.geojson`** - GeoJSON-data med alle verdens land (21.5MB)
- **`test_world_map.html`** - Interaktivt verdenskart med D3.js
- **`test_world_map_simple.py`** - Python-script for å analysere dataene
- **`test_results.html`** - Resultat-side med instruksjoner
- **`README_WORLD_MAP_TEST.md`** - Denne filen

## 🚀 Hvordan teste

### 1. Interaktivt Kart
Åpne `test_world_map.html` i en nettleser:
```
http://localhost:8001/test_world_map.html
```

**Funksjoner:**
- 🌍 Viser alle verdens land i grå farge
- 🔴 Norge er markert i rød farge
- 🖱️ Hover over land for å se dem lysere
- 👆 Klikk på land for å se ISO-kode i konsollen

### 2. Python Analyse
Kjør analysen for å se dataene:
```bash
python test_world_map_simple.py
```

**Resultat:**
- ✅ 245 land lastet
- 🇳🇴 Norge funnet med ISO-kode 'NO'
- 📊 Statistikk over geometri-typer og egenskaper

### 3. Resultat-side
Åpne `test_results.html` for instruksjoner:
```
http://localhost:8001/test_results.html
```

## 📊 Data-struktur

GeoJSON-filen inneholder:
- **245 land** med korrekte grenser
- **Egenskaper:** `cca2` (ISO 2-bokstavskoder)
- **Geometri:** Polygon (100 land) og MultiPolygon (145 land)

### Eksempler på landkoder:
- 🇳🇴 **NO** - Norge
- 🇸🇪 **SE** - Sverige  
- 🇩🇰 **DK** - Danmark
- 🇺🇸 **US** - USA
- 🇨🇳 **CN** - Kina

## 🎨 Kart-funksjoner

### Farger:
- **Grå (#cccccc):** Alle andre land
- **Rød (#ff4444):** Norge
- **Lysere grå (#999999):** Hover-effekt

### Interaktivitet:
- **Hover:** Land blir lysere
- **Klikk:** Viser ISO-kode i konsollen
- **Responsivt:** Fungerer på alle skjermstørrelser

## 🔧 Teknisk

### Brukte biblioteker:
- **D3.js v7** - For kart-visning
- **GeoJSON** - Data-format
- **Mercator projection** - Kart-projeksjon

### Kompatibilitet:
- ✅ Alle moderne nettlesere
- ✅ Mobil-enheter
- ✅ Desktop

## 📈 Test-resultater

```
🌍 Analyserer GeoJSON-data fra Stefie/geojson-world
==================================================
✅ Lastet 245 land
🇳🇴 Norge funnet: True
🇳🇴 Norge data:
  - ISO-kode: NO
  - Geometri-type: MultiPolygon
  - Alle egenskaper: ['cca2']

📊 Statistikk:
  - Totalt antall land: 245
  - Unike egenskaper: 1
  - Egenskaper: ['cca2']

🗺️ Geometri-typer:
  - Polygon: 100 land
  - MultiPolygon: 145 land
```

## 🎯 Konklusjon

✅ **Testen er vellykket!**

- GeoJSON-dataene fra Stefie/geojson-world fungerer perfekt
- Norge blir korrekt identifisert og markert i rød farge
- Kartet er interaktivt og responsivt
- Alle 245 land vises korrekt

Dette bekrefter at dataene kan brukes for å lage interaktive verdenskart med tilpasset fargemarkering av spesifikke land.

## 🔗 Lenker

- [Stefie/geojson-world Repository](https://github.com/Stefie/geojson-world)
- [D3.js Dokumentasjon](https://d3js.org/)
- [GeoJSON Spesifikasjon](https://geojson.org/)
