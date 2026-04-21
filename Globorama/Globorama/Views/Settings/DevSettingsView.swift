import SwiftUI

struct DevSettingsView: View {
    let countries: [Country]
    let language: String
    @Environment(\.dismiss) private var dismiss
    @AppStorage("gameMode") private var gameMode = "random"
    @AppStorage("specificCountry") private var specificCountry = ""
    @State private var showCountryBrowser = false

    var body: some View {
        NavigationStack {
            List {
                Section(language == "no" ? "Spillmodus" : "Game Mode") {
                    Picker("Mode", selection: $gameMode) {
                        Text(language == "no" ? "Tilfeldig" : "Random").tag("random")
                        Text(language == "no" ? "Spesifikt land" : "Specific Country").tag("specific")
                    }
                    .pickerStyle(.segmented)

                    if gameMode == "specific" {
                        Picker(language == "no" ? "Land" : "Country", selection: $specificCountry) {
                            Text(language == "no" ? "Velg..." : "Select...").tag("")
                            ForEach(countries.sorted { $0.displayName(for: language) < $1.displayName(for: language) }) { country in
                                Text(country.displayName(for: language)).tag(country.name)
                            }
                        }
                    }
                }

                Section(language == "no" ? "Data" : "Data") {
                    Button(language == "no" ? "Bla i land" : "Browse Countries") {
                        showCountryBrowser = true
                    }
                }

                Section(language == "no" ? "Systemstatus" : "System Status") {
                    statusRow(language == "no" ? "Totalt land" : "Total countries", value: "\(countries.count)")
                    statusRow(language == "no" ? "Med silhuetter" : "With silhouettes", value: "\(countries.count)")
                    statusRow(language == "no" ? "Med flagg" : "With flags", value: "\(countries.count)")
                    statusRow(language == "no" ? "Med befolkning" : "With population", value: "\(countries.filter { $0.population > 0 }.count)")
                    statusRow(language == "no" ? "Med hovedstad" : "With capital", value: "\(countries.filter { !$0.capital.isEmpty }.count)")
                    statusRow(language == "no" ? "Med fjell" : "With mountain", value: "\(countries.filter { !$0.highestMountain.isEmpty }.count)")
                    statusRow(language == "no" ? "Øyer" : "Islands", value: "\(countries.filter(\.isIsland).count)")
                }
            }
            .navigationTitle(language == "no" ? "Dev-innstillinger" : "Dev Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button(language == "no" ? "Ferdig" : "Done") { dismiss() }
                }
            }
            .sheet(isPresented: $showCountryBrowser) {
                CountryBrowserView(countries: countries, language: language)
            }
        }
    }

    private func statusRow(_ label: String, value: String) -> some View {
        HStack {
            Text(label)
            Spacer()
            Text(value)
                .foregroundStyle(.secondary)
        }
    }
}
