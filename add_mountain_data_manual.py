#!/usr/bin/env python3
"""
Script to add mountain data to countries_data.json
Manual mapping based on Wikipedia elevation extremes
"""

import json

def get_mountain_data():
    """Manual mountain data mapping from Wikipedia elevation extremes"""
    
    mountain_data = {
        "Afghanistan": {"mountain_name": "Noshaq", "elevation_meters": 7492, "elevation_feet": 24580},
        "Albania": {"mountain_name": "Korab", "elevation_meters": 2764, "elevation_feet": 9068},
        "Algeria": {"mountain_name": "Mount Tahat", "elevation_meters": 2908, "elevation_feet": 9541},
        "Andorra": {"mountain_name": "Coma Pedrosa", "elevation_meters": 2943, "elevation_feet": 9656},
        "Angola": {"mountain_name": "Mount Moco", "elevation_meters": 2620, "elevation_feet": 8596},
        "Argentina": {"mountain_name": "Aconcagua", "elevation_meters": 6961, "elevation_feet": 22838},
        "Armenia": {"mountain_name": "Mount Aragats", "elevation_meters": 4090, "elevation_feet": 13419},
        "Australia": {"mountain_name": "Mount Kosciuszko", "elevation_meters": 2228, "elevation_feet": 7310},
        "Austria": {"mountain_name": "Grossglockner", "elevation_meters": 3798, "elevation_feet": 12461},
        "Azerbaijan": {"mountain_name": "Mount Bazardüzü", "elevation_meters": 4466, "elevation_feet": 14652},
        "Bahrain": {"mountain_name": "Jabal ad Dukhan", "elevation_meters": 122, "elevation_feet": 400},
        "Bangladesh": {"mountain_name": "Saka Haphong", "elevation_meters": 1052, "elevation_feet": 3451},
        "Belarus": {"mountain_name": "Dzyarzhynskaya Hara", "elevation_meters": 345, "elevation_feet": 1132},
        "Belgium": {"mountain_name": "Signal de Botrange", "elevation_meters": 694, "elevation_feet": 2277},
        "Belize": {"mountain_name": "Doyle's Delight", "elevation_meters": 1124, "elevation_feet": 3688},
        "Benin": {"mountain_name": "Mont Sokbaro", "elevation_meters": 658, "elevation_feet": 2159},
        "Bhutan": {"mountain_name": "Gangkhar Puensum", "elevation_meters": 7570, "elevation_feet": 24836},
        "Bolivia": {"mountain_name": "Nevado Sajama", "elevation_meters": 6542, "elevation_feet": 21463},
        "Bosnia and Herzegovina": {"mountain_name": "Maglić", "elevation_meters": 2386, "elevation_feet": 7828},
        "Botswana": {"mountain_name": "Otse Hill", "elevation_meters": 1494, "elevation_feet": 4902},
        "Brazil": {"mountain_name": "Pico da Neblina", "elevation_meters": 2995, "elevation_feet": 9826},
        "Brunei": {"mountain_name": "Bukit Pagon", "elevation_meters": 1850, "elevation_feet": 6070},
        "Bulgaria": {"mountain_name": "Musala", "elevation_meters": 2925, "elevation_feet": 9596},
        "Burkina Faso": {"mountain_name": "Tena Kourou", "elevation_meters": 749, "elevation_feet": 2457},
        "Burundi": {"mountain_name": "Mount Heha", "elevation_meters": 2684, "elevation_feet": 8806},
        "Cambodia": {"mountain_name": "Phnom Aural", "elevation_meters": 1810, "elevation_feet": 5938},
        "Cameroon": {"mountain_name": "Mount Cameroon", "elevation_meters": 4040, "elevation_feet": 13255},
        "Canada": {"mountain_name": "Mount Logan", "elevation_meters": 5959, "elevation_feet": 19551},
        "Central African Republic": {"mountain_name": "Mont Ngaoui", "elevation_meters": 1420, "elevation_feet": 4659},
        "Chad": {"mountain_name": "Emi Koussi", "elevation_meters": 3445, "elevation_feet": 11304},
        "Chile": {"mountain_name": "Ojos del Salado", "elevation_meters": 6893, "elevation_feet": 22615},
        "China": {"mountain_name": "Mount Everest", "elevation_meters": 8848, "elevation_feet": 29029},
        "Colombia": {"mountain_name": "Pico Cristóbal Colón", "elevation_meters": 5775, "elevation_feet": 18947},
        "Comoros": {"mountain_name": "Mount Karthala", "elevation_meters": 2360, "elevation_feet": 7743},
        "Congo": {"mountain_name": "Mount Nabemba", "elevation_meters": 1020, "elevation_feet": 3346},
        "Costa Rica": {"mountain_name": "Cerro Chirripó", "elevation_meters": 3820, "elevation_feet": 12533},
        "Croatia": {"mountain_name": "Dinara", "elevation_meters": 1831, "elevation_feet": 6007},
        "Cuba": {"mountain_name": "Pico Turquino", "elevation_meters": 1974, "elevation_feet": 6476},
        "Cyprus": {"mountain_name": "Mount Olympus", "elevation_meters": 1952, "elevation_feet": 6404},
        "Czech Republic": {"mountain_name": "Sněžka", "elevation_meters": 1603, "elevation_feet": 5259},
        "Democratic Republic of the Congo": {"mountain_name": "Mount Stanley", "elevation_meters": 5109, "elevation_feet": 16762},
        "Denmark": {"mountain_name": "Møllehøj", "elevation_meters": 170, "elevation_feet": 558},
        "Djibouti": {"mountain_name": "Moussa Ali", "elevation_meters": 2028, "elevation_feet": 6654},
        "Dominican Republic": {"mountain_name": "Pico Duarte", "elevation_meters": 3098, "elevation_feet": 10164},
        "Ecuador": {"mountain_name": "Chimborazo", "elevation_meters": 6268, "elevation_feet": 20564},
        "Egypt": {"mountain_name": "Mount Catherine", "elevation_meters": 2629, "elevation_feet": 8625},
        "El Salvador": {"mountain_name": "Cerro El Pital", "elevation_meters": 2730, "elevation_feet": 8957},
        "Equatorial Guinea": {"mountain_name": "Pico Basile", "elevation_meters": 3008, "elevation_feet": 9869},
        "Eritrea": {"mountain_name": "Emba Soira", "elevation_meters": 3018, "elevation_feet": 9902},
        "Estonia": {"mountain_name": "Suur Munamägi", "elevation_meters": 318, "elevation_feet": 1043},
        "Eswatini": {"mountain_name": "Emlembe", "elevation_meters": 1862, "elevation_feet": 6109},
        "Ethiopia": {"mountain_name": "Ras Dejen", "elevation_meters": 4550, "elevation_feet": 14928},
        "Fiji": {"mountain_name": "Mount Tomanivi", "elevation_meters": 1324, "elevation_feet": 4344},
        "Finland": {"mountain_name": "Halti", "elevation_meters": 1324, "elevation_feet": 4344},
        "France": {"mountain_name": "Mont Blanc", "elevation_meters": 4809, "elevation_feet": 15777},
        "Gabon": {"mountain_name": "Mont Bengoué", "elevation_meters": 1070, "elevation_feet": 3510},
        "Gambia": {"mountain_name": "Red Rock", "elevation_meters": 53, "elevation_feet": 174},
        "Georgia": {"mountain_name": "Shkhara", "elevation_meters": 5201, "elevation_feet": 17064},
        "Germany": {"mountain_name": "Zugspitze", "elevation_meters": 2962, "elevation_feet": 9717},
        "Ghana": {"mountain_name": "Mount Afadjato", "elevation_meters": 885, "elevation_feet": 2904},
        "Greece": {"mountain_name": "Mount Olympus", "elevation_meters": 2917, "elevation_feet": 9570},
        "Guatemala": {"mountain_name": "Volcán Tajumulco", "elevation_meters": 4220, "elevation_feet": 13845},
        "Guinea": {"mountain_name": "Mount Richard-Molard", "elevation_meters": 1752, "elevation_feet": 5748},
        "Guinea-Bissau": {"mountain_name": "Unnamed location", "elevation_meters": 300, "elevation_feet": 984},
        "Guyana": {"mountain_name": "Mount Roraima", "elevation_meters": 2810, "elevation_feet": 9220},
        "Haiti": {"mountain_name": "Pic la Selle", "elevation_meters": 2680, "elevation_feet": 8793},
        "Honduras": {"mountain_name": "Cerro Las Minas", "elevation_meters": 2870, "elevation_feet": 9416},
        "Hungary": {"mountain_name": "Kékes", "elevation_meters": 1014, "elevation_feet": 3327},
        "Iceland": {"mountain_name": "Hvannadalshnúkur", "elevation_meters": 2110, "elevation_feet": 6923},
        "India": {"mountain_name": "Kangchenjunga", "elevation_meters": 8586, "elevation_feet": 28169},
        "Indonesia": {"mountain_name": "Puncak Jaya", "elevation_meters": 4884, "elevation_feet": 16024},
        "Iran": {"mountain_name": "Mount Damavand", "elevation_meters": 5610, "elevation_feet": 18406},
        "Iraq": {"mountain_name": "Cheekha Dar", "elevation_meters": 3611, "elevation_feet": 11847},
        "Ireland": {"mountain_name": "Carrauntoohil", "elevation_meters": 1038, "elevation_feet": 3405},
        "Israel": {"mountain_name": "Mount Hermon", "elevation_meters": 2236, "elevation_feet": 7336},
        "Italy": {"mountain_name": "Monte Bianco", "elevation_meters": 4809, "elevation_feet": 15777},
        "Ivory Coast": {"mountain_name": "Mount Nimba", "elevation_meters": 1752, "elevation_feet": 5748},
        "Jamaica": {"mountain_name": "Blue Mountain Peak", "elevation_meters": 2256, "elevation_feet": 7402},
        "Japan": {"mountain_name": "Mount Fuji", "elevation_meters": 3776, "elevation_feet": 12388},
        "Jordan": {"mountain_name": "Jabal Umm ad Dami", "elevation_meters": 1854, "elevation_feet": 6083},
        "Kazakhstan": {"mountain_name": "Khan Tengri", "elevation_meters": 7010, "elevation_feet": 23002},
        "Kenya": {"mountain_name": "Mount Kenya", "elevation_meters": 5199, "elevation_feet": 17057},
        "Kuwait": {"mountain_name": "Mutla Ridge", "elevation_meters": 306, "elevation_feet": 1004},
        "Kyrgyzstan": {"mountain_name": "Jengish Chokusu", "elevation_meters": 7439, "elevation_feet": 24406},
        "Laos": {"mountain_name": "Phou Bia", "elevation_meters": 2817, "elevation_feet": 9242},
        "Latvia": {"mountain_name": "Gaiziņkalns", "elevation_meters": 312, "elevation_feet": 1024},
        "Lebanon": {"mountain_name": "Qurnat as Sawda'", "elevation_meters": 3088, "elevation_feet": 10133},
        "Lesotho": {"mountain_name": "Thabana Ntlenyana", "elevation_meters": 3482, "elevation_feet": 11424},
        "Liberia": {"mountain_name": "Mount Wuteve", "elevation_meters": 1440, "elevation_feet": 4724},
        "Libya": {"mountain_name": "Bikku Bitti", "elevation_meters": 2267, "elevation_feet": 7438},
        "Lithuania": {"mountain_name": "Aukštojas Hill", "elevation_meters": 294, "elevation_feet": 965},
        "Luxembourg": {"mountain_name": "Kneiff", "elevation_meters": 560, "elevation_feet": 1837},
        "Madagascar": {"mountain_name": "Maromokotro", "elevation_meters": 2876, "elevation_feet": 9436},
        "Malawi": {"mountain_name": "Mount Mulanje", "elevation_meters": 3002, "elevation_feet": 9849},
        "Malaysia": {"mountain_name": "Mount Kinabalu", "elevation_meters": 4095, "elevation_feet": 13435},
        "Mali": {"mountain_name": "Hombori Tondo", "elevation_meters": 1155, "elevation_feet": 3789},
        "Mauritania": {"mountain_name": "Kediet ej Jill", "elevation_meters": 915, "elevation_feet": 3002},
        "Mauritius": {"mountain_name": "Piton de la Petite Rivière Noire", "elevation_meters": 828, "elevation_feet": 2717},
        "Mexico": {"mountain_name": "Pico de Orizaba", "elevation_meters": 5636, "elevation_feet": 18491},
        "Moldova": {"mountain_name": "Bălănești Hill", "elevation_meters": 430, "elevation_feet": 1411},
        "Monaco": {"mountain_name": "Chemin des Révoires", "elevation_meters": 161, "elevation_feet": 528},
        "Mongolia": {"mountain_name": "Khüiten Peak", "elevation_meters": 4374, "elevation_feet": 14350},
        "Montenegro": {"mountain_name": "Zla Kolata", "elevation_meters": 2534, "elevation_feet": 8314},
        "Morocco": {"mountain_name": "Jbel Toubkal", "elevation_meters": 4167, "elevation_feet": 13671},
        "Mozambique": {"mountain_name": "Mount Binga", "elevation_meters": 2436, "elevation_feet": 7992},
        "Myanmar": {"mountain_name": "Hkakabo Razi", "elevation_meters": 5881, "elevation_feet": 19295},
        "Namibia": {"mountain_name": "Königstein", "elevation_meters": 2606, "elevation_feet": 8550},
        "Nepal": {"mountain_name": "Mount Everest", "elevation_meters": 8848, "elevation_feet": 29029},
        "Netherlands": {"mountain_name": "Mount Scenery", "elevation_meters": 887, "elevation_feet": 2910},
        "New Zealand": {"mountain_name": "Aoraki / Mount Cook", "elevation_meters": 3724, "elevation_feet": 12218},
        "Nicaragua": {"mountain_name": "Mogotón", "elevation_meters": 2107, "elevation_feet": 6913},
        "Niger": {"mountain_name": "Mont Idoukal-n-Taghès", "elevation_meters": 2022, "elevation_feet": 6634},
        "Nigeria": {"mountain_name": "Chappal Waddi", "elevation_meters": 2419, "elevation_feet": 7936},
        "North Korea": {"mountain_name": "Mount Paektu", "elevation_meters": 2744, "elevation_feet": 9003},
        "North Macedonia": {"mountain_name": "Mount Korab", "elevation_meters": 2764, "elevation_feet": 9068},
        "Norway": {"mountain_name": "Galdhøpiggen", "elevation_meters": 2469, "elevation_feet": 8100},
        "Oman": {"mountain_name": "Jebel Shams", "elevation_meters": 3009, "elevation_feet": 9872},
        "Pakistan": {"mountain_name": "K2", "elevation_meters": 8611, "elevation_feet": 28251},
        "Panama": {"mountain_name": "Volcán Barú", "elevation_meters": 3475, "elevation_feet": 11401},
        "Papua New Guinea": {"mountain_name": "Mount Wilhelm", "elevation_meters": 4509, "elevation_feet": 14793},
        "Paraguay": {"mountain_name": "Cerro Peró", "elevation_meters": 842, "elevation_feet": 2762},
        "Peru": {"mountain_name": "Huascarán", "elevation_meters": 6768, "elevation_feet": 22205},
        "Philippines": {"mountain_name": "Mount Apo", "elevation_meters": 2954, "elevation_feet": 9692},
        "Poland": {"mountain_name": "Rysy", "elevation_meters": 2499, "elevation_feet": 8199},
        "Portugal": {"mountain_name": "Mount Pico", "elevation_meters": 2351, "elevation_feet": 7713},
        "Qatar": {"mountain_name": "Qurayn Abu al Bawl", "elevation_meters": 103, "elevation_feet": 338},
        "Romania": {"mountain_name": "Moldoveanu Peak", "elevation_meters": 2544, "elevation_feet": 8346},
        "Russia": {"mountain_name": "Mount Elbrus", "elevation_meters": 5642, "elevation_feet": 18510},
        "Rwanda": {"mountain_name": "Mount Karisimbi", "elevation_meters": 4507, "elevation_feet": 14787},
        "Saint Kitts and Nevis": {"mountain_name": "Mount Liamuiga", "elevation_meters": 1156, "elevation_feet": 3793},
        "Saint Lucia": {"mountain_name": "Mount Gimie", "elevation_meters": 950, "elevation_feet": 3117},
        "Saint Vincent and the Grenadines": {"mountain_name": "La Soufrière", "elevation_meters": 1234, "elevation_feet": 4049},
        "Samoa": {"mountain_name": "Mount Silisili", "elevation_meters": 1858, "elevation_feet": 6096},
        "Saudi Arabia": {"mountain_name": "Jabal Sawda", "elevation_meters": 3000, "elevation_feet": 9843},
        "Senegal": {"mountain_name": "Unnamed location", "elevation_meters": 648, "elevation_feet": 2126},
        "Serbia": {"mountain_name": "Midžor", "elevation_meters": 2169, "elevation_feet": 7116},
        "Seychelles": {"mountain_name": "Morne Seychellois", "elevation_meters": 905, "elevation_feet": 2969},
        "Sierra Leone": {"mountain_name": "Mount Bintumani", "elevation_meters": 1948, "elevation_feet": 6391},
        "Singapore": {"mountain_name": "Bukit Timah Hill", "elevation_meters": 164, "elevation_feet": 538},
        "Slovakia": {"mountain_name": "Gerlachovský štít", "elevation_meters": 2655, "elevation_feet": 8711},
        "Slovenia": {"mountain_name": "Triglav", "elevation_meters": 2864, "elevation_feet": 9396},
        "Solomon Islands": {"mountain_name": "Mount Popomanaseu", "elevation_meters": 2335, "elevation_feet": 7661},
        "Somalia": {"mountain_name": "Shimbiris", "elevation_meters": 2450, "elevation_feet": 8038},
        "South Africa": {"mountain_name": "Mafadi", "elevation_meters": 3450, "elevation_feet": 11319},
        "South Korea": {"mountain_name": "Hallasan", "elevation_meters": 1950, "elevation_feet": 6398},
        "South Sudan": {"mountain_name": "Kinyeti", "elevation_meters": 3187, "elevation_feet": 10456},
        "Spain": {"mountain_name": "Teide", "elevation_meters": 3718, "elevation_feet": 12198},
        "Sri Lanka": {"mountain_name": "Pidurutalagala", "elevation_meters": 2524, "elevation_feet": 8281},
        "Sudan": {"mountain_name": "Deriba Caldera", "elevation_meters": 3042, "elevation_feet": 9980},
        "Suriname": {"mountain_name": "Juliana Top", "elevation_meters": 1230, "elevation_feet": 4035},
        "Sweden": {"mountain_name": "Kebnekaise", "elevation_meters": 2106, "elevation_feet": 6910},
        "Switzerland": {"mountain_name": "Dufourspitze", "elevation_meters": 4634, "elevation_feet": 15203},
        "Syria": {"mountain_name": "Mount Hermon", "elevation_meters": 2814, "elevation_feet": 9232},
        "Taiwan": {"mountain_name": "Yu Shan", "elevation_meters": 3952, "elevation_feet": 12966},
        "Tajikistan": {"mountain_name": "Ismoil Somoni Peak", "elevation_meters": 7495, "elevation_feet": 24590},
        "Tanzania": {"mountain_name": "Mount Kilimanjaro", "elevation_meters": 5895, "elevation_feet": 19341},
        "Thailand": {"mountain_name": "Doi Inthanon", "elevation_meters": 2565, "elevation_feet": 8415},
        "Togo": {"mountain_name": "Mount Agou", "elevation_meters": 986, "elevation_feet": 3235},
        "Tunisia": {"mountain_name": "Jebel ech Chambi", "elevation_meters": 1544, "elevation_feet": 5066},
        "Turkey": {"mountain_name": "Mount Ararat", "elevation_meters": 5137, "elevation_feet": 16854},
        "Turkmenistan": {"mountain_name": "Aýrybaba", "elevation_meters": 3139, "elevation_feet": 10299},
        "Uganda": {"mountain_name": "Mount Stanley", "elevation_meters": 5109, "elevation_feet": 16762},
        "Ukraine": {"mountain_name": "Hoverla", "elevation_meters": 2061, "elevation_feet": 6762},
        "United Arab Emirates": {"mountain_name": "Jabal Yibir", "elevation_meters": 1527, "elevation_feet": 5010},
        "United Kingdom": {"mountain_name": "Ben Nevis", "elevation_meters": 1345, "elevation_feet": 4413},
        "United States": {"mountain_name": "Denali", "elevation_meters": 6190, "elevation_feet": 20310},
        "Uruguay": {"mountain_name": "Cerro Catedral", "elevation_meters": 514, "elevation_feet": 1686},
        "Uzbekistan": {"mountain_name": "Khazret Sultan", "elevation_meters": 4643, "elevation_feet": 15233},
        "Venezuela": {"mountain_name": "Pico Bolívar", "elevation_meters": 4978, "elevation_feet": 16332},
        "Vietnam": {"mountain_name": "Fansipan", "elevation_meters": 3143, "elevation_feet": 10312},
        "Yemen": {"mountain_name": "Jabal an-Nabi Shu'ayb", "elevation_meters": 3666, "elevation_feet": 12028},
        "Zambia": {"mountain_name": "Mafinga Central", "elevation_meters": 2329, "elevation_feet": 7641},
        "Zimbabwe": {"mountain_name": "Mount Nyangani", "elevation_meters": 2592, "elevation_feet": 8504}
    }
    
    return mountain_data

