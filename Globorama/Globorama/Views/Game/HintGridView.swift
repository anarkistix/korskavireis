import SwiftUI

struct HintGridView: View {
    let viewModel: GameViewModel

    private let columns = [
        GridItem(.flexible(), spacing: 8),
        GridItem(.flexible(), spacing: 8),
    ]

    var body: some View {
        LazyVGrid(columns: columns, spacing: 8) {
            HintCardView(
                hintNumber: 1,
                emoji: "🏳️",
                title: viewModel.language == "no" ? "Flagg" : "Flag",
                isUnlocked: viewModel.isHintUnlocked(1),
                requiredGuesses: 1,
                language: viewModel.language
            ) {
                if let flagName = viewModel.flagHintData {
                    Image(flagName)
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(maxHeight: 50)
                }
            }

            HintCardView(
                hintNumber: 2,
                emoji: "👥",
                title: viewModel.language == "no" ? "Befolkning" : "Population",
                isUnlocked: viewModel.isHintUnlocked(2),
                requiredGuesses: 2,
                language: viewModel.language
            ) {
                if let data = viewModel.populationHintData {
                    Text(data)
                        .font(.caption)
                        .multilineTextAlignment(.center)
                }
            }

            HintCardView(
                hintNumber: 3,
                emoji: "🏛️",
                title: viewModel.language == "no" ? "Hovedstad" : "Capital",
                isUnlocked: viewModel.isHintUnlocked(3),
                requiredGuesses: 3,
                language: viewModel.language
            ) {
                if let data = viewModel.capitalHintData {
                    Text(data)
                        .font(.subheadline.weight(.medium))
                }
            }

            HintCardView(
                hintNumber: 4,
                emoji: "🌍",
                title: viewModel.language == "no" ? "Region" : "Region",
                isUnlocked: viewModel.isHintUnlocked(4),
                requiredGuesses: 4,
                language: viewModel.language
            ) {
                if let data = viewModel.regionHintData {
                    Text(data)
                        .font(.caption)
                        .multilineTextAlignment(.center)
                }
            }

            HintCardView(
                hintNumber: 5,
                emoji: "⛰️",
                title: viewModel.language == "no" ? "Fjell" : "Mountain",
                isUnlocked: viewModel.isHintUnlocked(5),
                requiredGuesses: 5,
                language: viewModel.language
            ) {
                if let data = viewModel.mountainHintData {
                    Text(data)
                        .font(.caption)
                        .multilineTextAlignment(.center)
                }
            }

            HintCardView(
                hintNumber: 6,
                emoji: "🤝",
                title: viewModel.language == "no" ? "Naboland" : "Neighbors",
                isUnlocked: viewModel.isHintUnlocked(6),
                requiredGuesses: 6,
                language: viewModel.language
            ) {
                if let data = viewModel.bordersHintData {
                    Text(data)
                        .font(.caption)
                        .multilineTextAlignment(.center)
                }
            }
        }
    }
}
