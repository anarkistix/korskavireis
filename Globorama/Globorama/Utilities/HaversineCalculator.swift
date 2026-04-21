import Foundation

enum CompassDirection: String, CaseIterable {
    case north, northeast, east, southeast
    case south, southwest, west, northwest

    var emoji: String {
        switch self {
        case .north: "⬆️"
        case .northeast: "↗️"
        case .east: "➡️"
        case .southeast: "↘️"
        case .south: "⬇️"
        case .southwest: "↙️"
        case .west: "⬅️"
        case .northwest: "↖️"
        }
    }

    func localizedName(for language: String) -> String {
        let keys: [CompassDirection: (no: String, en: String)] = [
            .north: ("nord", "north"),
            .northeast: ("nordøst", "northeast"),
            .east: ("øst", "east"),
            .southeast: ("sørøst", "southeast"),
            .south: ("sør", "south"),
            .southwest: ("sørvest", "southwest"),
            .west: ("vest", "west"),
            .northwest: ("nordvest", "northwest"),
        ]
        let pair = keys[self]!
        return language == "no" ? pair.no : pair.en
    }
}

enum HaversineCalculator {
    private static let earthRadiusKm: Double = 6371

    static func distance(
        fromLat lat1: Double, fromLon lon1: Double,
        toLat lat2: Double, toLon lon2: Double
    ) -> Double {
        let dLat = toRadians(lat2 - lat1)
        let dLon = toRadians(lon2 - lon1)

        let a = sin(dLat / 2) * sin(dLat / 2) +
            cos(toRadians(lat1)) * cos(toRadians(lat2)) *
            sin(dLon / 2) * sin(dLon / 2)

        let c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return earthRadiusKm * c
    }

    static func direction(
        fromLat lat1: Double, fromLon lon1: Double,
        toLat lat2: Double, toLon lon2: Double
    ) -> CompassDirection {
        let dLat = lat2 - lat1
        let dLon = lon2 - lon1
        var angle = atan2(dLon, dLat) * (180.0 / .pi)
        if angle < 0 { angle += 360 }

        switch angle {
        case 337.5..<360, 0..<22.5: return .north
        case 22.5..<67.5: return .northeast
        case 67.5..<112.5: return .east
        case 112.5..<157.5: return .southeast
        case 157.5..<202.5: return .south
        case 202.5..<247.5: return .southwest
        case 247.5..<292.5: return .west
        case 292.5..<337.5: return .northwest
        default: return .north
        }
    }

    private static func toRadians(_ degrees: Double) -> Double {
        degrees * .pi / 180
    }
}
