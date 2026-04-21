#!/usr/bin/env python3
"""
Prepare country data for the iOS Globorama app.

Reads the web app's JSON data files, strips GeoJSON geometry,
pre-computes country center coordinates, and outputs a single
optimized JSON file for bundling in the iOS app.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
NO_FILE = REPO_ROOT / "countries_data_no.json"
EN_FILE = REPO_ROOT / "countries_data.json"
OUTPUT = Path(__file__).resolve().parent.parent / "Globorama" / "Resources" / "countries.json"


def calculate_center(geometry: dict) -> dict | None:
    """Compute bounding-box midpoint, matching the web app's calculateCenter()."""
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    if geometry["type"] == "Polygon":
        for point in geometry["coordinates"][0]:
            min_x = min(min_x, point[0])
            min_y = min(min_y, point[1])
            max_x = max(max_x, point[0])
            max_y = max(max_y, point[1])
    elif geometry["type"] == "MultiPolygon":
        for polygon in geometry["coordinates"]:
            for point in polygon[0]:
                min_x = min(min_x, point[0])
                min_y = min(min_y, point[1])
                max_x = max(max_x, point[0])
                max_y = max(max_y, point[1])
    else:
        return None

    return {
        "lon": (min_x + max_x) / 2,
        "lat": (min_y + max_y) / 2,
    }


def main():
    with open(NO_FILE, encoding="utf-8") as f:
        no_data = json.load(f)
    with open(EN_FILE, encoding="utf-8") as f:
        en_data = json.load(f)

    en_by_iso3 = {c["iso3"]: c for c in en_data}

    countries = []
    for c in no_data:
        iso3 = c["iso3"]
        en_country = en_by_iso3.get(iso3, {})

        center = calculate_center(c["geometry"]) if c.get("geometry") else None
        if center is None:
            print(f"WARNING: No center for {c['name']} ({iso3})", file=sys.stderr)
            continue

        cap = c.get("capital_coordinates") or {}
        borders_no = en_country.get("borders_no") or c.get("borders_no") or []

        country = {
            "name": c["name"],
            "nameNo": c.get("name_no") or c["name"],
            "originalName": c.get("original_name", c["name"]),
            "iso3": iso3,
            "continent": c["continent"],
            "region": c["region"],
            "centerLat": round(center["lat"], 6),
            "centerLon": round(center["lon"], 6),
            "flagFile": c["flagFile"],
            "imageFile": c["imageFile"],
            "population": c["population"],
            "populationYear": c["population_year"],
            "googleMapsUrl": c["google_maps_url"],
            "capital": c["capital"],
            "capitalLat": round(cap.get("lat", 0.0), 6),
            "capitalLon": round(cap.get("lon", 0.0), 6),
            "highestMountain": c["highest_mountain"],
            "highestElevationMeters": c["highest_elevation_meters"],
            "highestElevationFeet": c["highest_elevation_feet"],
            "borders": c.get("borders") or [],
            "bordersNo": borders_no,
            "isIsland": c.get("is_island", False),
        }
        countries.append(country)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(countries, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(countries)} countries to {OUTPUT}")
    print(f"File size: {OUTPUT.stat().st_size / 1024:.0f} KB")

    islands = sum(1 for c in countries if c["isIsland"])
    with_borders_no = sum(1 for c in countries if c["bordersNo"])
    with_diff_name = sum(1 for c in countries if c["name"] != c["nameNo"])
    print(f"Islands: {islands}")
    print(f"Countries with bordersNo: {with_borders_no}")
    print(f"Countries with different NO name: {with_diff_name}")


if __name__ == "__main__":
    main()
