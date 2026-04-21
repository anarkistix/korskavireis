import SwiftUI

struct CountryBrowserView: View {
    let countries: [Country]
    let language: String
    @Environment(\.dismiss) private var dismiss
    @State private var searchText = ""

    private var filtered: [Country] {
        if searchText.isEmpty {
            return countries.sorted { $0.displayName(for: language) < $1.displayName(for: language) }
        }
        return countries
            .filter {
                $0.name.localizedCaseInsensitiveContains(searchText) ||
                $0.nameNo.localizedCaseInsensitiveContains(searchText) ||
                $0.iso3.localizedCaseInsensitiveContains(searchText)
            }
            .sorted { $0.displayName(for: language) < $1.displayName(for: language) }
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
                            Text(country.displayName(for: language))
                                .font(.subheadline.weight(.medium))
                            Text(country.iso3)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
            }
            .searchable(text: $searchText, prompt: language == "no" ? "Søk etter land..." : "Search countries...")
            .navigationTitle(language == "no" ? "Land (\(filtered.count))" : "Countries (\(filtered.count))")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button(language == "no" ? "Ferdig" : "Done") { dismiss() }
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

            Section(language == "no" ? "Navn" : "Names") {
                row(language == "no" ? "Engelsk" : "English", country.name)
                row(language == "no" ? "Norsk" : "Norwegian", country.nameNo)
                row(language == "no" ? "Originalt" : "Original", country.originalName)
                row("ISO3", country.iso3)
            }

            Section(language == "no" ? "Geografi" : "Geography") {
                row(language == "no" ? "Kontinent" : "Continent", country.continent)
                row(language == "no" ? "Region" : "Region", country.region)
                row(language == "no" ? "Hovedstad" : "Capital", country.capital)
                row(language == "no" ? "Senter" : "Center", "\(country.centerLat), \(country.centerLon)")
                row(language == "no" ? "Øy" : "Island", country.isIsland ? (language == "no" ? "Ja" : "Yes") : (language == "no" ? "Nei" : "No"))
            }

            Section(language == "no" ? "Detaljer" : "Details") {
                row(language == "no" ? "Befolkning" : "Population", "\(country.population) (\(country.populationYear))")
                row(language == "no" ? "Høyeste fjell" : "Highest Mountain", country.highestMountain)
                row(language == "no" ? "Høyde" : "Elevation", "\(country.highestElevationMeters)m / \(country.highestElevationFeet)ft")
            }

            if !country.borders.isEmpty {
                Section(language == "no" ? "Naboland" : "Borders") {
                    Text(country.displayBorders(for: language).joined(separator: ", "))
                        .font(.subheadline)
                }
            }
        }
        .navigationTitle(country.displayName(for: language))
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
