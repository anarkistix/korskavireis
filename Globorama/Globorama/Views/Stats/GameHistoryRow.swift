import SwiftUI

struct GameHistoryRow: View {
    let result: GameResult
    let language: String

    var body: some View {
        HStack(spacing: 12) {
            Image("flag-\(result.countryIso3.prefix(2).lowercased())")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(width: 30, height: 20)
                .clipShape(RoundedRectangle(cornerRadius: 2))

            VStack(alignment: .leading, spacing: 2) {
                Text(result.countryName)
                    .font(.subheadline.weight(.medium))

                Text(result.date, style: .date)
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            VStack(alignment: .trailing, spacing: 2) {
                resultBadge

                Text(guessCountText)
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }
        }
    }

    private var guessCountText: String {
        if language == "no" {
            return "\(result.guessCount) gjett"
        }
        return "\(result.guessCount) guess\(result.guessCount == 1 ? "" : "es")"
    }

    private var resultBadge: some View {
        Group {
            if result.won {
                Text(language == "no" ? "Vunnet" : "Won")
                    .font(.caption2.weight(.bold))
                    .foregroundStyle(Theme.success)
            } else if result.gaveUp {
                Text(language == "no" ? "Ga opp" : "Gave up")
                    .font(.caption2.weight(.bold))
                    .foregroundStyle(.orange)
            } else {
                Text(language == "no" ? "Tapte" : "Lost")
                    .font(.caption2.weight(.bold))
                    .foregroundStyle(Theme.error)
            }
        }
    }
}
