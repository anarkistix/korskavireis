#!/usr/bin/env python3
"""
Script to analyze mountain data coverage across all countries
"""

import json

def analyze_mountain_coverage():
    """Analyze which countries have mountain data and which are missing"""
    
    print("🏔️ ANALYSERER FJELLDATA-DEKNING")
    print("=" * 50)
    
    try:
        # Load countries data
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        
        total_countries = len(countries)
        countries_with_mountains = []
        countries_without_mountains = []
        
        # Analyze each country
        for country in countries:
            country_name = country.get('name', 'Unknown')
            
            if 'highest_mountain' in country and country['highest_mountain']:
                countries_with_mountains.append({
                    'name': country_name,
                    'mountain': country['highest_mountain'],
                    'elevation_m': country.get('highest_elevation_meters', 'N/A'),
                    'elevation_ft': country.get('highest_elevation_feet', 'N/A')
                })
            else:
                countries_without_mountains.append(country_name)
        
        # Calculate statistics
        coverage_count = len(countries_with_mountains)
        missing_count = len(countries_without_mountains)
        coverage_percentage = (coverage_count / total_countries) * 100
        
        # Print results
        print(f"📊 STATISTIKK:")
        print(f"   Totalt antall land: {total_countries}")
        print(f"   Land med fjelldata: {coverage_count}")
        print(f"   Land uten fjelldata: {missing_count}")
        print(f"   Dekning: {coverage_percentage:.1f}%")
        
        print(f"\n✅ LAND MED FJELLDATA ({coverage_count}):")
        print("-" * 40)
        for country in countries_with_mountains:
            print(f"   {country['name']}: {country['mountain']} ({country['elevation_m']}m)")
        
        if countries_without_mountains:
            print(f"\n❌ LAND UTEN FJELLDATA ({missing_count}):")
            print("-" * 40)
            for country in countries_without_mountains:
                print(f"   {country}")
        
        # Find highest and lowest mountains
        if countries_with_mountains:
            highest = max(countries_with_mountains, key=lambda x: x['elevation_m'] if isinstance(x['elevation_m'], int) else 0)
            lowest = min(countries_with_mountains, key=lambda x: x['elevation_m'] if isinstance(x['elevation_m'], int) else float('inf'))
            
            print(f"\n🏆 HØYESTE FJELL:")
            print(f"   {highest['name']}: {highest['mountain']} ({highest['elevation_m']}m)")
            
            print(f"\n🏔️ LAVESTE FJELL:")
            print(f"   {lowest['name']}: {lowest['mountain']} ({lowest['elevation_m']}m)")
        
        # Save detailed analysis to file
        analysis_data = {
            'summary': {
                'total_countries': total_countries,
                'countries_with_mountains': coverage_count,
                'countries_without_mountains': missing_count,
                'coverage_percentage': coverage_percentage
            },
            'countries_with_mountains': countries_with_mountains,
            'countries_without_mountains': countries_without_mountains
        }
        
        with open('mountain_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detaljert analyse lagret til mountain_analysis.json")
        
        return coverage_percentage
        
    except Exception as e:
        print(f"❌ Feil ved analyse: {e}")
        return 0

if __name__ == "__main__":
    analyze_mountain_coverage()
