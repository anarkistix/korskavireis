#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def convert_svg_to_png(svg_dir, output_dir, size=128):
    """Konverterer SVG-filer til PNG med spesifisert størrelse"""
    
    # Opprett output-mappe hvis den ikke eksisterer
    os.makedirs(output_dir, exist_ok=True)
    
    # Sjekk om svgexport er tilgjengelig
    try:
        subprocess.run(['svgexport', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ svgexport er ikke installert. Prøver å installere...")
        try:
            subprocess.run(['npm', 'install', '-g', 'svgexport'], check=True)
            print("✅ svgexport installert!")
        except subprocess.CalledProcessError:
            print("❌ Kunne ikke installere svgexport. Prøver alternativ metode...")
            return convert_with_rsvg(svg_dir, output_dir, size)
    
    print(f"🔄 Konverterer SVG-filer til PNG ({size}x{size})...")
    
    svg_files = list(Path(svg_dir).glob("*.svg"))
    total_files = len(svg_files)
    
    for i, svg_file in enumerate(svg_files, 1):
        png_file = Path(output_dir) / f"{svg_file.stem}.png"
        
        print(f"📁 [{i}/{total_files}] Konverterer {svg_file.name}...")
        
        try:
            # Bruk svgexport med padding for å få kvadratisk output
            cmd = [
                'svgexport',
                str(svg_file),
                str(png_file),
                f'pad {size}:'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {svg_file.name} -> {png_file.name}")
            else:
                print(f"❌ Feil ved konvertering av {svg_file.name}: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Feil ved konvertering av {svg_file.name}: {e}")
    
    print(f"🎉 Konvertering fullført! {total_files} filer behandlet.")

def convert_with_rsvg(svg_dir, output_dir, size=128):
    """Alternativ metode med rsvg-convert hvis tilgjengelig"""
    try:
        subprocess.run(['rsvg-convert', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ rsvg-convert er ikke tilgjengelig. Prøver å installere...")
        try:
            subprocess.run(['brew', 'install', 'librsvg'], check=True)
            print("✅ librsvg installert!")
        except subprocess.CalledProcessError:
            print("❌ Kunne ikke installere librsvg. Prøver siste alternativ...")
            return convert_with_python_svg(svg_dir, output_dir, size)
    
    print(f"🔄 Konverterer SVG-filer til PNG med rsvg-convert ({size}x{size})...")
    
    svg_files = list(Path(svg_dir).glob("*.svg"))
    total_files = len(svg_files)
    
    for i, svg_file in enumerate(svg_files, 1):
        png_file = Path(output_dir) / f"{svg_file.stem}.png"
        
        print(f"📁 [{i}/{total_files}] Konverterer {svg_file.name}...")
        
        try:
            cmd = [
                'rsvg-convert',
                '-w', str(size),
                '-h', str(size),
                '-f', 'png',
                '-o', str(png_file),
                str(svg_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {svg_file.name} -> {png_file.name}")
            else:
                print(f"❌ Feil ved konvertering av {svg_file.name}: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Feil ved konvertering av {svg_file.name}: {e}")

def convert_with_python_svg(svg_dir, output_dir, size=128):
    """Python-basert konvertering med svglib hvis tilgjengelig"""
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
    except ImportError:
        print("❌ svglib er ikke installert. Prøver å installere...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'svglib'], check=True)
            from svglib.svglib import svg2rlg
            from reportlab.graphics import renderPM
            print("✅ svglib installert!")
        except Exception as e:
            print(f"❌ Kunne ikke installere svglib: {e}")
            print("💡 Prøv manuelt: pip install svglib")
            return
    
    print(f"🔄 Konverterer SVG-filer til PNG med svglib ({size}x{size})...")
    
    svg_files = list(Path(svg_dir).glob("*.svg"))
    total_files = len(svg_files)
    
    for i, svg_file in enumerate(svg_files, 1):
        png_file = Path(output_dir) / f"{svg_file.stem}.png"
        
        print(f"📁 [{i}/{total_files}] Konverterer {svg_file.name}...")
        
        try:
            # Konverter SVG til ReportLab drawing
            drawing = svg2rlg(str(svg_file))
            
            if drawing:
                # Skaler til ønsket størrelse
                drawing.width = size
                drawing.height = size
                drawing.scale(size / max(drawing.width, drawing.height), 
                            size / max(drawing.width, drawing.height))
                
                # Render til PNG
                renderPM.drawToFile(drawing, str(png_file), fmt="PNG")
                print(f"✅ {svg_file.name} -> {png_file.name}")
            else:
                print(f"❌ Kunne ikke laste {svg_file.name}")
                
        except Exception as e:
            print(f"❌ Feil ved konvertering av {svg_file.name}: {e}")

if __name__ == "__main__":
    svg_dir = "temp_flags/svg"
    output_dir = "flags_new"
    
    if not os.path.exists(svg_dir):
        print(f"❌ SVG-mappe ikke funnet: {svg_dir}")
        sys.exit(1)
    
    print("🚀 Starter konvertering av SVG til PNG...")
    convert_svg_to_png(svg_dir, output_dir, size=128)
    
    print(f"\n📊 Resultat:")
    if os.path.exists(output_dir):
        png_count = len(list(Path(output_dir).glob("*.png")))
        print(f"✅ {png_count} PNG-filer generert i {output_dir}/")
    else:
        print("❌ Ingen PNG-filer ble generert")
