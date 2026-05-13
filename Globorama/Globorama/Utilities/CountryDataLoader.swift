import Foundation
import os

private let logger = Logger(subsystem: Bundle.main.bundleIdentifier ?? "com.mariusarnesen.globorama", category: "data")

enum CountryDataLoader {
    static func loadCountries() -> [Country] {
        guard let url = Bundle.main.url(forResource: "countries", withExtension: "json") else {
            logger.error("countries.json not found in bundle")
            return fallbackCountries
        }
        do {
            let data = try Data(contentsOf: url)
            return try JSONDecoder().decode([Country].self, from: data)
        } catch {
            logger.error("Failed to decode countries.json: \(error)")
            return fallbackCountries
        }
    }

    private static let fallbackCountries: [Country] = [
        Country(
            name: "Norway", nameNo: "Norge", originalName: "Norway",
            iso3: "NOR", continent: "Europe", region: "Northern Europe",
            centerLat: 64.57, centerLon: 17.93,
            flagFile: "no.png", imageFile: "no.png",
            population: 5_421_241, populationYear: 2023,
            googleMapsUrl: "https://www.google.com/maps/search/Norway",
            capital: "Oslo", capitalLat: 59.91, capitalLon: 10.75,
            highestMountain: "Galdhøpiggen",
            highestElevationMeters: 2469, highestElevationFeet: 8100,
            borders: ["Finland", "Russia", "Sweden"],
            bordersNo: ["Finland", "Russland", "Sverige"],
            isIsland: false
        ),
        Country(
            name: "Sweden", nameNo: "Sverige", originalName: "Sweden",
            iso3: "SWE", continent: "Europe", region: "Northern Europe",
            centerLat: 62.20, centerLon: 17.64,
            flagFile: "se.png", imageFile: "se.png",
            population: 10_521_556, populationYear: 2023,
            googleMapsUrl: "https://www.google.com/maps/search/Sweden",
            capital: "Stockholm", capitalLat: 59.33, capitalLon: 18.07,
            highestMountain: "Kebnekaise",
            highestElevationMeters: 2097, highestElevationFeet: 6880,
            borders: ["Finland", "Norway"],
            bordersNo: ["Finland", "Norge"],
            isIsland: false
        ),
        Country(
            name: "Denmark", nameNo: "Danmark", originalName: "Denmark",
            iso3: "DNK", continent: "Europe", region: "Northern Europe",
            centerLat: 56.26, centerLon: 9.50,
            flagFile: "dk.png", imageFile: "dk.png",
            population: 5_910_913, populationYear: 2023,
            googleMapsUrl: "https://www.google.com/maps/search/Denmark",
            capital: "Copenhagen", capitalLat: 55.68, capitalLon: 12.57,
            highestMountain: "Møllehøj",
            highestElevationMeters: 171, highestElevationFeet: 561,
            borders: ["Germany"],
            bordersNo: ["Tyskland"],
            isIsland: false
        ),
    ]
}
