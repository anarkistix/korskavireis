import SwiftUI
import SwiftData

struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @State private var gameViewModel: GameViewModel?
    @State private var showStats = false

    var body: some View {
        if let viewModel = gameViewModel {
            GameView(viewModel: viewModel, showStats: $showStats)
                .sheet(isPresented: $showStats) {
                    StatsView(modelContext: modelContext, language: viewModel.language)
                }
        } else {
            ProgressView()
                .onAppear {
                    gameViewModel = GameViewModel(modelContext: modelContext)
                }
        }
    }
}
