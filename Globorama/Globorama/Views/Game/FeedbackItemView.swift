import SwiftUI

struct FeedbackItemView: View {
    let result: GuessResult
    let language: String

    var body: some View {
        HStack(spacing: 12) {
            Text("\(result.attemptNumber)")
                .font(.caption.weight(.bold))
                .foregroundStyle(.white)
                .frame(width: 28, height: 28)
                .background(result.isCorrect ? Theme.success : Theme.purpleStart)
                .clipShape(Circle())

            if result.isCorrect {
                HStack(spacing: 4) {
                    Text("🎉")
                    Text(result.countryName)
                        .font(.subheadline.weight(.semibold))
                    Text(language == "no" ? "RIKTIG" : "CORRECT")
                        .font(.caption.weight(.bold))
                        .foregroundStyle(Theme.success)
                    Text("🎉")
                }
            } else {
                VStack(alignment: .leading, spacing: 2) {
                    Text(result.countryName)
                        .font(.subheadline.weight(.medium))

                    if let distance = result.distanceKm, let dir = result.direction {
                        HStack(spacing: 4) {
                            Text(dir.emoji)
                                .font(.caption)
                            Text("\(distance) km \(dir.localizedName(for: language))")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
            }

            Spacer()
        }
        .padding(10)
        .background(result.isCorrect
            ? Color.green.opacity(0.1)
            : Color(.systemGray6))
        .clipShape(RoundedRectangle(cornerRadius: 10))
    }
}
