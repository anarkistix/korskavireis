import SwiftUI
import SwiftData

struct StatsView: View {
    let modelContext: ModelContext
    @State private var viewModel = StatsViewModel()
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Group {
                if viewModel.gamesPlayed == 0 {
                    emptyState
                } else {
                    statsContent
                }
            }
            .navigationTitle("Statistics")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") { dismiss() }
                }
            }
        }
        .onAppear {
            viewModel.loadResults(from: modelContext)
        }
    }

    private var emptyState: some View {
        VStack(spacing: 16) {
            Text("🌍")
                .font(.system(size: 60))
            Text("No games played yet")
                .font(.title3.weight(.medium))
            Text("Start playing to see your statistics!")
                .font(.subheadline)
                .foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private var statsContent: some View {
        List {
            Section("Overview") {
                statsGrid
            }

            Section("Guess Distribution") {
                guessDistributionChart
            }

            Section("History") {
                ForEach(viewModel.results, id: \.persistentModelID) { result in
                    GameHistoryRow(result: result)
                }
            }
        }
    }

    private var statsGrid: some View {
        LazyVGrid(columns: [
            GridItem(.flexible()),
            GridItem(.flexible()),
        ], spacing: 12) {
            statCard(value: "\(viewModel.gamesPlayed)", label: "Played")
            statCard(value: String(format: "%.0f%%", viewModel.winRate), label: "Win Rate")
            statCard(value: String(format: "%.1f", viewModel.averageGuesses), label: "Avg Guesses")
            statCard(value: "\(viewModel.currentStreak)", label: "Streak")
        }
    }

    private func statCard(value: String, label: String) -> some View {
        VStack(spacing: 4) {
            Text(value)
                .font(.title2.weight(.bold))
                .foregroundStyle(Theme.purpleStart)
            Text(label)
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 8)
    }

    private var guessDistributionChart: some View {
        VStack(alignment: .leading, spacing: 4) {
            let dist = viewModel.guessDistribution
            let maxCount = dist.values.max() ?? 1

            ForEach(1...10, id: \.self) { guessCount in
                let count = dist[guessCount] ?? 0

                HStack(spacing: 8) {
                    Text("\(guessCount)")
                        .font(.caption.monospacedDigit())
                        .frame(width: 20, alignment: .trailing)

                    GeometryReader { geo in
                        let width = maxCount > 0
                            ? max(CGFloat(count) / CGFloat(maxCount) * geo.size.width, count > 0 ? 20 : 0)
                            : 0

                        RoundedRectangle(cornerRadius: 3)
                            .fill(Theme.purpleGradient)
                            .frame(width: width)
                            .overlay(alignment: .trailing) {
                                if count > 0 {
                                    Text("\(count)")
                                        .font(.caption2.weight(.bold))
                                        .foregroundStyle(.white)
                                        .padding(.trailing, 4)
                                }
                            }
                    }
                    .frame(height: 18)
                }
            }
        }
    }
}
