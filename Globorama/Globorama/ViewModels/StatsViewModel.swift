import Foundation
import Observation
import SwiftData

@Observable
class StatsViewModel {
    var results: [GameResult] = []

    var gamesPlayed: Int { results.count }

    var winRate: Double {
        guard gamesPlayed > 0 else { return 0 }
        return Double(results.filter(\.won).count) / Double(gamesPlayed) * 100
    }

    var averageGuesses: Double {
        let wins = results.filter(\.won)
        guard !wins.isEmpty else { return 0 }
        return Double(wins.map(\.guessCount).reduce(0, +)) / Double(wins.count)
    }

    var currentStreak: Int {
        var streak = 0
        let sorted = results.sorted { $0.date > $1.date }
        for result in sorted {
            if result.won {
                streak += 1
            } else {
                break
            }
        }
        return streak
    }

    var bestStreak: Int {
        var best = 0
        var current = 0
        let sorted = results.sorted { $0.date < $1.date }
        for result in sorted {
            if result.won {
                current += 1
                best = max(best, current)
            } else {
                current = 0
            }
        }
        return best
    }

    var guessDistribution: [Int: Int] {
        var dist: [Int: Int] = [:]
        for result in results where result.won {
            dist[result.guessCount, default: 0] += 1
        }
        return dist
    }

    func loadResults(from context: ModelContext) {
        let descriptor = FetchDescriptor<GameResult>(
            sortBy: [SortDescriptor(\.date, order: .reverse)]
        )
        results = (try? context.fetch(descriptor)) ?? []
    }
}
