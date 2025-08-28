#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path
import time

def convert_svg_batch(svg_dir, output_dir, size=128, batch_size=10):
    """Konverterer SVG-filer til PNG i små batcher for å unngå timeout"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    svg_files = list(Path(svg_dir).glob("*.svg"))
    total_files = len(svg_files)
    
    print(f"🚀 Starter konvertering av {total_files} SVG-filer...")
    print(f"📁 Input: {svg_dir}")
    print(f"📁 Output: {output_dir}")
    print(f"📏 Størrelse: {size}x{size}px")
    print(f"📦 Batch-størrelse: {batch_size}")
    print("-" * 50)
    
    successful = 0
    failed = 0
    
    for i in range(0, total_files, batch_size):
        batch = svg_files[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_files + batch_size - 1) // batch_size
        
        print(f"\n📦 Batch {batch_num}/{total_batches} ({len(batch)} filer)")
        
        for svg_file in batch:
            png_file = Path(output_dir) / f"{svg_file.stem}.png"
            
            # Hopp over hvis filen allerede eksisterer
            if png_file.exists():
                print(f"⏭️  {svg_file.name} (allerede eksisterer)")
                successful += 1
                continue
            
            try:
                # Bruk svgexport med timeout
                cmd = [
                    'svgexport',
                    str(svg_file),
                    str(png_file),
                    f'pad {size}:'
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
                    print(f"✅ {svg_file.name} -> {file_size} bytes")
                    successful += 1
                else:
                    print(f"❌ {svg_file.name} - Return code: {result.returncode}")
                    if result.stderr:
                        print(f"   Feil: {result.stderr.strip()}")
                    failed += 1
                    
            except subprocess.TimeoutExpired:
                print(f"⏰ {svg_file.name} - Timeout (30s)")
                failed += 1
            except Exception as e:
                print(f"💥 {svg_file.name} - Feil: {e}")
                failed += 1
        
        # Pause mellom batcher for å unngå overbelastning
        if i + batch_size < total_files:
            print("⏸️  Pause 2 sekunder...")
            time.sleep(2)
    
    print("\n" + "=" * 50)
    print(f"🎉 Konvertering fullført!")
    print(f"✅ Vellykket: {successful}")
    print(f"❌ Feilet: {failed}")
    print(f"📊 Total: {total_files}")
    
    if successful > 0:
        print(f"\n📁 PNG-filer lagret i: {output_dir}")
        print(f"📏 Størrelse: {size}x{size}px")
    
    return successful, failed

if __name__ == "__main__":
    svg_dir = "temp_flags/svg"
    output_dir = "flags_new"
    
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
    
    # Start konvertering
    convert_svg_batch(svg_dir, output_dir, size=128, batch_size=5)
