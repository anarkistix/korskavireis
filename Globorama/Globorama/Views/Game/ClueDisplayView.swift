import SwiftUI

struct ClueDisplayView: View {
    let gameMode: GameMode
    let country: Country?
    let language: String

    var body: some View {
        Group {
            if let country {
                switch gameMode {
                case .silhouette:
                    SilhouetteView(country: country)

                case .flag:
                    VStack(spacing: 8) {
                        Text(language == "no" ? "Hvilket land har dette flagget?" : "Which country has this flag?")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                        Image(country.flagAssetName)
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .frame(maxWidth: 300, maxHeight: 200)
                    }
                    .padding(8)

                case .capital:
                    VStack(spacing: 8) {
                        Text(language == "no" ? "Hvilket land har denne hovedstaden?" : "Which country has this capital?")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                        Text(country.capital)
                            .font(.system(size: 32, weight: .bold, design: .serif))
                            .multilineTextAlignment(.center)
                    }
                    .padding(8)

                case .mountain:
                    VStack(spacing: 8) {
                        Text(language == "no" ? "Hvilket land har dette fjellet?" : "Which country has this mountain?")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                        Text(country.highestMountain)
                            .font(.system(size: 28, weight: .bold, design: .serif))
                            .multilineTextAlignment(.center)
                        Text("\(country.highestElevationMeters) m / \(country.highestElevationFeet) ft")
                            .font(.title3)
                            .foregroundStyle(.secondary)
                    }
                    .padding(8)
                }
            } else {
                ProgressView()
                    .frame(height: 200)
            }
        }
        .frame(maxWidth: 350, maxHeight: 250)
    }
}
