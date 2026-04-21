import SwiftUI

struct DevSettingsView: View {
    let countries: [Country]
    @Environment(\.dismiss) private var dismiss
    @AppStorage("gameMode") private var gameMode = "random"
    @AppStorage("specificCountry") private var specificCountry = ""
    @State private var showCountryBrowser = false

    var body: some View {
        NavigationStack {
            List {
                Section("Game Mode") {
                    Picker("Mode", selection: $gameMode) {
                        Text("Random").tag("random")
                        Text("Specific Country").tag("specific")
                    }
                    .pickerStyle(.segmented)

                    if gameMode == "specific" {
                        Picker("Country", selection: $specificCountry) {
                            Text("Select...").tag("")
                            ForEach(countries.sorted { $0.name < $1.name }) { country in
                                Text(country.name).tag(country.name)
                            }
                        }
                    }
                }

                Section("Data") {
                    Button("Browse Countries") {
                        showCountryBrowser = true
                    }
                }

                Section("System Status") {
                    statusRow("Total countries", value: "\(countries.count)")
                    statusRow("With silhouettes", value: "\(countries.count)")
                    statusRow("With flags", value: "\(countries.count)")
                    statusRow("With population", value: "\(countries.filter { $0.population > 0 }.count)")
                    statusRow("With capital", value: "\(countries.filter { !$0.capital.isEmpty }.count)")
                    statusRow("With mountain", value: "\(countries.filter { !$0.highestMountain.isEmpty }.count)")
                    statusRow("Islands", value: "\(countries.filter(\.isIsland).count)")
                }
            }
            .navigationTitle("Dev Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") { dismiss() }
                }
            }
            .sheet(isPresented: $showCountryBrowser) {
                CountryBrowserView(countries: countries)
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
