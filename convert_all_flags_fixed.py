#!/usr/bin/env python3
import os
import subprocess
import sys
import json
import shutil
from pathlib import Path
import time

def convert_all_svg_to_png(svg_dir, output_dir, size=128):
    """Konverterer alle SVG-filer til PNG med eksakt samme størrelse"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    svg_files = list(Path(svg_dir).glob("*.svg"))
    total_files = len(svg_files)
    
    print(f"🚀 Starter konvertering av ALLE {total_files} SVG-filer...")
    print(f"📁 Input: {svg_dir}")
    print(f"📁 Output: {output_dir}")
    print(f"📏 Størrelse: {size}x{size}px (alle like store)")
    print("-" * 50)
    
    successful = 0
    failed = 0
    
    for i, svg_file in enumerate(svg_files, 1):
        png_file = Path(output_dir) / f"{svg_file.stem}.png"
        
        # Hopp over hvis filen allerede eksisterer
        if png_file.exists():
            print(f"⏭️  [{i}/{total_files}] {svg_file.name} (allerede eksisterer)")
            successful += 1
            continue
        
        print(f"🔄 [{i}/{total_files}] Konverterer {svg_file.name}...")
        
        try:
            # Bruk svgexport med 'fit' for å få eksakt samme størrelse
            cmd = [
                'svgexport',
                str(svg_file),
                str(png_file),
                f'{size}:{size}'  # Eksakt størrelse, ikke pad
            ]
            
            # Kjør med timeout på 30 sekunder
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0 and png_file.exists():
                file_size = png_file.stat().st_size
                print(f"✅ [{i}/{total_files}] {svg_file.name} -> {file_size} bytes")
                successful += 1
            else:
                print(f"❌ [{i}/{total_files}] {svg_file.name} - Return code: {result.returncode}")
                if result.stderr:
                    print(f"   Feil: {result.stderr.strip()}")
                failed += 1
                
        except subprocess.TimeoutExpired:
            print(f"⏰ [{i}/{total_files}] {svg_file.name} - Timeout (30s)")
            failed += 1
        except Exception as e:
            print(f"💥 [{i}/{total_files}] {svg_file.name} - Feil: {e}")
            failed += 1
        
        # Pause hver 10. fil for å unngå overbelastning
        if i % 10 == 0:
            print("⏸️  Pause 1 sekund...")
            time.sleep(1)
    
    print("\n" + "=" * 50)
    print(f"🎉 Konvertering fullført!")
    print(f"✅ Vellykket: {successful}")
    print(f"❌ Feilet: {failed}")
    print(f"📊 Total: {total_files}")
    
    return successful, failed

def backup_old_flags():
    """Lager backup av gamle flagg"""
    if os.path.exists('flags'):
        backup_dir = 'flags_backup_' + time.strftime('%Y%m%d_%H%M%S')
        print(f"💾 Lager backup av gamle flagg til {backup_dir}/")
        shutil.copytree('flags', backup_dir)
        return backup_dir
    return None

def replace_all_flags(new_flags_dir):
    """Erstatter alle gamle flagg med nye"""
    print(f"🔄 Erstatter alle flagg med nye fra {new_flags_dir}/")
    
    # Slett gamle flags-mappe
    if os.path.exists('flags'):
        shutil.rmtree('flags')
    
    # Kopier nye flagg
    shutil.copytree(new_flags_dir, 'flags')
    
    print(f"✅ Alle flagg erstattet!")

def update_all_flag_files():
    """Oppdaterer alle flagFile-feltene i countries_data.json"""
    
    # Les countries_data.json
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"🔄 Oppdaterer flagFile for alle {len(countries)} land...")
    
    updated_count = 0
    
    for country in countries:
        iso_code = country.get('iso_code')
        if iso_code:
            old_flag = country.get('flagFile', '')
            new_flag = f"{iso_code}.png"
            
            if old_flag != new_flag:
                country['flagFile'] = new_flag
                print(f"✅ {country['name']} ({iso_code}): {old_flag} -> {new_flag}")
                updated_count += 1
    
    # Lagre oppdatert data
    with open('countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Oppdatering fullført!")
    print(f"✅ {updated_count} land oppdatert")
    
    # Vis statistikk
    total_countries = len(countries)
    countries_with_flags = sum(1 for c in countries if c.get('flagFile'))
    
    print(f"\n📊 Statistikk:")
    print(f"🌍 Totalt antall land: {total_countries}")
    print(f"🏁 Land med flagg: {countries_with_flags}")
    print(f"📈 Dekning: {countries_with_flags/total_countries*100:.1f}%")

def verify_flag_sizes(output_dir):
    """Verifiserer at alle flagg har samme størrelse"""
    print(f"🔍 Verifiserer flagg-størrelser i {output_dir}/")
    
    png_files = list(Path(output_dir).glob("*.png"))
    if not png_files:
        print("❌ Ingen PNG-filer funnet")
        return
    
    # Sjekk første fil for referanse
    first_file = png_files[0]
    try:
        from PIL import Image
        with Image.open(first_file) as img:
            expected_size = img.size
            print(f"📏 Forventet størrelse: {expected_size}")
    except ImportError:
        print("⚠️  PIL ikke tilgjengelig, kan ikke verifisere størrelser")
        return
    except Exception as e:
        print(f"❌ Kunne ikke lese {first_file}: {e}")
        return
    
    # Sjekk alle filer
    correct_size = 0
    wrong_size = 0
    
    for png_file in png_files:
        try:
            with Image.open(png_file) as img:
                if img.size == expected_size:
                    correct_size += 1
                else:
                    wrong_size += 1
                    print(f"❌ {png_file.name}: {img.size} (forventet: {expected_size})")
        except Exception as e:
            wrong_size += 1
            print(f"❌ {png_file.name}: feil - {e}")
    
    print(f"\n📊 Størrelse-verifikasjon:")
    print(f"✅ Riktig størrelse: {correct_size}")
    print(f"❌ Feil størrelse: {wrong_size}")
    print(f"📈 Nøyaktighet: {correct_size/(correct_size+wrong_size)*100:.1f}%")

def main():
    """Hovedfunksjon som kjører hele prosessen"""
    
    svg_dir = "temp_flags/svg"
    output_dir = "flags_new_all_fixed"
    
    if not os.path.exists(svg_dir):
        print(f"❌ SVG-mappe ikke funnet: {svg_dir}")
        sys.exit(1)
    
    # Sjekk om svgexport er tilgjengelig
    try:
        subprocess.run(['svgexport', '--version'], capture_output=True, check=True)
        print("✅ svgexport er tilgjengelig")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ svgexport er ikke installert")
        print("💡 Installer med: npm install -g svgexport")
        sys.exit(1)
    
    print("🚀 STARTER KOMPLETT FLAGGOPPGRADERING (FIKSET STØRRELSE)")
    print("=" * 60)
    
    # Steg 1: Backup gamle flagg
    backup_dir = backup_old_flags()
    
    # Steg 2: Konverter alle SVG til PNG med eksakt samme størrelse
    successful, failed = convert_all_svg_to_png(svg_dir, output_dir, size=128)
    
    if successful == 0:
        print("❌ Ingen flagg ble konvertert. Avbryter.")
        sys.exit(1)
    
    # Steg 3: Verifiser størrelser
    verify_flag_sizes(output_dir)
    
    # Steg 4: Erstatt alle flagg
    replace_all_flags(output_dir)
    
    # Steg 5: Oppdater countries_data.json
    update_all_flag_files()
    
    print("\n" + "=" * 60)
    print("🎉 KOMPLETT FLAGGOPPGRADERING FULLFØRT!")
    print("=" * 60)
    print(f"✅ {successful} nye flagg konvertert (alle {128}x{128}px)")
    print(f"❌ {failed} feilet")
    print(f"💾 Backup lagret i: {backup_dir}")
    print(f"📁 Nye flagg i: flags/")
    print(f"📊 Alle land oppdatert i countries_data.json")
    
    if backup_dir:
        print(f"\n💡 Hvis du vil gå tilbake til gamle flagg:")
        print(f"   rm -rf flags && mv {backup_dir} flags")

if __name__ == "__main__":
    main()
