import SwiftUI

struct PaywallView: View {
    let purchaseManager: PurchaseManager
    let gamesPlayed: Int
    let language: String
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ZStack {
            Theme.teal.ignoresSafeArea()

            ScrollView {
                VStack(spacing: 24) {
                    Spacer().frame(height: 20)

                    Text("🌍")
                        .font(.system(size: 64))

                    Text(language == "no" ? "Ubegrenset Globorama" : "Unlimited Globorama")
                        .font(.title.weight(.bold))
                        .foregroundStyle(Theme.cream)

                    Text(language == "no"
                         ? "Du har spilt \(gamesPlayed) av 10 gratisspill"
                         : "You've played \(gamesPlayed) of 10 free games")
                        .font(.subheadline)
                        .foregroundStyle(.white.opacity(0.9))

                    VStack(alignment: .leading, spacing: 12) {
                        featureRow(icon: "infinity", text: language == "no"
                                   ? "Ubegrenset antall spill"
                                   : "Unlimited games")
                        featureRow(icon: "globe.europe.africa.fill", text: language == "no"
                                   ? "Alle 100+ land"
                                   : "All 100+ countries")
                        featureRow(icon: "chart.bar.fill", text: language == "no"
                                   ? "Full statistikk"
                                   : "Full statistics")
                        featureRow(icon: "heart.fill", text: language == "no"
                                   ? "Støtt en norsk utvikler"
                                   : "Support a Norwegian developer")
                    }
                    .padding(20)
                    .background(.white.opacity(0.15))
                    .clipShape(RoundedRectangle(cornerRadius: 16))

                    Button {
                        Task { await purchaseManager.purchase() }
                    } label: {
                        let price = purchaseManager.product?.displayPrice ?? "kr 59,00"
                        Text(language == "no"
                             ? "Kjøp for \(price)"
                             : "Buy for \(price)")
                            .font(.headline)
                            .foregroundStyle(.white)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 16)
                            .background(Theme.purpleGradient)
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                    }
                    .disabled(purchaseManager.purchaseState == .loading)

                    Button {
                        Task { await purchaseManager.restorePurchases() }
                    } label: {
                        Text(language == "no" ? "Gjenopprett kjøp" : "Restore purchases")
                            .font(.subheadline)
                            .foregroundStyle(.white.opacity(0.8))
                    }

                    if case .error(let message) = purchaseManager.purchaseState {
                        Text(message)
                            .font(.caption)
                            .foregroundStyle(.white)
                            .padding(12)
                            .background(Theme.error.opacity(0.8))
                            .clipShape(RoundedRectangle(cornerRadius: 8))
                    }

                    Spacer().frame(height: 20)
                }
                .padding(.horizontal, 24)
            }

            if purchaseManager.purchaseState == .loading {
                Color.black.opacity(0.3).ignoresSafeArea()
                ProgressView()
                    .tint(.white)
                    .scaleEffect(1.5)
            }
        }
        .onChange(of: purchaseManager.isUnlocked) { _, unlocked in
            if unlocked { dismiss() }
        }
    }

    private func featureRow(icon: String, text: String) -> some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.body)
                .foregroundStyle(Theme.cream)
                .frame(width: 24)
            Text(text)
                .font(.subheadline)
                .foregroundStyle(.white)
        }
    }
}
