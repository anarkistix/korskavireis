import SwiftUI

struct HintGridView: View {
    let viewModel: GameViewModel
    @State private var showFullSilhouette = false

    private let columns = [
        GridItem(.flexible(), spacing: 8),
        GridItem(.flexible(), spacing: 8),
    ]

    var body: some View {
        LazyVGrid(columns: columns, spacing: 8) {
            ForEach(Array(viewModel.currentHintSlots.enumerated()), id: \.offset) { index, slot in
                hintCard(for: slot, hintNumber: index + 1)
            }
        }
        .fullScreenCover(isPresented: $showFullSilhouette) {
            ZStack {
                Color.white.opacity(0.95).ignoresSafeArea()
                if let country = viewModel.currentCountry {
                    Image(country.silhouetteAssetName)
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .padding(32)
                }
            }
            .onTapGesture { showFullSilhouette = false }
        }
    }

    @ViewBuilder
    private func hintCard(for slot: HintSlot, hintNumber: Int) -> some View {
        switch slot {
        case .flag:
            HintCardView(
                hintNumber: hintNumber,
                emoji: "🏳️",
                title: viewModel.language == "no" ? "Flagg" : "Flag",
                isUnlocked: viewModel.isHintUnlocked(hintNumber),
                requiredGuesses: hintNumber,
                language: viewModel.language
            ) {
                if let flagName = viewModel.flagHintData {
                    Image(flagName)
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(maxHeight: 50)
                }
            }

        case .population:
            HintCardView(
                hintNumber: hintNumber,
                emoji: "👥",
                title: viewModel.language == "no" ? "Befolkning" : "Population",
                isUnlocked: viewModel.isHintUnlocked(hintNumber),
                requiredGuesses: hintNumber,
                language: viewModel.language
            ) {
                if let data = viewModel.populationHintData {
                    Text(data)
                        .font(.caption)
                        .multilineTextAlignment(.center)
                }
            }

        case .capital:
            HintCardView(
                hintNumber: hintNumber,
                emoji: "🏛️",
                title: viewModel.language == "no" ? "Hovedstad" : "Capital",
                isUnlocked: viewModel.isHintUnlocked(hintNumber),
                requiredGuesses: hintNumber,
                language: viewModel.language
            ) {
                if let data = viewModel.capitalHintData {
                    Text(data)
                        .font(.subheadline.weight(.medium))
                }
            }

        case .region:
            HintCardView(
                hintNumber: hintNumber,
                emoji: "🌍",
                title: viewModel.language == "no" ? "Region" : "Region",
                isUnlocked: viewModel.isHintUnlocked(hintNumber),
                requiredGuesses: hintNumber,
                language: viewModel.language
            ) {
                if let data = viewModel.regionHintData {
                    Text(data)
                        .font(.caption)
                        .multilineTextAlignment(.center)
                }
            }

        case .mountain:
            HintCardView(
                hintNumber: hintNumber,
                emoji: "⛰️",
                title: viewModel.language == "no" ? "Fjell" : "Mountain",
                isUnlocked: viewModel.isHintUnlocked(hintNumber),
                requiredGuesses: hintNumber,
                language: viewModel.language
            ) {
                if let data = viewModel.mountainHintData {
                    Text(data)
                        .font(.caption)
                        .multilineTextAlignment(.center)
                }
            }

        case .neighbors:
            HintCardView(
                hintNumber: hintNumber,
                emoji: "🤝",
                title: viewModel.language == "no" ? "Naboland" : "Neighbors",
                isUnlocked: viewModel.isHintUnlocked(hintNumber),
                requiredGuesses: hintNumber,
                language: viewModel.language
            ) {
                if let data = viewModel.bordersHintData {
                    Text(data)
                        .font(.caption)
                        .multilineTextAlignment(.center)
                }
            }

        case .silhouette:
            HintCardView(
                hintNumber: hintNumber,
                emoji: "",
                title: viewModel.language == "no" ? "Silhuett" : "Silhouette",
                isUnlocked: viewModel.isHintUnlocked(hintNumber),
                requiredGuesses: hintNumber,
                language: viewModel.language,
                onUnlockedTap: { showFullSilhouette = true }
            ) {
                if let assetName = viewModel.silhouetteHintData {
                    Image(assetName)
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(maxHeight: 60)
                }
            }
        }
    }
}