def update_countries_data():
    """Update countries_data.json with mountain information"""
    
    print("🏔️ LEGGER TIL FJELLDATA I KORSAKAVIREIS")
    print("=" * 50)
    
    # Get mountain data
    mountain_data = get_mountain_data()
    
    print(f"📊 Har fjelldata for {len(mountain_data)} land")
    
    try:
        # Load existing data
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        
        updated_count = 0
        
        for country in countries:
            country_name = country.get('name', '')
            
            if country_name in mountain_data:
                mountain_info = mountain_data[country_name]
                country['highest_mountain'] = mountain_info['mountain_name']
                country['highest_elevation_meters'] = mountain_info['elevation_meters']
                country['highest_elevation_feet'] = mountain_info['elevation_feet']
                updated_count += 1
                print(f"✅ {country_name}: {mountain_info['mountain_name']} ({mountain_info['elevation_meters']}m)")
        
        # Save updated data
        with open('countries_data.json', 'w', encoding='utf-8') as f:
            json.dump(countries, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Oppdatert {updated_count} land med fjelldata")
        print(f"💾 Lagret til countries_data.json")
        
        return updated_count
        
    except Exception as e:
        print(f"❌ Feil ved oppdatering: {e}")
        return 0

if __name__ == "__main__":
    update_countries_data()
