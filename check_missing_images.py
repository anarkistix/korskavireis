#!/usr/bin/env python3
"""
Check which countries are missing images
"""

import json
import os
from pathlib import Path

def check_missing_images():
    """Check which countries are missing images"""
    print("🔍 Checking for missing images...")
    
    # Load country data
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    # Get list of available images
    country_images_dir = Path('country_images')
    available_images = set([f.stem for f in country_images_dir.glob('*.png')])
    
    print(f"📁 Available images: {len(available_images)}")
    print(f"📊 Countries with imageFile: {len([c for c in countries_data if 'imageFile' in c])}")
    
    # Check for missing images
    missing_count = 0
    for country in countries_data:
        if 'imageFile' in country:
            image_file = country['imageFile']
            image_name = Path(image_file).stem  # Remove .png extension
            
            if image_name not in available_images:
                print(f"❌ Missing image for {country['name']}: {image_file}")
                missing_count += 1
    
    print(f"\n📊 Missing images: {missing_count}")

if __name__ == '__main__':
    check_missing_images()
