# 🌍 Korskavireis - Geografisk Gjettespill

Et interaktivt geografisk gjettespill hvor spillere skal gjette land basert på omriss.

## 🎮 Funksjoner

- **195 land** med høydetaljerte omriss
- **Prediktiv tekst** med autocomplete
- **Avstandsberegning** mellom gjettet og riktig land
- **Himmelretninger** som hint
- **Flagg som hint** for hvert land
- **Befolkningsdata** som hint
- **Responsivt design** som fungerer på alle enheter

## 🚀 Kom i gang

1. **Last ned prosjektet**
   ```bash
   git clone https://github.com/dittbrukernavn/korskavireis.git
   cd korskavireis
   ```

2. **Start lokal server**
   ```bash
   python -m http.server 8000
   ```

3. **Åpne i nettleser**
   ```
   http://localhost:8000
   ```

## 🛠️ Teknologier

- **HTML5** - Struktur
- **CSS3** - Styling og responsivt design
- **JavaScript (ES6+)** - Spilllogikk og interaktivitet
- **Matplotlib** - Generering av landomriss
- **GeoJSON** - Geografiske data
- **World Bank Data** - Befolkningsdata

## 📊 Datakilder

- **Landomriss**: Natural Earth Data
- **Flagg**: GitHub/cristiroma/countries
- **Befolkningsdata**: World Bank via GitHub/datasets/population

## 🎯 Hvordan spille

1. Se på landomrisset som vises
2. Skriv inn landnavnet (med autocomplete)
3. Få tilbakemelding på avstand og retning
4. Bruk hint (flagg/befolkning) hvis nødvendig
5. Du har 10 forsøk på å gjette riktig land

## 📝 Lisens

Dette prosjektet er lisensiert under MIT License.

## 👨‍💻 Utvikler

Bygget med ❤️ av Marius Arnesen
