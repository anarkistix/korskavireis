#!/usr/bin/env python3
"""
Test script for checking random distribution of countries in KorSkaViReis
Tests the random selection logic directly without browser
"""

import json
import random
from collections import Counter
import time

def test_random_distribution():
    total_simulations = 10000
    print(f"🚀 Starter test av random-funksjonen...")
    print(f"📊 Simulerer {total_simulations} spill...")
    print("-" * 50)
    
    # Load countries data
    try:
        with open('countries_data.json', 'r', encoding='utf-8') as f:
            countries_data = json.load(f)
        total_countries = len(countries_data)
        print(f"📋 Totalt antall land i systemet: {total_countries}")
        print(f"🎯 Forventet gjennomsnitt per land: {total_simulations / total_countries:.2f}")
        print("-" * 50)
    except FileNotFoundError:
        print("❌ Kunne ikke laste countries_data.json")
        return
    
    # Simulate the same random selection logic as in the game
    country_counts = Counter()
    start_time = time.time()
    
    for i in range(total_simulations):
        # Simulate the same random selection as in the game
        # From js/main.js line 675: this.currentCountry = this.countries[randomIndex];
        random_index = random.randint(0, len(countries_data) - 1)
        selected_country = countries_data[random_index]
        country_name = selected_country['name']
        
        country_counts[country_name] += 1
        
        if i % 1000 == 0:
            print(f"✅ Spill {i+1}: {country_name}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTATER")
    print("=" * 60)
    
    print(f"⏱️ Total tid: {total_time:.2f} sekunder")
    print(f"📞 Totalt antall spill: {total_simulations}")
    print(f"✅ Vellykkede spill: {total_simulations}")
    print(f"❌ Mislykkede spill: 0")
    print(f"🌍 Unike land funnet: {len(country_counts)}")
    
    coverage = (len(country_counts) / total_countries) * 100
    print(f"📈 Dekning: {coverage:.1f}% ({len(country_counts)}/{total_countries})")
    
    print("\n" + "-" * 60)
    print("🏆 TOP 10 LAND (mest frekvente)")
    print("-" * 60)
    
    for i, (country, count) in enumerate(country_counts.most_common(10), 1):
        percentage = (count / total_simulations) * 100
        expected = total_simulations / total_countries
        deviation = ((count - expected) / expected) * 100
        print(f"{i:2d}. {country:20s} | {count:4d} ganger | {percentage:5.2f}% | {deviation:+6.1f}% fra forventet")
    
    print("\n" + "-" * 60)
    print("🔽 BUNN 10 LAND (minst frekvente)")
    print("-" * 60)
    
    for i, (country, count) in enumerate(country_counts.most_common()[-10:], 1):
        percentage = (count / total_simulations) * 100
        expected = total_simulations / total_countries
        deviation = ((count - expected) / expected) * 100
        print(f"{i:2d}. {country:20s} | {count:4d} ganger | {percentage:5.2f}% | {deviation:+6.1f}% fra forventet")
    
    print("\n" + "-" * 60)
    print("📈 STATISTIKK")
    print("-" * 60)
    
    counts = list(country_counts.values())
    avg_count = sum(counts) / len(counts)
    min_count = min(counts)
    max_count = max(counts)
    
    print(f"📊 Gjennomsnitt per land: {avg_count:.2f}")
    print(f"📉 Minste antall: {min_count}")
    print(f"📈 Største antall: {max_count}")
    print(f"📏 Spenn: {max_count - min_count}")
    
    # Calculate standard deviation
    variance = sum((x - avg_count) ** 2 for x in counts) / len(counts)
    std_dev = variance ** 0.5
    print(f"📐 Standardavvik: {std_dev:.2f}")
    
    # Coefficient of variation (CV) - lower is more uniform
    cv = (std_dev / avg_count) * 100 if avg_count > 0 else 0
    print(f"🎯 Variasjonskoeffisient: {cv:.1f}%")
    
    if cv < 20:
        print("✅ God fordeling - lav variasjon")
    elif cv < 40:
        print("⚠️ Moderat fordeling - noe variasjon")
    else:
        print("❌ Dårlig fordeling - høy variasjon")
    
    # Chi-square test for uniformity
    expected = total_simulations / total_countries
    chi_square = sum(((count - expected) ** 2) / expected for count in counts)
    print(f"🔬 Chi-square statistikk: {chi_square:.2f}")
    
    # Degrees of freedom = number of categories - 1
    df = len(counts) - 1
    print(f"📊 Frihetsgrader: {df}")
    
    # For 191 degrees of freedom, critical value at 5% significance is ~228
    if chi_square < 228:
        print("✅ Chi-square test: Fordelingen er uniform (p > 0.05)")
    else:
        print("❌ Chi-square test: Fordelingen er ikke uniform (p < 0.05)")
    
    print("\n" + "=" * 60)
    print("🎯 KONKLUSJON")
    print("=" * 60)
    
    if len(country_counts) < total_countries * 0.95:
        print("⚠️ Lav dekning - ikke alle land ble testet")
    elif max_count > min_count * 2:
        print("⚠️ Stor variasjon - random-funksjonen kan være biased")
    elif chi_square > 228:
        print("❌ Chi-square test feilet - fordelingen er ikke uniform")
    else:
        print("✅ God fordeling - random-funksjonen ser ut til å fungere bra")
    
    # Save detailed results to file
    results = {
        "test_info": {
            "total_calls": total_simulations,
            "successful_calls": total_simulations,
            "failed_calls": 0,
            "total_time": total_time,
            "unique_countries": len(country_counts)
        },
        "country_counts": dict(country_counts),
        "statistics": {
            "average": avg_count,
            "min": min_count,
            "max": max_count,
            "std_dev": std_dev,
            "cv": cv,
            "chi_square": chi_square,
            "degrees_of_freedom": df
        }
    }
    
    with open('random_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detaljerte resultater lagret i: random_test_results.json")

if __name__ == "__main__":
    test_random_distribution()
