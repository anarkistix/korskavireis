import SwiftUI

struct GameOverView: View {
    let viewModel: GameViewModel

    var body: some View {
        VStack(spacing: 16) {
            if let country = viewModel.currentCountry {
                VStack(spacing: 8) {
                    Text(viewModel.gameState == .won ? "🎉" : "🌍")
                        .font(.largeTitle)

                    Text(country.displayName(for: viewModel.language))
                        .font(.title2.weight(.bold))
                        .foregroundStyle(.white)
                        .padding(.horizontal, 24)
                        .padding(.vertical, 12)
                        .background(Theme.purpleGradient)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        .transition(.scale)
                }
                .sensoryFeedback(.success, trigger: viewModel.gameState == .won)
            }

            VStack(spacing: 10) {
                Button {
                    viewModel.startNewGame()
                } label: {
                    Label(
                        viewModel.language == "no" ? "Gi meg et nytt land" : "Give me a new country",
                        systemImage: "arrow.clockwise"
                    )
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(.white)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 12)
                    .background(Theme.purpleGradient)
                    .clipShape(RoundedRectangle(cornerRadius: 10))
                }

                HStack(spacing: 10) {
                    Button {
                        viewModel.openGoogleMaps()
                    } label: {
                        Label(
                            viewModel.language == "no" ? "Google Maps" : "Google Maps",
                            systemImage: "map.fill"
                        )
                        .font(.caption.weight(.medium))
                        .foregroundStyle(.white)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 10)
                        .background(Theme.info)
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                    }

                    Button {
                        viewModel.openNorli()
                    } label: {
                        Label("Norli", systemImage: "book.fill")
                            .font(.caption.weight(.medium))
                            .foregroundStyle(.white)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 10)
                            .background(Theme.darkTeal)
                            .clipShape(RoundedRectangle(cornerRadius: 8))
                    }
                }
            }
        }
    }
}
