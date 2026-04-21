import SwiftUI
import SwiftData

struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @State private var gameViewModel: GameViewModel?
    @State private var showStats = false

    var body: some View {
        NavigationStack {
            if let viewModel = gameViewModel {
                GameView(viewModel: viewModel)
                    .toolbar {
                        ToolbarItem(placement: .topBarTrailing) {
                            Button {
                                showStats = true
                            } label: {
                                Image(systemName: "chart.bar.fill")
                                    .foregroundStyle(.white)
                            }
                        }
                    }
                    .sheet(isPresented: $showStats) {
                        StatsView(modelContext: modelContext)
                    }
            } else {
                ProgressView()
            }
        }
        .onAppear {
            if gameViewModel == nil {
                gameViewModel = GameViewModel(modelContext: modelContext)
            }
        }
    }
}
