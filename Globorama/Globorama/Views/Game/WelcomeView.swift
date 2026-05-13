import SwiftUI

struct WelcomeView: View {
    @Bindable var viewModel: GameViewModel

    private let columns = [
        GridItem(.flexible(), spacing: 12),
        GridItem(.flexible(), spacing: 12),
    ]

    var body: some View {
        ZStack {
            Theme.darkTeal.ignoresSafeArea()

            ScrollView {
                VStack(spacing: 24) {
                    header
                    howToPlay
                    modeSelection
                }
                .padding(.horizontal, 24)
                .padding(.vertical, 32)
            }
        }
    }

    private var header: some View {
        VStack(spacing: 8) {
            Text("GLOBORAMA")
                .font(.system(size: 36, weight: .bold, design: .serif))
                .foregroundStyle(Theme.cream)

            Text(viewModel.language == "no"
                ? "Geografispillet"
                : "The Geography Game")
                .font(.title3)
                .foregroundStyle(Theme.cream.opacity(0.7))
        }
        .padding(.top, 16)
    }

    private var howToPlay: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(viewModel.language == "no" ? "Slik spiller du" : "How to play")
                .font(.headline.weight(.bold))
                .foregroundStyle(.primary)

            let steps: [(String, String)] = viewModel.language == "no"
                ? [
                    ("1.", "Du får en ledetråd — et omriss, flagg, hovedstad eller fjell"),
                    ("2.", "Gjett hvilket land det er. Du har 10 forsøk"),
                    ("3.", "For hvert feilsvar får du avstand og retning"),
                    ("4.", "Nye hint låses opp etter hvert forsøk"),
                ]
                : [
                    ("1.", "You get a clue — a silhouette, flag, capital or mountain"),
                    ("2.", "Guess which country it is. You have 10 attempts"),
                    ("3.", "Wrong answers show distance and direction"),
                    ("4.", "New hints unlock with each attempt"),
                ]

            ForEach(steps, id: \.0) { step in
                HStack(alignment: .top, spacing: 8) {
                    Text(step.0)
                        .font(.subheadline.weight(.bold).monospacedDigit())
                        .foregroundStyle(Theme.purpleStart)
                    Text(step.1)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
            }
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(.white.opacity(0.95))
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }

    private var modeSelection: some View {
        VStack(spacing: 16) {
            Text(viewModel.language == "no" ? "Velg spillmodus" : "Choose game mode")
                .font(.headline.weight(.bold))
                .foregroundStyle(Theme.cream)

            LazyVGrid(columns: columns, spacing: 12) {
                ForEach(GameMode.allCases) { mode in
                    modeCard(mode)
                }
            }
        }
    }

    private func modeCard(_ mode: GameMode) -> some View {
        Button {
            viewModel.gameMode = mode
            viewModel.startNewGame()
            viewModel.showWelcomeScreen = false
        } label: {
            VStack(spacing: 8) {
                Text(mode.emoji)
                    .font(.system(size: 36))

                Text(mode.displayName(for: viewModel.language))
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(.primary)

                Text(mode.clueDescription(for: viewModel.language))
                    .font(.caption2)
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 16)
            .padding(.horizontal, 8)
            .background(.white.opacity(0.95))
            .clipShape(RoundedRectangle(cornerRadius: 14))
        }
    }
}
