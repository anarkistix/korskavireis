#!/usr/bin/env python3
"""
Integrate border data from country-borders CSV into countries_data.json (Manual mapping)
"""

import json
import csv
from collections import defaultdict

def integrate_border_data():
    """Integrate border data into countries_data.json"""
    
    print("🗺️ INTEGRERER NABOLAND-DATA (MANUELL MAPPING)")
    print("=" * 55)
    
    try:
        # Load existing countries data
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        
        print(f"✅ Lastet {len(countries)} land fra countries_data.json")
        
        # Manual ISO2 to ISO3 mapping for key countries
        iso2_to_iso3 = {
            'CH': 'CHE',  # Switzerland
            'NO': 'NOR',  # Norway
            'SE': 'SWE',  # Sweden
            'DK': 'DNK',  # Denmark
            'FI': 'FIN',  # Finland
            'DE': 'DEU',  # Germany
            'FR': 'FRA',  # France
            'IT': 'ITA',  # Italy
            'ES': 'ESP',  # Spain
            'PT': 'PRT',  # Portugal
            'AT': 'AUT',  # Austria
            'LI': 'LIE',  # Liechtenstein
            'NL': 'NLD',  # Netherlands
            'BE': 'BEL',  # Belgium
            'LU': 'LUX',  # Luxembourg
            'PL': 'POL',  # Poland
            'CZ': 'CZE',  # Czech Republic
            'SK': 'SVK',  # Slovakia
            'HU': 'HUN',  # Hungary
            'RO': 'ROU',  # Romania
            'BG': 'BGR',  # Bulgaria
            'HR': 'HRV',  # Croatia
            'SI': 'SVN',  # Slovenia
            'RS': 'SRB',  # Serbia
            'ME': 'MNE',  # Montenegro
            'BA': 'BIH',  # Bosnia and Herzegovina
            'MK': 'MKD',  # North Macedonia
            'AL': 'ALB',  # Albania
            'GR': 'GRC',  # Greece
            'TR': 'TUR',  # Turkey
            'RU': 'RUS',  # Russia
            'UA': 'UKR',  # Ukraine
            'BY': 'BLR',  # Belarus
            'LT': 'LTU',  # Lithuania
            'LV': 'LVA',  # Latvia
            'EE': 'EST',  # Estonia
            'MD': 'MDA',  # Moldova
            'GE': 'GEO',  # Georgia
            'AM': 'ARM',  # Armenia
            'AZ': 'AZE',  # Azerbaijan
            'KZ': 'KAZ',  # Kazakhstan
            'KG': 'KGZ',  # Kyrgyzstan
            'TJ': 'TJK',  # Tajikistan
            'UZ': 'UZB',  # Uzbekistan
            'TM': 'TKM',  # Turkmenistan
            'AF': 'AFG',  # Afghanistan
            'PK': 'PAK',  # Pakistan
            'IN': 'IND',  # India
            'CN': 'CHN',  # China
            'MN': 'MNG',  # Mongolia
            'KP': 'PRK',  # North Korea
            'KR': 'KOR',  # South Korea
            'JP': 'JPN',  # Japan
            'TH': 'THA',  # Thailand
            'VN': 'VNM',  # Vietnam
            'LA': 'LAO',  # Laos
            'KH': 'KHM',  # Cambodia
            'MM': 'MMR',  # Myanmar
            'BD': 'BGD',  # Bangladesh
            'NP': 'NPL',  # Nepal
            'BT': 'BTN',  # Bhutan
            'LK': 'LKA',  # Sri Lanka
            'MV': 'MDV',  # Maldives
            'MY': 'MYS',  # Malaysia
            'SG': 'SGP',  # Singapore
            'ID': 'IDN',  # Indonesia
            'PH': 'PHL',  # Philippines
            'BN': 'BRN',  # Brunei
            'TL': 'TLS',  # Timor-Leste
            'AU': 'AUS',  # Australia
            'NZ': 'NZL',  # New Zealand
            'FJ': 'FJI',  # Fiji
            'PG': 'PNG',  # Papua New Guinea
            'SB': 'SLB',  # Solomon Islands
            'VU': 'VUT',  # Vanuatu
            'NC': 'NCL',  # New Caledonia
            'CA': 'CAN',  # Canada
            'US': 'USA',  # United States
            'MX': 'MEX',  # Mexico
            'GT': 'GTM',  # Guatemala
            'BZ': 'BLZ',  # Belize
            'SV': 'SLV',  # El Salvador
            'HN': 'HND',  # Honduras
            'NI': 'NIC',  # Nicaragua
            'CR': 'CRI',  # Costa Rica
            'PA': 'PAN',  # Panama
            'CO': 'COL',  # Colombia
            'VE': 'VEN',  # Venezuela
            'GY': 'GUY',  # Guyana
            'SR': 'SUR',  # Suriname
            'BR': 'BRA',  # Brazil
            'PE': 'PER',  # Peru
            'EC': 'ECU',  # Ecuador
            'BO': 'BOL',  # Bolivia
            'PY': 'PRY',  # Paraguay
            'UY': 'URY',  # Uruguay
            'AR': 'ARG',  # Argentina
            'CL': 'CHL',  # Chile
            'MA': 'MAR',  # Morocco
            'DZ': 'DZA',  # Algeria
            'TN': 'TUN',  # Tunisia
            'LY': 'LBY',  # Libya
            'EG': 'EGY',  # Egypt
            'SD': 'SDN',  # Sudan
            'SS': 'SSD',  # South Sudan
            'ET': 'ETH',  # Ethiopia
            'ER': 'ERI',  # Eritrea
            'DJ': 'DJI',  # Djibouti
            'SO': 'SOM',  # Somalia
            'KE': 'KEN',  # Kenya
            'TZ': 'TZA',  # Tanzania
            'UG': 'UGA',  # Uganda
            'RW': 'RWA',  # Rwanda
            'BI': 'BDI',  # Burundi
            'CD': 'COD',  # Democratic Republic of the Congo
            'CG': 'COG',  # Republic of the Congo
            'GA': 'GAB',  # Gabon
            'CM': 'CMR',  # Cameroon
            'CF': 'CAF',  # Central African Republic
            'TD': 'TCD',  # Chad
            'NE': 'NER',  # Niger
            'NG': 'NGA',  # Nigeria
            'ML': 'MLI',  # Mali
            'BF': 'BFA',  # Burkina Faso
            'CI': 'CIV',  # Ivory Coast
            'GH': 'GHA',  # Ghana
            'TG': 'TGO',  # Togo
            'BJ': 'BEN',  # Benin
            'SN': 'SEN',  # Senegal
            'GM': 'GMB',  # Gambia
            'GN': 'GIN',  # Guinea
            'GW': 'GNB',  # Guinea-Bissau
            'SL': 'SLE',  # Sierra Leone
            'LR': 'LBR',  # Liberia
            'MR': 'MRT',  # Mauritania
            'MA': 'MAR',  # Morocco
            'ZA': 'ZAF',  # South Africa
            'NA': 'NAM',  # Namibia
            'BW': 'BWA',  # Botswana
            'ZW': 'ZWE',  # Zimbabwe
            'ZM': 'ZMB',  # Zambia
            'MW': 'MWI',  # Malawi
            'MZ': 'MOZ',  # Mozambique
            'SZ': 'SWZ',  # Eswatini
            'LS': 'LSO',  # Lesotho
            'MG': 'MDG',  # Madagascar
            'MU': 'MUS',  # Mauritius
            'SC': 'SYC',  # Seychelles
            'KM': 'COM',  # Comoros
            'CV': 'CPV',  # Cape Verde
            'ST': 'STP',  # Sao Tome and Principe
            'GQ': 'GNQ',  # Equatorial Guinea
            'SA': 'SAU',  # Saudi Arabia
            'YE': 'YEM',  # Yemen
            'OM': 'OMN',  # Oman
            'AE': 'ARE',  # United Arab Emirates
            'QA': 'QAT',  # Qatar
            'BH': 'BHR',  # Bahrain
            'KW': 'KWT',  # Kuwait
            'IQ': 'IRQ',  # Iraq
            'JO': 'JOR',  # Jordan
            'SY': 'SYR',  # Syria
            'LB': 'LBN',  # Lebanon
            'IL': 'ISR',  # Israel
            'PS': 'PSE',  # Palestine
            'CY': 'CYP',  # Cyprus
            'IS': 'ISL',  # Iceland
            'IE': 'IRL',  # Ireland
            'GB': 'GBR',  # United Kingdom
            'MT': 'MLT',  # Malta
            'AD': 'AND',  # Andorra
            'MC': 'MCO',  # Monaco
            'SM': 'SMR',  # San Marino
            'VA': 'VAT',  # Vatican City
            'IR': 'IRN',  # Iran
            'AO': 'AGO',  # Angola
            'HT': 'HTI',  # Haiti
            'DO': 'DOM',  # Dominican Republic
            'PH': 'PHL',  # Philippines
            'MG': 'MDG',  # Madagascar
        }
        
        # Create reverse mapping
        iso3_to_name = {}
        for country in countries:
            iso3_to_name[country['iso3']] = country['name']
        
        print(f"✅ Opprettet mapping for {len(iso2_to_iso3)} land")
        
        # Load border data and convert to ISO3
        borders = defaultdict(list)
        with open('country-borders.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                country_code_iso2 = row['country_code']
                border_code_iso2 = row['country_border_code']
                
                # Convert to ISO3
                if country_code_iso2 in iso2_to_iso3:
                    country_code_iso3 = iso2_to_iso3[country_code_iso2]
                    if border_code_iso2 in iso2_to_iso3:
                        border_code_iso3 = iso2_to_iso3[border_code_iso2]
                        border_name = iso3_to_name.get(border_code_iso3, row['country_border_name'])
                        borders[country_code_iso3].append(border_name)
        
        print(f"✅ Konvertert naboland-data for {len(borders)} land")
        
        # Integrate border data into countries
        updated_count = 0
        for country in countries:
            iso3 = country['iso3']
            if iso3 in borders:
                # Get border countries
                border_names = borders[iso3]
                
                # Convert border names to Norwegian if possible
                border_names_norwegian = []
                for border_name in border_names:
                    # Find the Norwegian name for this border country
                    norwegian_name = None
                    for other_country in countries:
                        if other_country['name'] == border_name:
                            norwegian_name = other_country.get('name_no', border_name)
                            break
                    border_names_norwegian.append(norwegian_name or border_name)
                
                # Add border data
                country['borders'] = border_names
                country['borders_no'] = border_names_norwegian
                country['is_island'] = len(border_names) == 0
                updated_count += 1
            else:
                # No borders found - mark as island
                country['borders'] = []
                country['borders_no'] = []
                country['is_island'] = True
                updated_count += 1
        
        # Save updated data
        with open('countries_data.json', 'w', encoding='utf-8') as f:
            json.dump(countries, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Oppdatert {updated_count} land med naboland-data")
        
        # Show some examples
        print("\n📋 Eksempler på naboland-data:")
        examples = ['Switzerland', 'Norway', 'Australia', 'Japan', 'Iceland']
        for example_name in examples:
            for country in countries:
                if country['name'] == example_name:
                    borders_list = country.get('borders', [])
                    is_island = country.get('is_island', False)
                    if is_island:
                        print(f"   {example_name}: Øy (ingen naboland)")
                    else:
                        print(f"   {example_name}: {', '.join(borders_list)}")
                    break
        
        # Also update Norwegian data
        print("\n🇳🇴 OPPDATERER NORSK DATA:")
        try:
            with open('countries_data_no.json', 'r', encoding='utf-8') as f:
                norwegian_countries = json.load(f)
            
            # Update Norwegian countries with border data
            for norwegian_country in norwegian_countries:
                iso3 = norwegian_country['iso3']
                if iso3 in borders:
                    border_names = borders[iso3]
                    norwegian_country['borders'] = border_names
                    norwegian_country['is_island'] = len(border_names) == 0
                else:
                    norwegian_country['borders'] = []
                    norwegian_country['is_island'] = True
            
            with open('countries_data_no.json', 'w', encoding='utf-8') as f:
                json.dump(norwegian_countries, f, indent=2, ensure_ascii=False)
            
            print("✅ Norsk data oppdatert med naboland")
            
        except Exception as e:
            print(f"❌ Feil ved oppdatering av norsk data: {e}")
        
    except Exception as e:
        print(f"❌ Feil ved integrasjon: {e}")

if __name__ == "__main__":
    integrate_border_data()
