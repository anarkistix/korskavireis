import SwiftUI

struct GuessInputView: View {
    @Bindable var viewModel: GameViewModel
    @FocusState private var isInputFocused: Bool

    var body: some View {
        VStack(spacing: 8) {
            ZStack(alignment: .top) {
                VStack(spacing: 0) {
                    HStack {
                        TextField(
                            viewModel.language == "no"
                                ? "Skriv navn på landet her..."
                                : "Type the country name here...",
                            text: $viewModel.searchText
                        )
                        .focused($isInputFocused)
                        .textInputAutocapitalization(.words)
                        .autocorrectionDisabled()
                        .padding(12)
                        .background(Color(.systemGray6))
                        .clipShape(RoundedRectangle(cornerRadius: 10))
                        .onSubmit {
                            submitCurrentGuess()
                        }
                    }

                    if isInputFocused && !viewModel.filteredCountries.isEmpty {
                        AutocompleteListView(
                            countries: viewModel.filteredCountries,
                            language: viewModel.language,
                            guessedIds: viewModel.guessedCountryIds
                        ) { country in
                            viewModel.searchText = country.displayName(for: viewModel.language)
                            isInputFocused = false
                            viewModel.submitGuess(viewModel.searchText)
                        }
                    }
                }
            }

            HStack(spacing: 12) {
                Button {
                    submitCurrentGuess()
                } label: {
                    Text(viewModel.language == "no" ? "Gjett land" : "Guess country")
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(.white)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                        .background(Theme.purpleGradient)
                        .clipShape(RoundedRectangle(cornerRadius: 10))
                }

                Button {
                    viewModel.giveUp()
                } label: {
                    Text(viewModel.language == "no" ? "Gi opp" : "Give up")
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(.white)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                        .background(Theme.error)
                        .clipShape(RoundedRectangle(cornerRadius: 10))
                }
            }

            Text("\(viewModel.attempts)/\(viewModel.maxAttempts)")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .sensoryFeedback(.error, trigger: viewModel.guessResults.first?.isCorrect == false ? viewModel.attempts : 0)
    }

    private func submitCurrentGuess() {
        isInputFocused = false
        viewModel.submitGuess(viewModel.searchText)
    }
}
