import SwiftUI

struct CountryBrowserView: View {
    let countries: [Country]
    @Environment(\.dismiss) private var dismiss
    @State private var searchText = ""

    private var filtered: [Country] {
        if searchText.isEmpty { return countries.sorted { $0.name < $1.name } }
        return countries
            .filter {
                $0.name.localizedCaseInsensitiveContains(searchText) ||
                $0.nameNo.localizedCaseInsensitiveContains(searchText) ||
                $0.iso3.localizedCaseInsensitiveContains(searchText)
            }
            .sorted { $0.name < $1.name }
    }

    var body: some View {
        NavigationStack {
            List(filtered) { country in
                NavigationLink {
                    countryDetail(country)
                } label: {
                    HStack(spacing: 12) {
                        Image(country.flagAssetName)
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .frame(width: 30, height: 20)
                            .clipShape(RoundedRectangle(cornerRadius: 2))

                        VStack(alignment: .leading) {
                            Text(country.name)
                                .font(.subheadline.weight(.medium))
                            Text(country.iso3)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
            }
            .searchable(text: $searchText, prompt: "Search countries...")
            .navigationTitle("Countries (\(filtered.count))")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }

    private func countryDetail(_ country: Country) -> some View {
        List {
            Section {
                HStack {
                    Spacer()
                    Image(country.silhouetteAssetName)
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(maxHeight: 200)
                    Spacer()
                }
            }

            Section("Names") {
                row("English", country.name)
                row("Norwegian", country.nameNo)
                row("Original", country.originalName)
                row("ISO3", country.iso3)
            }

            Section("Geography") {
                row("Continent", country.continent)
                row("Region", country.region)
                row("Capital", country.capital)
                row("Center", "\(country.centerLat), \(country.centerLon)")
                row("Island", country.isIsland ? "Yes" : "No")
            }

            Section("Details") {
                row("Population", "\(country.population) (\(country.populationYear))")
                row("Highest Mountain", country.highestMountain)
                row("Elevation", "\(country.highestElevationMeters)m / \(country.highestElevationFeet)ft")
            }

            if !country.borders.isEmpty {
                Section("Borders") {
                    Text(country.borders.joined(separator: ", "))
                        .font(.subheadline)
                }
            }
        }
        .navigationTitle(country.name)
    }

    private func row(_ label: String, _ value: String) -> some View {
        HStack {
            Text(label)
                .foregroundStyle(.secondary)
            Spacer()
            Text(value)
        }
        .font(.subheadline)
    }
}
