#if DEBUG
import SwiftUI
import SwiftData

struct DevSettingsView: View {
    let countries: [Country]
    let language: String
    let purchaseManager: PurchaseManager
    @Environment(\.dismiss) private var dismiss
    @Environment(\.modelContext) private var modelContext
    @AppStorage("debugCountryMode") private var debugCountryMode = "random"
    @AppStorage("specificCountry") private var specificCountry = ""
    @State private var showCountryBrowser = false
    @State private var gameCount: Int = 0

    var body: some View {
        NavigationStack {
            List {
                Section(language == "no" ? "Spillmodus" : "Game Mode") {
                    Picker("Mode", selection: $debugCountryMode) {
                        Text(language == "no" ? "Tilfeldig" : "Random").tag("random")
                        Text(language == "no" ? "Spesifikt land" : "Specific Country").tag("specific")
                    }
                    .pickerStyle(.segmented)

                    if debugCountryMode == "specific" {
                        Picker(language == "no" ? "Land" : "Country", selection: $specificCountry) {
                            Text(language == "no" ? "Velg..." : "Select...").tag("")
                            ForEach(countries.sorted { $0.displayName(for: language) < $1.displayName(for: language) }) { country in
                                Text(country.displayName(for: language)).tag(country.name)
                            }
                        }
                    }
                }

                Section("In-App Purchase") {
                    HStack {
                        Text("Games played")
                        Spacer()
                        Text("\(gameCount) / 10")
                            .foregroundStyle(.secondary)
                    }

                    HStack {
                        Text("Unlocked")
                        Spacer()
                        Text(purchaseManager.isUnlocked ? "Yes" : "No")
                            .foregroundStyle(purchaseManager.isUnlocked ? .green : .secondary)
                    }

                    HStack {
                        Text("Product loaded")
                        Spacer()
                        Text(purchaseManager.product != nil
                             ? (purchaseManager.product!.displayPrice)
                             : "No")
                            .foregroundStyle(purchaseManager.product != nil ? .green : .red)
                    }

                    if case .error(let msg) = purchaseManager.purchaseState {
                        HStack {
                            Text("Error")
                            Spacer()
                            Text(msg)
                                .foregroundStyle(.red)
                                .font(.caption)
                        }
                    }

                    Button("Reload product") {
                        Task { await purchaseManager.loadProduct() }
                    }

                    Button("Reset game counter (delete all results)", role: .destructive) {
                        do {
                            try modelContext.delete(model: GameResult.self)
                            try modelContext.save()
                            gameCount = 0
                        } catch {}
                    }

                    Button("Reset purchase unlock", role: .destructive) {
                        purchaseManager.resetPurchase()
                    }

                    Button("Manage Sandbox Account") {
                        if let url = URL(string: "itms-ui://") {
                            UIApplication.shared.open(url)
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
            .onAppear {
                let descriptor = FetchDescriptor<GameResult>()
                gameCount = (try? modelContext.fetchCount(descriptor)) ?? 0
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
#endif
