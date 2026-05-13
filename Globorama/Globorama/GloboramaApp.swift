import SwiftUI
import SwiftData

@main
struct GloboramaApp: App {
    @State private var purchaseManager = PurchaseManager()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(purchaseManager)
        }
        .modelContainer(for: GameResult.self)
    }
}
