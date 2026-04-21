# Brainstorm: GLOBORAMA Native iOS App

**Date:** 2026-04-21
**Status:** Complete

## What We're Building

A native iOS (Swift/SwiftUI) port of the GLOBORAMA geography guessing game, currently a vanilla HTML/CSS/JS web app. The app will be distributed via the App Store with a polished native experience.

**Core game:** Player sees a country silhouette, types guesses with autocomplete, receives distance/direction feedback, and unlocks progressive hints (flag, population, capital, region, highest mountain, neighbors). 10 attempts max per round.

### Scope

- Full player-facing game with all 6 hint types
- Bilingual support (Norwegian default, English)
- Admin panel for game control, country data viewer, and system status
- Game statistics and history tracking (new feature not in web version)
- External links to Google Maps and Norli bookstore post-game
- Fully offline — all data bundled in the app

### Out of Scope

- Multiplayer / leaderboards
- Push notifications
- Backend / server component
- iPad-specific layouts (iPhone-first, iPad via compatibility)

## Why This Approach

**Architecture: SwiftUI + MVVM + SwiftData**

The existing web architecture (single `GeographyGame` class with all state and logic) maps cleanly to a SwiftUI MVVM pattern:

| Web (JS) | iOS (Swift) |
|-----------|-------------|
| `GeographyGame` class | `GameViewModel` (ObservableObject) |
| DOM manipulation | SwiftUI declarative views |
| `localStorage` | `@AppStorage` / SwiftData |
| `fetch()` JSON | Bundle JSON decoded via `Codable` |
| `translations.json` | `Localizable.xcstrings` (String Catalogs) |
| CSS responsive layout | SwiftUI adaptive layout |

**Why SwiftUI over UIKit:** Modern declarative approach, less boilerplate, state management aligns with the reactive pattern the game needs (hints unlocking, feedback appearing, game state transitions).

**Why SwiftData over UserDefaults/Core Data:** Game history with queryable stats (win rate, streaks, average guesses) needs a proper persistence layer. SwiftData is the modern choice for iOS 17+ and requires minimal boilerplate.

**Why pre-compute country centers:** The 18MB JSON files embed full GeoJSON geometry solely to calculate country center coordinates at runtime. Pre-computing these into simple lat/lon fields and stripping geometry reduces data to ~1MB — critical for App Store bundle size.

## Key Decisions

1. **SwiftUI + MVVM architecture** — `GameViewModel` as the central ObservableObject driving all game state
2. **SwiftData for persistence** — Game history, stats, and settings
3. **iOS 17+ minimum target** — Required for SwiftData, covers ~85% of active devices
4. **Pre-computed country centers** — Strip GeoJSON geometry, add `centerLat`/`centerLon` fields to data
5. **Full port including admin panel** — Settings screen with game mode control, country data browser, system status
6. **Bilingual via String Catalogs** — Native iOS localization (NO/EN) replacing `translations.json`
7. **New feature: game statistics** — Games played, win rate, average guesses, streak, plus scrollable game history
8. **Keep external links** — Google Maps and Norli bookstore open in Safari/Maps post-game
9. **Asset Catalog for images** — 192 silhouettes + 254 flags bundled as image assets

## App Structure (Proposed)

```
Globorama/
├── GloboramaApp.swift              # App entry point
├── Models/
│   ├── Country.swift               # Codable country model
│   ├── GameResult.swift            # SwiftData model for game history
│   └── GameState.swift             # Enum: playing, won, lost
├── ViewModels/
│   ├── GameViewModel.swift         # Core game logic (port of GeographyGame)
│   └── StatsViewModel.swift        # Stats computation from game history
├── Views/
│   ├── GameView.swift              # Main game screen
│   ├── SilhouetteView.swift        # Country image display
│   ├── HintCardsView.swift         # Horizontal scrolling hint row
│   ├── GuessInputView.swift        # Text field + autocomplete
│   ├── FeedbackListView.swift      # Guess results with distance/direction
│   ├── GameOverView.swift          # Results, links, new game button
│   ├── StatsView.swift             # Statistics and game history
│   └── AdminView.swift             # Settings/admin panel
├── Utilities/
│   ├── HaversineCalculator.swift   # Distance + direction calculation
│   └── CountryDataLoader.swift     # JSON bundle loading
├── Resources/
│   ├── countries_en.json           # Optimized English data (~500KB)
│   ├── countries_no.json           # Optimized Norwegian data (~500KB)
│   └── Localizable.xcstrings       # UI strings (NO/EN)
└── Assets.xcassets/
    ├── CountrySilhouettes/         # 192 PNGs
    ├── Flags/                      # 254 PNGs
    └── AppIcon                     # App icon
```

## Data Model Mapping

### Country (from JSON, read-only)

```swift
struct Country: Codable, Identifiable {
    let id: String              // iso3
    let name: String
    let nameNo: String?         // Norwegian name (only in NO data)
    let originalName: String
    let iso3: String
    let continent: String
    let region: String
    let centerLat: Double       // Pre-computed from geometry
    let centerLon: Double       // Pre-computed from geometry
    let flagFile: String
    let imageFile: String
    let population: Int
    let populationYear: Int
    let googleMapsUrl: String
    let capital: String
    let capitalLat: Double
    let capitalLon: Double
    let highestMountain: String
    let highestElevationMeters: Int
    let highestElevationFeet: Int
    let borders: [String]
    let bordersNo: [String]?
    let isIsland: Bool
}
```

### GameResult (SwiftData, persisted)

```swift
@Model
class GameResult {
    var countryName: String
    var countryIso3: String
    var won: Bool
    var guessCount: Int
    var date: Date
    var language: String        // "no" or "en"
}
```

## UI Design Notes

- Adapt the existing teal/purple color scheme to iOS
- Use system fonts (San Francisco) rather than web fonts
- Hint cards: horizontal `ScrollView` with `.scrollTargetBehavior(.viewAligned)`
- Autocomplete: custom overlay list below text field
- Feedback items: `List` or `LazyVStack` with slide-in animation
- Haptic feedback on correct guess and hint unlock
- Support Dynamic Type for accessibility

## Open Questions

*None — all questions resolved during brainstorm.*

## Resolved Questions

1. **Motivation:** App Store presence + better mobile experience
2. **UI Framework:** SwiftUI (modern, declarative, fits the reactive game pattern)
3. **Architecture:** MVVM + SwiftData
4. **iOS target:** 17+
5. **Scope:** Full port including admin + new stats feature
6. **Data strategy:** Pre-compute centers, strip geometry
7. **External links:** Keep both Google Maps and Norli
