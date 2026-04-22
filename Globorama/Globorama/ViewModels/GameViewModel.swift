import Foundation
import Observation
import SwiftData
import UIKit

struct GuessResult: Identifiable, Equatable {
    let id = UUID()
    let attemptNumber: Int
    let countryName: String
    let isCorrect: Bool
    let distanceKm: Int?
    let direction: CompassDirection?
}

@Observable
class GameViewModel {
    var countries: [Country] = []
    var currentCountry: Country?
    var gameState: GameState = .playing
    var attempts: Int = 0
    var guessResults: [GuessResult] = []
    var guessedCountryIds: Set<String> = []
    var searchText: String = ""
    var toastMessage: String?

    @ObservationIgnored
    var modelContext: ModelContext?
    @ObservationIgnored
    var recentlyPlayedIso3s: [String] = []
    @ObservationIgnored
    var gameStartTime: Date = .now

    let maxAttempts = 10

    var language: String = UserDefaults.standard.string(forKey: "selectedLanguage") ?? "no" {
        didSet {
            UserDefaults.standard.set(language, forKey: "selectedLanguage")
        }
    }

    var hintsUnlocked: Int {
        min(attempts, 6)
    }

    var filteredCountries: [Country] {
        let query = searchText.lowercased().trimmingCharacters(in: .whitespaces)
        guard !query.isEmpty else { return [] }

        let matches = countries.filter { country in
            let displayName = country.displayName(for: language)
            return displayName.lowercased().contains(query) ||
                country.iso3.lowercased().contains(query)
        }

        return matches
            .sorted { a, b in
                let aName = a.displayName(for: language).lowercased()
                let bName = b.displayName(for: language).lowercased()
                let aPrefix = aName.hasPrefix(query)
                let bPrefix = bName.hasPrefix(query)
                if aPrefix != bPrefix { return aPrefix }
                return aName < bName
            }
            .prefix(10)
            .map { $0 }
    }

    init(modelContext: ModelContext? = nil) {
        self.modelContext = modelContext
        countries = CountryDataLoader.loadCountries()
        startNewGame()
    }

    func startNewGame() {
        let gameMode = UserDefaults.standard.string(forKey: "gameMode") ?? "random"

        if gameMode == "specific",
           let specificName = UserDefaults.standard.string(forKey: "specificCountry"),
           let country = countries.first(where: { $0.name == specificName || $0.nameNo == specificName }) {
            currentCountry = country
        } else {
            selectRandomCountry()
        }

        gameState = .playing
        attempts = 0
        guessResults = []
        guessedCountryIds = []
        searchText = ""
        toastMessage = nil
        gameStartTime = .now
    }

    func selectRandomCountry() {
        let eligible = countries.filter { !recentlyPlayedIso3s.contains($0.iso3) }
        let pool = eligible.isEmpty ? countries : eligible

        guard let country = pool.randomElement() else { return }
        currentCountry = country

        recentlyPlayedIso3s.append(country.iso3)
        if recentlyPlayedIso3s.count > 10 {
            recentlyPlayedIso3s.removeFirst()
        }
    }

    func submitGuess(_ name: String) {
        guard gameState == .playing else { return }
        let trimmed = name.trimmingCharacters(in: .whitespaces)
        guard !trimmed.isEmpty else { return }
        guard let target = currentCountry else { return }

        let guessed = countries.first { country in
            country.displayName(for: language).caseInsensitiveCompare(trimmed) == .orderedSame ||
                country.iso3.caseInsensitiveCompare(trimmed) == .orderedSame
        }

        guard let guessed else {
            toastMessage = language == "no"
                ? "Landet ble ikke funnet. Prøv et annet navn!"
                : "Country not found. Try another name!"
            return
        }

        attempts += 1
        guessedCountryIds.insert(guessed.iso3)

        if guessed.iso3 == target.iso3 {
            let result = GuessResult(
                attemptNumber: attempts,
                countryName: guessed.displayName(for: language),
                isCorrect: true,
                distanceKm: nil,
                direction: nil
            )
            guessResults.insert(result, at: 0)
            endGame(.won)
        } else {
            let dist = HaversineCalculator.distance(
                fromLat: target.centerLat, fromLon: target.centerLon,
                toLat: guessed.centerLat, toLon: guessed.centerLon
            )
            let dir = HaversineCalculator.direction(
                fromLat: target.centerLat, fromLon: target.centerLon,
                toLat: guessed.centerLat, toLon: guessed.centerLon
            )
            let result = GuessResult(
                attemptNumber: attempts,
                countryName: guessed.displayName(for: language),
                isCorrect: false,
                distanceKm: Int(dist),
                direction: dir
            )
            guessResults.insert(result, at: 0)

            if attempts >= maxAttempts {
                endGame(.lost)
            }
        }

        searchText = ""
    }

    func giveUp() {
        guard gameState == .playing else { return }
        endGame(.gaveUp)
    }

    func endGame(_ state: GameState) {
        gameState = state
        saveGameResult()
    }

    func isHintUnlocked(_ hintNumber: Int) -> Bool {
        gameState.isGameOver || attempts >= hintNumber
    }

    func hintRequiredGuesses(_ hintNumber: Int) -> Int {
        hintNumber
    }

    // MARK: - Hint data accessors

    var flagHintData: String? {
        currentCountry?.flagAssetName
    }

    var populationHintData: String? {
        guard let c = currentCountry else { return nil }
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.locale = Locale(identifier: language == "no" ? "nb_NO" : "en_US")
        let formatted = formatter.string(from: NSNumber(value: c.population)) ?? "\(c.population)"
        let label = language == "no" ? "innbyggere" : "inhabitants"
        return "\(formatted) \(label) (\(c.populationYear))"
    }

    var capitalHintData: String? {
        currentCountry?.capital
    }

    var regionHintData: String? {
        currentCountry?.region
    }

    var mountainHintData: String? {
        guard let c = currentCountry else { return nil }
        return "\(c.highestMountain) (\(c.highestElevationMeters)m / \(c.highestElevationFeet)ft)"
    }

    var bordersHintData: String? {
        guard let c = currentCountry else { return nil }
        if c.isIsland {
            return language == "no" ? "Øy (ingen naboland)" : "Island (no borders)"
        }
        let borders = c.displayBorders(for: language)
        return borders.isEmpty ? (language == "no" ? "Ingen data" : "No data") : borders.joined(separator: ", ")
    }

    // MARK: - External links

    func openGoogleMaps() {
        guard let urlString = currentCountry?.googleMapsUrl,
              let url = URL(string: urlString) else { return }
        openURL(url)
    }

    func openNorli() {
        guard let country = currentCountry else { return }
        let name = country.displayName(for: language)
        guard let encoded = name.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed),
              let url = URL(string: "https://www.norli.no/search?query=\(encoded)") else { return }
        openURL(url)
    }

    private func openURL(_ url: URL) {
        UIApplication.shared.open(url)
    }

    // MARK: - Persistence

    private func saveGameResult() {
        guard let context = modelContext, let country = currentCountry else { return }
        let duration = Int(Date.now.timeIntervalSince(gameStartTime))
        let result = GameResult(
            countryIso3: country.iso3,
            countryName: country.displayName(for: language),
            won: gameState == .won,
            gaveUp: gameState == .gaveUp,
            guessCount: attempts,
            hintsRevealed: hintsUnlocked,
            language: language,
            durationSeconds: duration
        )
        context.insert(result)
        try? context.save()
    }
}
