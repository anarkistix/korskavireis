import SwiftUI

struct HintCardView<Content: View>: View {
    let hintNumber: Int
    let emoji: String
    let title: String
    let isUnlocked: Bool
    let requiredGuesses: Int
    let language: String
    @ViewBuilder let content: () -> Content

    @State private var showLockMessage = false

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 10)
                .fill(Theme.hintCardBackground)
                .overlay(
                    RoundedRectangle(cornerRadius: 10)
                        .stroke(Theme.hintCardBorder, lineWidth: 1)
                )

            if isUnlocked {
                VStack(spacing: 4) {
                    Text(emoji)
                        .font(.title3)
                    content()
                }
                .padding(8)
                .transition(.scale.combined(with: .opacity))
            } else {
                VStack(spacing: 4) {
                    Image(systemName: "lock.fill")
                        .font(.title3)
                        .foregroundStyle(.white)
                    Text(title)
                        .font(.caption2)
                        .foregroundStyle(.white)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(Color.black.opacity(0.5))
                .clipShape(RoundedRectangle(cornerRadius: 10))
                .onTapGesture {
                    showLockMessage = true
                    DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                        showLockMessage = false
                    }
                }
            }
        }
        .frame(minHeight: 80, idealHeight: 90)
        .animation(.spring(duration: 0.3), value: isUnlocked)
        .sensoryFeedback(.selection, trigger: isUnlocked)
        .overlay {
            if showLockMessage {
                let msg = language == "no"
                    ? "Du må gjette \(requiredGuesses) gang\(requiredGuesses > 1 ? "er" : "") for å låse opp"
                    : "You need to guess \(requiredGuesses) time\(requiredGuesses > 1 ? "s" : "") to unlock"
                Text(msg)
                    .font(.caption2.weight(.medium))
                    .foregroundStyle(.white)
                    .padding(8)
                    .background(Theme.error)
                    .clipShape(RoundedRectangle(cornerRadius: 6))
                    .transition(.opacity)
                    .animation(.easeInOut, value: showLockMessage)
            }
        }
    }
}
