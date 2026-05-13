import Foundation

enum HintSlot {
    case flag, population, capital, region, mountain, neighbors, silhouette
}

enum GameMode: String, Codable, CaseIterable, Identifiable {
    case silhouette, flag, capital, mountain

    var id: String { rawValue }

    var emoji: String {
        switch self {
        case .silhouette: "🗺️"
        case .flag: "🏳️"
        case .capital: "🏛️"
        case .mountain: "⛰️"
        }
    }

    func displayName(for language: String) -> String {
        switch self {
        case .silhouette: language == "no" ? "Silhuett" : "Silhouette"
        case .flag: language == "no" ? "Flagg" : "Flag"
        case .capital: language == "no" ? "Hovedstad" : "Capital"
        case .mountain: language == "no" ? "Fjell" : "Mountain"
        }
    }

    func clueDescription(for language: String) -> String {
        switch self {
        case .silhouette:
            language == "no" ? "Gjett landet fra silhuetten" : "Guess the country from its silhouette"
        case .flag:
            language == "no" ? "Gjett landet fra flagget" : "Guess the country from its flag"
        case .capital:
            language == "no" ? "Gjett landet fra hovedstaden" : "Guess the country from its capital"
        case .mountain:
            language == "no" ? "Gjett landet fra fjelltoppen" : "Guess the country from its highest peak"
        }
    }

    var hintSlots: [HintSlot] {
        switch self {
        case .silhouette:
            [.flag, .population, .capital, .region, .mountain, .neighbors]
        case .flag:
            [.silhouette, .population, .capital, .region, .mountain, .neighbors]
        case .capital:
            [.flag, .population, .silhouette, .region, .mountain, .neighbors]
        case .mountain:
            [.flag, .population, .capital, .region, .silhouette, .neighbors]
        }
    }
}
