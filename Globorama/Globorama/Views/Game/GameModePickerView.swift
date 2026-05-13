import SwiftUI

struct GameModePickerView: View {
    @Bindable var viewModel: GameViewModel
    @Environment(\.dismiss) private var dismiss

    private let columns = [
        GridItem(.flexible(), spacing: 12),
        GridItem(.flexible(), spacing: 12),
    ]

    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Text(viewModel.language == "no" ? "Velg spillmodus" : "Choose Game Mode")
                    .font(.title2.weight(.bold))
                    .padding(.top, 8)

                LazyVGrid(columns: columns, spacing: 12) {
                    ForEach(GameMode.allCases) { mode in
                        modeCard(mode)
                    }
                }
                .padding(.horizontal)

                Spacer()
            }
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button(viewModel.language == "no" ? "Lukk" : "Close") {
                        dismiss()
                    }
                }
            }
        }
    }

    private func modeCard(_ mode: GameMode) -> some View {
        let isSelected = viewModel.gameMode == mode

        return Button {
            viewModel.gameMode = mode
            viewModel.startNewGame()
            dismiss()
        } label: {
            VStack(spacing: 8) {
                Text(mode.emoji)
                    .font(.system(size: 36))

                Text(mode.displayName(for: viewModel.language))
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(isSelected ? .white : .primary)

                Text(mode.clueDescription(for: viewModel.language))
                    .font(.caption2)
                    .foregroundStyle(isSelected ? .white.opacity(0.8) : .secondary)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 16)
            .padding(.horizontal, 8)
            .background(isSelected ? AnyShapeStyle(Theme.purpleGradient) : AnyShapeStyle(Theme.hintCardBackground))
            .clipShape(RoundedRectangle(cornerRadius: 14))
            .overlay(
                RoundedRectangle(cornerRadius: 14)
                    .stroke(isSelected ? .clear : Theme.hintCardBorder, lineWidth: 1)
            )
        }
    }
}
