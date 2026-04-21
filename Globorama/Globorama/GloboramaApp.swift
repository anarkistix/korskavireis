import SwiftUI
import SwiftData

@main
struct GloboramaApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: GameResult.self)
    }
}
