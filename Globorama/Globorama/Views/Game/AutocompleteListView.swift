import SwiftUI

struct AutocompleteListView: View {
    let countries: [Country]
    let language: String
    let guessedIds: Set<String>
    let onSelect: (Country) -> Void

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 0) {
                ForEach(countries) { country in
                    let isGuessed = guessedIds.contains(country.iso3)

                    Button {
                        onSelect(country)
                    } label: {
                        HStack {
                            Text(country.displayName(for: language))
                                .font(.subheadline)
                                .foregroundStyle(isGuessed ? .secondary : .primary)

                            Spacer()

                            if isGuessed {
                                Image(systemName: "checkmark")
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 10)
                        .contentShape(Rectangle())
                    }

                    if country.id != countries.last?.id {
                        Divider()
                    }
                }
            }
        }
        .frame(maxHeight: 200)
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 8))
        .shadow(radius: 4)
    }
}
