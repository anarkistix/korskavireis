#!/bin/bash

# Deploy-script for KorSkaViReis
# Automatisk versjonering og deploy til GitHub Pages

echo "🚀 Starter deploy av KorSkaViReis..."

# Oppdater versjonsinformasjon
echo "📝 Oppdaterer versjonsinformasjon..."
python update_version.py

# Legg til alle endringer
echo "📦 Legger til endringer..."
git add .

# Commit med timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo "💾 Committer endringer..."
git commit -m "Deploy: $TIMESTAMP - Automatisk versjonering"

# Push til GitHub
echo "🌐 Pusher til GitHub..."
git push origin main

# Push tags hvis det finnes nye
echo "🏷️ Pusher tags..."
git push --tags

echo "✅ Deploy fullført!"
echo "🌍 Nettsiden vil være tilgjengelig på: https://anarkistix.github.io/korskavireis/"
echo "📊 Versjon: $(cat version.json | grep -o '"tag": "[^"]*"' | cut -d'"' -f4)"
