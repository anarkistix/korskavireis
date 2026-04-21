import SwiftUI

struct GameHistoryRow: View {
    let result: GameResult

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

                Text("\(result.guessCount) guess\(result.guessCount == 1 ? "" : "es")")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }
        }
    }

    private var resultBadge: some View {
        Group {
            if result.won {
                Text("Won")
                    .font(.caption2.weight(.bold))
                    .foregroundStyle(Theme.success)
            } else if result.gaveUp {
                Text("Gave up")
                    .font(.caption2.weight(.bold))
                    .foregroundStyle(.orange)
            } else {
                Text("Lost")
                    .font(.caption2.weight(.bold))
                    .foregroundStyle(Theme.error)
            }
        }
    }
}
