import Foundation
import SwiftData

@Model
class GameResult {
    var countryIso3: String
    var countryName: String
    var won: Bool
    var gaveUp: Bool
    var guessCount: Int
    var hintsRevealed: Int
    var date: Date
    var language: String
    var durationSeconds: Int

    init(
        countryIso3: String,
        countryName: String,
        won: Bool,
        gaveUp: Bool,
        guessCount: Int,
        hintsRevealed: Int,
        date: Date = .now,
        language: String,
        durationSeconds: Int
    ) {
        self.countryIso3 = countryIso3
        self.countryName = countryName
        self.won = won
        self.gaveUp = gaveUp
        self.guessCount = guessCount
        self.hintsRevealed = hintsRevealed
        self.date = date
        self.language = language
        self.durationSeconds = durationSeconds
    }
}
