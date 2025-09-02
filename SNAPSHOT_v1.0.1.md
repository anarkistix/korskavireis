# 📸 SNAPSHOT v1.0.1
**Dato:** 2. september 2025  
**Commit:** 620d91e  
**Tag:** v1.0.1  

## 🎯 Status
Kompakt UI med forbedret mobilopplevelse. Hint vises nå konsekvent i samme område som hintknappene.

---

## 🌟 Hovedendringer i denne versjonen

- Hint-innhold åpnes i samme horisontale scroll-rad som hintknapper
- Når et hint åpnes erstatter hint-kortet sin knapp (mer kompakt UI)
- Mobilfikser: fjernet unødvendig glippe, hindret kutt i bunnen av hint-raden
- Fjernet overskriften over kartet for å spare vertikal plass
- La til Cursor-regler: mobil-først fokus og versjonering i footer

---

## 📁 Berørte filer

- `js/main.js`: Plassering av hint-innhold, erstatt knapp ved åpning, revealAllHints-oppførsel
- `css/style.v2.css`: Hint-rad høyder/padding/overflow, mobilmarginer, auto-høyde
- `index.html`: Fjernet `<h2>`-tittel over kart/landvisning
- `.cursor/rules/mobile-first.mdc`: Ny regel for mobil-først
- `.cursor/rules/versioning-footer.mdc`: Ny regel for versjonsoppdatering i footer
- `version.json`: Bump til 1.0.1, oppdatert build/tag/description

---

## 🚀 Kjøring lokalt

```bash
python3 -m http.server 8000
open http://127.0.0.1:8000
```

---

## 📝 Notater

- Footer henter versjon via `loadVersionInfo()` fra `version.json`
- Test spesielt hint-området på små skjermer: horisontal scroll, ingen vertikal glippe, ingen kutt i bunn

---

## 📦 Oppsummering

v1.0.1 leverer en mer kompakt og mobilvennlig opplevelse, med konsistent hintplassering og ryddigere layout.


