import SwiftUI

struct GameView: View {
    @Bindable var viewModel: GameViewModel
    @Binding var showStats: Bool
    @State private var showDevSettings = false
    @State private var versionTapCount = 0

    var body: some View {
        ZStack {
            Theme.teal.ignoresSafeArea()

            ScrollView {
                VStack(spacing: 16) {
                    headerRow
                    gameContent
                    footerView
                }
                .padding(.horizontal)
                .padding(.bottom, 32)
            }

            if let toast = viewModel.toastMessage {
                toastOverlay(toast)
            }
        }
        .sheet(isPresented: $showDevSettings) {
            DevSettingsView(countries: viewModel.countries, language: viewModel.language)
        }
    }

    // MARK: - Header

    private var headerRow: some View {
        HStack {
            languageToggle

            Spacer()

            Text("GLOBORAMA")
                .font(.system(size: 24, weight: .bold, design: .serif))
                .foregroundStyle(Theme.cream)

            Spacer()

            Button {
                showStats = true
            } label: {
                Image(systemName: "chart.bar.fill")
                    .font(.title3)
                    .foregroundStyle(Theme.cream)
            }
        }
        .padding(.horizontal, 4)
        .padding(.top, 8)
    }

    private var languageToggle: some View {
        HStack(spacing: 8) {
            Button {
                viewModel.language = "no"
            } label: {
                Text("🇳🇴")
                    .font(.title3)
                    .opacity(viewModel.language == "no" ? 1.0 : 0.4)
            }
            Button {
                viewModel.language = "en"
            } label: {
                Text("🇬🇧")
                    .font(.title3)
                    .opacity(viewModel.language == "en" ? 1.0 : 0.4)
            }
        }
    }

    // MARK: - Game content

    private var gameContent: some View {
        VStack(spacing: 16) {
            SilhouetteView(country: viewModel.currentCountry)

            if viewModel.gameState.isGameOver {
                GameOverView(viewModel: viewModel)
            } else {
                GuessInputView(viewModel: viewModel)
            }

            HintGridView(viewModel: viewModel)

            FeedbackListView(results: viewModel.guessResults, language: viewModel.language)
        }
        .padding(20)
        .background(.white.opacity(0.95))
        .clipShape(RoundedRectangle(cornerRadius: 20))
    }

    // MARK: - Footer

    private var footerView: some View {
        VStack(spacing: 4) {
            Text(viewModel.language == "no"
                ? "© 2024 KorSkaViReis?"
                : "© 2024 WhereShouldWeGo?")
                .font(.caption2)
                .foregroundStyle(.white.opacity(0.6))

            Text(viewModel.language == "no"
                ? "Bygget med ❤️ av Marius Arnesen"
                : "Built with ❤️ by Marius Arnesen")
                .font(.caption2)
                .foregroundStyle(.white.opacity(0.6))

            Text("v1.0.0")
                .font(.caption2)
                .foregroundStyle(.white.opacity(0.4))
                .onTapGesture {
                    versionTapCount += 1
                    if versionTapCount >= 3 {
                        versionTapCount = 0
                        showDevSettings = true
                    }
                    DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
                        versionTapCount = 0
                    }
                }
        }
        .padding(.top, 8)
    }

    // MARK: - Toast

    private func toastOverlay(_ message: String) -> some View {
        VStack {
            Text(message)
                .font(.subheadline.weight(.medium))
                .foregroundStyle(.white)
                .padding(.horizontal, 20)
                .padding(.vertical, 12)
                .background(Theme.error)
                .clipShape(RoundedRectangle(cornerRadius: 10))
                .shadow(radius: 4)
                .transition(.opacity)
                .onAppear {
                    DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                        withAnimation { viewModel.toastMessage = nil }
                    }
                }

            Spacer()
        }
        .padding(.top, 60)
        .animation(.easeInOut, value: viewModel.toastMessage)
    }
}
