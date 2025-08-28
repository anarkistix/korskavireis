#!/usr/bin/env python3
"""
Download all Mapsicon resolutions and map them to our country data
"""

import os
import json
import shutil
from pathlib import Path

def download_mapsicon_resolutions():
    """Download all Mapsicon resolutions"""
    print("🚀 Starting Mapsicon download...")
    
    # Create directories for all resolutions
    resolutions = ['16', '24', '32', '48', '64', '80', '96', '128', '256', '512', '1024']
    base_dir = Path('mapsicon_downloads')
    
    for res in resolutions:
        (base_dir / res).mkdir(exist_ok=True)
    
    # Also create SVG directory
    (base_dir / 'svg').mkdir(exist_ok=True)
    
    # Load our country data to get ISO codes
    with open('countries_data.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    print(f"📊 Found {len(countries_data)} countries in our data")
    
    # ISO code mapping (our names to ISO codes)
    iso_mapping = {
        'Afghanistan': 'af',
        'Albania': 'al',
        'Algeria': 'dz',
        'Andorra': 'ad',
        'Angola': 'ao',
        'Antigua & Barbuda': 'ag',
        'Antigua and Barbuda': 'ag',
        'Argentina': 'ar',
        'Armenia': 'am',
        'Australia': 'au',
        'Austria': 'at',
        'Azerbaijan': 'az',
        'Bahamas': 'bs',
        'Bahrain': 'bh',
        'Bangladesh': 'bd',
        'Barbados': 'bb',
        'Belarus': 'by',
        'Belgium': 'be',
        'Belize': 'bz',
        'Benin': 'bj',
        'Bhutan': 'bt',
        'Bolivia': 'bo',
        'Bosnia & Herzegovina': 'ba',
        'Bosnia and Herzegovina': 'ba',
        'Botswana': 'bw',
        'Brazil': 'br',
        'Brunei Darussalam': 'bn',
        'Brunei': 'bn',
        'Bulgaria': 'bg',
        'Burkina Faso': 'bf',
        'Burundi': 'bi',
        'Cambodia': 'kh',
        'Cameroon': 'cm',
        'Canada': 'ca',
        'Cape Verde': 'cv',
        'Central African Republic': 'cf',
        'Chad': 'td',
        'Chile': 'cl',
        'China': 'cn',
        'Colombia': 'co',
        'Comoros': 'km',
        'Congo': 'cg',
        'Costa Rica': 'cr',
        'Croatia': 'hr',
        'Cuba': 'cu',
        'Cyprus': 'cy',
        'Czech Republic': 'cz',
        'Democratic People\'s Republic of Korea': 'kp',
        'North Korea': 'kp',
        'Democratic Republic of the Congo': 'cd',
        'Denmark': 'dk',
        'Djibouti': 'dj',
        'Dominica': 'dm',
        'Dominican Republic': 'do',
        'Ecuador': 'ec',
        'Egypt': 'eg',
        'El Salvador': 'sv',
        'Equatorial Guinea': 'gq',
        'Eritrea': 'er',
        'Estonia': 'ee',
        'Ethiopia': 'et',
        'Fiji': 'fj',
        'Finland': 'fi',
        'France': 'fr',
        'Gabon': 'ga',
        'Gambia': 'gm',
        'Georgia': 'ge',
        'Germany': 'de',
        'Ghana': 'gh',
        'Greece': 'gr',
        'Grenada': 'gd',
        'Guatemala': 'gt',
        'Guinea': 'gn',
        'Guinea-Bissau': 'gw',
        'Guyana': 'gy',
        'Haiti': 'ht',
        'Honduras': 'hn',
        'Hungary': 'hu',
        'Iceland': 'is',
        'India': 'in',
        'Indonesia': 'id',
        'Iran (Islamic Republic of)': 'ir',
        'Iran': 'ir',
        'Iraq': 'iq',
        'Ireland': 'ie',
        'Israel': 'il',
        'Italy': 'it',
        'Jamaica': 'jm',
        'Japan': 'jp',
        'Jordan': 'jo',
        'Kazakhstan': 'kz',
        'Kenya': 'ke',
        'Kiribati': 'ki',
        'Kuwait': 'kw',
        'Kyrgyzstan': 'kg',
        'Lao People\'s Democratic Republic': 'la',
        'Laos': 'la',
        'Latvia': 'lv',
        'Lebanon': 'lb',
        'Lesotho': 'ls',
        'Liberia': 'lr',
        'Libya': 'ly',
        'Liechtenstein': 'li',
        'Lithuania': 'lt',
        'Luxembourg': 'lu',
        'Madagascar': 'mg',
        'Malawi': 'mw',
        'Malaysia': 'my',
        'Maldives': 'mv',
        'Mali': 'ml',
        'Malta': 'mt',
        'Marshall Islands': 'mh',
        'Mauritania': 'mr',
        'Mauritius': 'mu',
        'Mexico': 'mx',
        'Micronesia (Federated States of)': 'fm',
        'Micronesia': 'fm',
        'Moldova, Republic of': 'md',
        'Moldova': 'md',
        'Monaco': 'mc',
        'Mongolia': 'mn',
        'Montenegro': 'me',
        'Morocco': 'ma',
        'Mozambique': 'mz',
        'Myanmar': 'mm',
        'Namibia': 'na',
        'Nauru': 'nr',
        'Nepal': 'np',
        'Netherlands': 'nl',
        'New Zealand': 'nz',
        'Nicaragua': 'ni',
        'Niger': 'ne',
        'Nigeria': 'ng',
        'North Macedonia': 'mk',
        'Norway': 'no',
        'Oman': 'om',
        'Pakistan': 'pk',
        'Palau': 'pw',
        'Panama': 'pa',
        'Papua New Guinea': 'pg',
        'Paraguay': 'py',
        'Peru': 'pe',
        'Philippines': 'ph',
        'Poland': 'pl',
        'Portugal': 'pt',
        'Qatar': 'qa',
        'Republic of Korea': 'kr',
        'South Korea': 'kr',
        'Romania': 'ro',
        'Russian Federation': 'ru',
        'Russia': 'ru',
        'Rwanda': 'rw',
        'Saint Kitts and Nevis': 'kn',
        'Saint Lucia': 'lc',
        'Saint Vincent and the Grenadines': 'vc',
        'Samoa': 'ws',
        'San Marino': 'sm',
        'Sao Tome and Principe': 'st',
        'Saudi Arabia': 'sa',
        'Senegal': 'sn',
        'Serbia': 'rs',
        'Seychelles': 'sc',
        'Sierra Leone': 'sl',
        'Singapore': 'sg',
        'Slovakia': 'sk',
        'Slovenia': 'si',
        'Solomon Islands': 'sb',
        'Somalia': 'so',
        'South Africa': 'za',
        'South Sudan': 'ss',
        'Spain': 'es',
        'Sri Lanka': 'lk',
        'Sudan': 'sd',
        'Suriname': 'sr',
        'Sweden': 'se',
        'Switzerland': 'ch',
        'Syrian Arab Republic': 'sy',
        'Syria': 'sy',
        'Tajikistan': 'tj',
        'Thailand': 'th',
        'Timor-Leste': 'tl',
        'East Timor': 'tl',
        'Togo': 'tg',
        'Tonga': 'to',
        'Trinidad and Tobago': 'tt',
        'Tunisia': 'tn',
        'Turkey': 'tr',
        'Turkmenistan': 'tm',
        'Tuvalu': 'tv',
        'Uganda': 'ug',
        'Ukraine': 'ua',
        'United Arab Emirates': 'ae',
        'United Kingdom of Great Britain and Northern Ireland': 'gb',
        'United Kingdom': 'gb',
        'United Republic of Tanzania': 'tz',
        'Tanzania': 'tz',
        'United States of America': 'us',
        'United States': 'us',
        'Uruguay': 'uy',
        'Uzbekistan': 'uz',
        'Vanuatu': 'vu',
        'Vatican City': 'va',
        'Venezuela': 've',
        'Vietnam': 'vn',
        'Yemen': 'ye',
        'Zambia': 'zm',
        'Zimbabwe': 'zw',
        'Taiwan': 'tw',
        'Eswatini': 'sz',
        'Ivory Coast': 'ci'
    }
    
    # Copy files for each resolution
    copied_count = 0
    missing_count = 0
    
    for country in countries_data:
        country_name = country['name']
        iso_code = iso_mapping.get(country_name)
        
        if not iso_code:
            print(f"⚠️  No ISO mapping found for: {country_name}")
            missing_count += 1
            continue
        
        # Check if the country exists in Mapsicon
        mapsicon_path = Path(f'mapsicon/all/{iso_code}')
        if not mapsicon_path.exists():
            print(f"⚠️  Country not found in Mapsicon: {country_name} ({iso_code})")
            missing_count += 1
            continue
        
        # Copy all resolutions
        for res in resolutions:
            src_file = mapsicon_path / f'{res}.png'
            dst_file = base_dir / res / f'{iso_code}.png'
            
            if src_file.exists():
                shutil.copy2(src_file, dst_file)
        
        # Copy SVG
        svg_src = mapsicon_path / 'vector.svg'
        svg_dst = base_dir / 'svg' / f'{iso_code}.svg'
        if svg_src.exists():
            shutil.copy2(svg_src, svg_dst)
        
        copied_count += 1
        print(f"✓ Copied {country_name} ({iso_code})")
    
    print(f"\n📊 Summary:")
    print(f"✅ Successfully copied: {copied_count} countries")
    print(f"⚠️  Missing: {missing_count} countries")
    print(f"📁 Files saved to: mapsicon_downloads/")
    
    return copied_count, missing_count

if __name__ == '__main__':
    download_mapsicon_resolutions()
