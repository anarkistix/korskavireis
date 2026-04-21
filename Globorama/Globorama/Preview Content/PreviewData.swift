import Foundation

enum PreviewData {
    static let norway = Country(
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
    )

    static let japan = Country(
        name: "Japan", nameNo: "Japan", originalName: "Japan",
        iso3: "JPN", continent: "Asia", region: "Eastern Asia",
        centerLat: 34.87, centerLon: 134.75,
        flagFile: "jp.png", imageFile: "jp.png",
        population: 125_681_593, populationYear: 2023,
        googleMapsUrl: "https://www.google.com/maps/search/Japan",
        capital: "Tokyo", capitalLat: 35.68, capitalLon: 139.69,
        highestMountain: "Mount Fuji",
        highestElevationMeters: 3776, highestElevationFeet: 12388,
        borders: [], bordersNo: [],
        isIsland: true
    )
}
