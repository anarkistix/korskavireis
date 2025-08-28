#!/usr/bin/env python3
"""
Check all imageFile values against available images
"""

import json
import os
from pathlib import Path

def check_all_imagefiles():
    """Check all imageFile values"""
    print("🔍 Checking all imageFile values...")
    
    # Load country data
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    # Get list of available images
    country_images_dir = Path('country_images')
    available_images = set([f.name for f in country_images_dir.glob('*.png')])
    
    print(f"📁 Available images: {len(available_images)}")
    
    # Check each country
    missing_count = 0
    for country in countries_data:
        if 'imageFile' in country:
            image_file = country['imageFile']
            if image_file not in available_images:
                print(f"❌ Missing image for {country['name']}: {image_file}")
                missing_count += 1
    
    print(f"\n📊 Missing images: {missing_count}")

if __name__ == '__main__':
    check_all_imagefiles()
