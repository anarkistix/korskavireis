import Foundation

struct Country: Codable, Identifiable, Hashable {
    var id: String { iso3 }
    let name: String
    let nameNo: String
    let originalName: String
    let iso3: String
    let continent: String
    let region: String
    let centerLat: Double
    let centerLon: Double
    let flagFile: String
    let imageFile: String
    let population: Int
    let populationYear: Int
    let googleMapsUrl: String
    let capital: String
    let capitalLat: Double
    let capitalLon: Double
    let highestMountain: String
    let highestElevationMeters: Int
    let highestElevationFeet: Int
    let borders: [String]
    let bordersNo: [String]
    let isIsland: Bool

    func displayName(for language: String) -> String {
        language == "no" ? nameNo : name
    }

    func displayBorders(for language: String) -> [String] {
        if language == "no" && !bordersNo.isEmpty {
            return bordersNo
        }
        return borders
    }

    var silhouetteAssetName: String {
        "silhouette-\(imageFile.replacingOccurrences(of: ".png", with: ""))"
    }

    var flagAssetName: String {
        "flag-\(flagFile.replacingOccurrences(of: ".png", with: ""))"
    }
}
