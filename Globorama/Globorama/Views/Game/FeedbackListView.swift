import SwiftUI

struct FeedbackListView: View {
    let results: [GuessResult]
    let language: String

    var body: some View {
        if !results.isEmpty {
            VStack(spacing: 8) {
                ForEach(results) { result in
                    FeedbackItemView(result: result, language: language)
                        .transition(.move(edge: .top).combined(with: .opacity))
                }
            }
            .animation(.spring(duration: 0.3), value: results.count)
        }
    }
}
