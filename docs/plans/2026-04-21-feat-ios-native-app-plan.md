---
title: "feat: Convert GLOBORAMA to Native iOS App"
type: feat
status: active
date: 2026-04-21
origin: docs/brainstorms/2026-04-21-ios-native-app-brainstorm.md
---

# feat: Convert GLOBORAMA to Native iOS App

## Overview

Port the GLOBORAMA geography guessing game from a vanilla HTML/CSS/JS web app to a native iOS app using SwiftUI, MVVM architecture, and SwiftData. The app will be distributed via the App Store targeting iOS 17+. All 192 countries, 6 progressive hints, bilingual support (NO/EN), and a hidden admin panel will be ported. A new game statistics and history feature will be added.

## Problem Statement

GLOBORAMA currently runs as a client-side web app hosted on GitHub Pages. While functional, the mobile web experience lacks native feel — no haptic feedback, no persistent stats, no App Store discoverability, and the browser chrome consumes screen real estate. Converting to a native iOS app addresses both distribution (App Store presence) and UX (native interactions, offline-first, smooth animations).

## Proposed Solution

A SwiftUI app using the `@Observable` macro (iOS 17+) with MVVM architecture. The existing `GeographyGame` JavaScript class (1781 lines, 47 methods) maps to a `GameViewModel`. Country data is pre-processed to strip GeoJSON geometry (~18MB → ~1MB), bundled as JSON, and decoded via `Codable`. Game history is persisted with SwiftData. Localization uses String Catalogs.

(see brainstorm: `docs/brainstorms/2026-04-21-ios-native-app-brainstorm.md`)

## Technical Approach

### Architecture

```
┌─────────────────────────────────────────────────┐
│                  GloboramaApp                    │
│              (App entry + ModelContainer)         │
├─────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────────┐  ┌──────────────┐              │
│  │  GameViewModel│  │ StatsViewModel│              │
│  │  (@Observable)│  │ (@Observable) │              │
│  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                      │
│  ┌──────┴──────────────────┴───────┐             │
│  │           SwiftUI Views          │             │
│  │  GameView · HintCards · Input    │             │
│  │  Feedback · GameOver · Stats     │             │
│  └──────────────────────────────────┘             │
│                                                   │
│  ┌──────────────────────────────────┐             │
│  │         Data Layer               │             │
│  │  Country (Codable, bundled JSON) │             │
│  │  GameResult (@Model, SwiftData)  │             │
│  │  Settings (@AppStorage)          │             │
│  └──────────────────────────────────┘             │
└─────────────────────────────────────────────────┘
```

**Key architectural decisions (from brainstorm):**

| Web (JS) | iOS (Swift) | Rationale |
|-----------|-------------|-----------|
| `GeographyGame` class | `GameViewModel` (`@Observable`) | Granular view updates, no `@Published` boilerplate |
| `localStorage` | `@AppStorage` + SwiftData | Simple prefs via `@AppStorage`, history via SwiftData |
| `fetch()` JSON | `Bundle.main.url` + `JSONDecoder` | Bundled data, no network needed |
| `translations.json` | `Localizable.xcstrings` | Native iOS localization with auto-discovery |
| DOM manipulation | SwiftUI declarative views | Reactive UI matching game state transitions |
| `window.postMessage` (admin) | In-app navigation | No cross-window communication needed |

### File Structure

```
Globorama/
├── GloboramaApp.swift                  # @main, ModelContainer setup
├── Models/
│   ├── Country.swift                   # Codable struct from bundled JSON
│   ├── GameResult.swift                # @Model for SwiftData persistence
│   └── GameState.swift                 # Enum: .playing, .won, .lost, .gaveUp
├── ViewModels/
│   ├── GameViewModel.swift             # Core game logic (port of GeographyGame)
│   └── StatsViewModel.swift            # Computed stats from GameResult queries
├── Views/
│   ├── ContentView.swift               # Root view with NavigationStack
│   ├── Game/
│   │   ├── GameView.swift              # Main game screen composition
│   │   ├── SilhouetteView.swift        # Country image display
│   │   ├── HintGridView.swift          # 2x3 grid of hint cards
│   │   ├── HintCardView.swift          # Single hint card (locked/unlocked)
│   │   ├── GuessInputView.swift        # TextField + autocomplete overlay
│   │   ├── AutocompleteListView.swift  # Suggestion dropdown
│   │   ├── FeedbackListView.swift      # Scrollable guess results
│   │   ├── FeedbackItemView.swift      # Single guess result row
│   │   └── GameOverView.swift          # Results, links, new game
│   ├── Stats/
│   │   ├── StatsView.swift             # Statistics dashboard
│   │   └── GameHistoryRow.swift        # Single history entry
│   └── Settings/
│       ├── DevSettingsView.swift        # Hidden admin panel
│       └── CountryBrowserView.swift     # Country data viewer
├── Utilities/
│   ├── HaversineCalculator.swift       # Distance + 8-point compass direction
│   ├── CountryDataLoader.swift         # JSON bundle loading + decoding
│   └── Theme.swift                     # Color constants, shared styling
├── Resources/
│   ├── countries.json                  # Unified, optimized country data (~1MB)
│   └── Localizable.xcstrings           # String Catalog (NO/EN, ~80 keys)
├── Assets.xcassets/
│   ├── AppIcon.appiconset/             # 1024x1024 app icon
│   ├── Colors/                         # Named colors (Teal, DarkTeal, Purple, etc.)
│   ├── Silhouettes/                    # 192 country silhouette PNGs
│   └── Flags/                          # 254 country flag PNGs
├── Preview Content/
│   └── PreviewData.swift               # Sample countries for SwiftUI previews
└── Scripts/
    └── prepare_ios_data.py             # One-time script: strip geometry, merge JSONs
```

### Data Models

#### Country.swift (Codable, read-only, loaded from bundle)

```swift
struct Country: Codable, Identifiable, Hashable {
    var id: String { iso3 }
    let name: String
    let nameNo: String
    let originalName: String
    let iso3: String
    let continent: String
    let region: String
    let centerLat: Double
    let centerLon: Double
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
    let bordersNo: [String]
    let isIsland: Bool

    var displayName: String {
        // Returns name based on current locale
    }
}
```

**Data changes from web version:**
- `geometry` field **removed** — centers pre-computed into `centerLat`/`centerLon`
- `capital_coordinates` flattened into `capitalLat`/`capitalLon`
- `nameNo` required (not optional) — sourced from `countries_data_no.json`
- `bordersNo` populated for all 155 non-island countries (currently empty in web data — needs manual population or kept as English fallback)
- `iso_code` (2-letter) dropped — unused in game logic
- Keys converted to camelCase for Swift `Codable` conventions

#### GameResult.swift (SwiftData, persisted)

```swift
import SwiftData

@Model
class GameResult {
    var countryIso3: String
    var countryName: String
    var won: Bool
    var gaveUp: Bool
    var guessCount: Int
    var hintsRevealed: Int          // 0-6, how many hints were unlocked
    var date: Date
    var language: String            // "no" or "en"
    var durationSeconds: Int        // time from game start to end

    init(countryIso3: String, countryName: String, won: Bool,
         gaveUp: Bool, guessCount: Int, hintsRevealed: Int,
         date: Date, language: String, durationSeconds: Int) {
        self.countryIso3 = countryIso3
        self.countryName = countryName
        self.won = won
        self.gaveUp = gaveUp
        self.guessCount = guessCount
        self.hintsRevealed = hintsRevealed
        self.date = date
        self.language = language
        self.durationSeconds = durationSeconds
    }
}
```

#### GameState.swift

```swift
enum GameState: Equatable {
    case playing
    case won
    case lost       // exhausted 10 attempts
    case gaveUp
}
```

### Game Logic Port

The `GameViewModel` ports all 47 methods from `GeographyGame`. Key mappings:

| JS Method | Swift Method | Notes |
|-----------|-------------|-------|
| `init()` | `init(modelContext:)` | Load countries, restore language |
| `loadCountries()` | `loadCountries()` | Decode from `Bundle.main`, no geometry |
| `startNewGame()` | `startNewGame()` | Reset state, select country, exclude last 10 played |
| `selectRandomCountry()` | `selectRandomCountry()` | Filter out recently played |
| `submitGuess()` | `submitGuess(_ name: String)` | Match by name or ISO3, case-insensitive |
| `calculateDistance()` | `HaversineCalculator.distance()` | Static utility, returns km |
| `getDirection()` | `HaversineCalculator.direction()` | Returns `CompassDirection` enum |
| `checkAndUnlockHints()` | `unlockAvailableHints()` | Updates `@Observable` hint state |
| `showHint()` ... `showBordersHint()` | Computed properties on ViewModel | SwiftUI reads hint data reactively |
| `endGame(won)` | `endGame(_ state: GameState)` | Unified: always reveals all hints (fixes web bug) |
| `giveUp()` | `giveUp()` | Calls `endGame(.gaveUp)` |
| `revealAllHints()` | Automatic via `gameState` change | SwiftUI reacts to state, no manual DOM manipulation |
| `showSuggestions(query)` | `filteredCountries` computed property | Substring match, sorted, max 10 |
| `switchLanguage(lang)` | `setLanguage(_ lang: String)` | Updates `@AppStorage`, recomputes display names |
| `updateStats()` | `StatsViewModel` queries SwiftData | Separate ViewModel for stats screen |
| `scrollToMapTop()` | Not needed | SwiftUI handles scroll position naturally |

**Bug fix from web:** `endGame(false)` in the web version does NOT reveal hints or show the country reveal box (see `main.js:1043-1070`). The iOS version unifies all three end states to always reveal everything.

**New behavior:** Exclude the last 10 played countries from random selection to prevent repeats.

### Hint System

6 progressive hints, unlocked after N wrong guesses:

| # | Hint | Unlocks After | Data Source | Display |
|---|------|--------------|-------------|---------|
| 1 | Flag | 1 guess | `flagFile` → Asset Catalog | Flag image |
| 2 | Population | 2 guesses | `population` + `populationYear` | "114,535,772 (2023)" |
| 3 | Capital | 3 guesses | `capital` | "Cairo" |
| 4 | Region | 4 guesses | `region` | "Northern Africa" |
| 5 | Mountain | 5 guesses | `highestMountain` + elevations | "Mount Catherine (2629m / 8625ft)" |
| 6 | Borders | 6 guesses | `borders`/`bordersNo` or `isIsland` | "Israel, Libya, Sudan" or "Island (no borders)" |

**iOS layout:** 2 columns × 3 rows grid (not horizontal scroll like web). Each card shows:
- **Locked:** Dark overlay with lock icon, emoji label, hint name. Tapping shows toast with required guess count.
- **Unlocked:** Hint content replaces the lock overlay with a reveal animation.

### Autocomplete

Custom SwiftUI component (`GuessInputView` + `AutocompleteListView`):

- **Trigger:** 1 character minimum (matching web behavior)
- **Matching:** Substring match on country name AND ISO3 code (case-insensitive)
- **Sorting:** Prefix matches first, then substring-only matches, alphabetical within each group
- **Max results:** 10
- **Already-guessed countries:** Dimmed in the list with a checkmark, still selectable
- **Keyboard:** Dismissed on guess submission and on tapping a suggestion
- **Scroll behavior:** Max height ~200pt, scrollable

### Navigation

```swift
enum AppRoute: Hashable {
    case game
    case stats
    case devSettings
    case countryBrowser
}
```

Simple `NavigationStack` — the game is the root. Stats accessible via toolbar button. Dev settings accessible via triple-tap on version label in a sheet.

### Localization

**String Catalog (`Localizable.xcstrings`)** with ~80 keys:

- 49 existing keys from `translations.json` (ported directly)
- ~15 new keys for stats screen (games played, win rate, average guesses, streak, history header, empty state)
- ~10 new keys for settings/admin (game mode, language, country browser)
- ~6 new keys for accessibility labels

**Development language:** Norwegian (nb). English added as localization target.

All `Text()` views use string literals that Xcode auto-discovers into the catalog.

### Styling and Theme

`Theme.swift` defines named constants matching the web design:

```swift
enum Theme {
    static let teal = Color("Teal")                // #379490
    static let darkTeal = Color("DarkTeal")        // #175157
    static let cream = Color("Cream")              // #faf4d0
    static let purpleStart = Color("PurpleStart")  // #667eea
    static let purpleEnd = Color("PurpleEnd")      // #764ba2
    static let success = Color("Success")          // #28a745
    static let error = Color("Error")              // #dc3545
    static let info = Color("Info")                // #17a2b8

    static let purpleGradient = LinearGradient(
        colors: [purpleStart, purpleEnd],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )
}
```

**Typography:** San Francisco (system default). No custom fonts needed.

**Animations:**
- Feedback items: `.transition(.move(edge: .top).combined(with: .opacity))`
- Hint unlock: `.transition(.scale.combined(with: .opacity))`
- Country reveal: `.transition(.scale)` with spring animation
- Lock message toast: `.opacity` with auto-dismiss after 2 seconds

**Haptics** (via `.sensoryFeedback`):
- Correct guess: `.success`
- Wrong guess: `.error` (light)
- Hint unlock: `.selection`
- Give up: none

### Statistics Feature (New)

**StatsViewModel** computes from SwiftData `GameResult` queries:

| Metric | Computation |
|--------|-------------|
| Games Played | `COUNT(*)` |
| Win Rate | `COUNT(won=true) / COUNT(*)` as percentage |
| Average Guesses (wins) | `AVG(guessCount) WHERE won=true` |
| Current Streak | Count consecutive `won=true` from most recent game backwards. Broken by any loss or give-up. Abandoning a game (starting new mid-game) does NOT count and does NOT break streak. |
| Best Streak | Maximum consecutive wins ever |
| Guess Distribution | Histogram of win guess counts (1-10) |

**History list:** Scrollable `List` of `GameResult` entries, newest first. Each row shows: country flag, country name, result (win/loss/gave up), guess count, date.

**Empty state:** "No games played yet" with globe illustration and "Start Playing" button.

**No iCloud sync for v1** — local SwiftData only.

### Admin / Dev Settings

Accessible via **triple-tap on version label** in the footer area (or in a settings sheet).

**Features ported:**
- Game mode toggle: Random / Specific country (with country picker)
- Country data browser: searchable list showing all 192 countries with their data fields
- System status: counts of countries with images, flags, population, etc.

**Features NOT ported (web-only):**
- Data editing (population, mountain, borders) — makes no sense for bundled data
- Image upload — images are bundled in Asset Catalog
- Export — replaced by share sheet if needed later
- Cross-window communication — not applicable

**Password:** Removed. Access is gated by the hidden triple-tap gesture instead.

### External Links

| Link | iOS Implementation |
|------|-------------------|
| Google Maps | `UIApplication.shared.open(URL)` — opens Maps app or Safari |
| Norli bookstore | `UIApplication.shared.open(URL)` — opens Safari |

Both links shown for both languages (Norli is Norway-specific but the app targets a Norwegian audience).

## Implementation Phases

### Phase 1: Foundation (Data + Project Setup)

**Tasks:**
- [x] Create Xcode project: "Globorama", iOS 17+, SwiftUI lifecycle (`GloboramaApp.swift`)
- [x] Write `prepare_ios_data.py` script to process web JSON data:
  - Read `countries_data_no.json` as base (has `name_no` for all 192)
  - Compute `centerLat`/`centerLon` from geometry bounding box midpoint
  - Flatten `capital_coordinates` to `capitalLat`/`capitalLon`
  - Strip `geometry` field entirely
  - Convert keys to camelCase
  - Populate `bordersNo` from web English file (155 non-island countries)
  - Output single `countries.json` (~1MB)
- [x] Run script, validate output: all 192 countries, all fields present, no nulls except `bordersNo` for islands
- [x] Import 192 silhouette PNGs into `Assets.xcassets/Silhouettes/` with naming: `silhouette-{iso2}`
- [x] Import 254 flag PNGs into `Assets.xcassets/Flags/` with naming: `flag-{iso2}`
- [x] Define named colors in Asset Catalog matching web palette
- [x] Create `Country.swift` Codable struct
- [x] Create `CountryDataLoader.swift` — load and decode from bundle
- [x] Create `Theme.swift` with color constants and gradient
- [x] Create `HaversineCalculator.swift` — port `calculateDistance()` and `getDirection()` from `main.js:1150-1210`
- [x] Write unit tests for Haversine distance (e.g., Oslo→Stockholm ≈ 417km) and direction

**Success criteria:** App launches, loads 192 countries from JSON, all images accessible from Asset Catalog, Haversine calculations verified.

**Estimated effort:** 2-3 days

### Phase 2: Core Game Loop

**Tasks:**
- [x] Create `GameState.swift` enum
- [x] Create `GameViewModel.swift` — port core game logic:
  - `startNewGame()` — random selection with last-10 exclusion
  - `submitGuess(_ name:)` — name/ISO3 matching, distance/direction feedback
  - `unlockAvailableHints()` — progressive hint unlock after each guess
  - `endGame(_ state:)` — unified end state, always reveals all hints
  - `giveUp()` — calls `endGame(.gaveUp)`
  - Computed properties: `filteredCountries`, `isHintUnlocked(_ number:)`, hint data accessors
- [x] Create `GameView.swift` — main game screen composition
- [x] Create `SilhouetteView.swift` — country image from Asset Catalog
- [x] Create `GuessInputView.swift` + `AutocompleteListView.swift`:
  - TextField with focus state management
  - Overlay dropdown with filtered suggestions
  - Keyboard dismissal on submit and suggestion tap
  - Already-guessed countries dimmed
- [x] Create `FeedbackListView.swift` + `FeedbackItemView.swift`:
  - Numbered circle (purple, green for correct)
  - Country name, distance in km, compass direction
  - Slide-in animation, newest first
- [x] Create `GameOverView.swift`:
  - Country name reveal with purple gradient box
  - "New Game", "Google Maps", "Norli" buttons
  - All hints displayed
- [x] Add haptic feedback: `.sensoryFeedback(.success)` on win, `.sensoryFeedback(.error)` on wrong guess

**Success criteria:** Full game loop playable — guess countries, see feedback, unlock hints, win/lose, start new game. No persistence yet.

**Estimated effort:** 4-5 days

### Phase 3: Hint System + UI Polish

**Tasks:**
- [x] Create `HintGridView.swift` — 2×3 grid layout
- [x] Create `HintCardView.swift` — locked/unlocked states:
  - Locked: dark overlay, lock icon, emoji + label, tap shows toast
  - Unlocked: reveal animation, hint content displayed
- [x] Implement all 6 hint types:
  - Flag: image from Asset Catalog
  - Population: formatted number with locale + year
  - Capital: text
  - Region: text
  - Mountain: name + elevation in meters and feet
  - Borders: comma-separated list, or "Island (no borders)" for `isIsland`
- [x] Lock message toast: centered overlay, auto-dismiss 2s, shows required guess count
- [x] Animations: hint card unlock (scale+opacity), feedback slide-in, country reveal
- [ ] Adapt layout for different iPhone sizes (SE through Pro Max)
- [ ] Test with Dynamic Type (large and extra-large text sizes)

**Success criteria:** All 6 hints work correctly, locked/unlocked states clear, animations smooth, layout works on iPhone SE through Pro Max.

**Estimated effort:** 2-3 days

### Phase 4: Localization

**Tasks:**
- [ ] Create `Localizable.xcstrings` String Catalog
- [ ] Set development language to Norwegian (nb)
- [ ] Add English localization target
- [ ] Port all 49 translation keys from `translations.json`
- [ ] Add new keys for stats, settings, accessibility (~30 additional keys)
- [x] Implement language toggle in UI (flag buttons in header, matching web design)
- [x] Wire `@AppStorage("selectedLanguage")` for persistence
- [x] Country display names switch based on language (`name` vs `nameNo`)
- [x] Borders display switches based on language (`borders` vs `bordersNo`)
- [x] Population formatting: use `nb_NO` locale for Norwegian, `en_US` for English
- [x] Compass directions use localized strings
- [ ] Test both languages end-to-end

**Success criteria:** Full game playable in both Norwegian and English, language persists across launches, all UI text localized.

**Estimated effort:** 1-2 days

### Phase 5: Statistics + SwiftData

**Tasks:**
- [x] Create `GameResult.swift` SwiftData model
- [x] Configure `ModelContainer` in `GloboramaApp.swift`
- [x] Save `GameResult` at end of each game in `GameViewModel.endGame()`
- [x] Create `StatsViewModel.swift`:
  - Games played, win rate, average guesses (wins only)
  - Current streak (consecutive wins, broken by loss/give-up)
  - Best streak (all-time max)
  - Guess distribution histogram (1-10)
- [x] Create `StatsView.swift`:
  - Stats cards at top (games, win%, avg guesses, streak)
  - Guess distribution bar chart
  - Scrollable game history list
- [x] Create `GameHistoryRow.swift`:
  - Country flag thumbnail, country name, result badge (win/loss/gave up), guess count, date
- [x] Empty state for first launch
- [x] Navigation: stats accessible via toolbar button on GameView
- [ ] Test stats accuracy after 10+ games

**Success criteria:** Stats persist across app launches, all metrics computed correctly, history scrollable and accurate.

**Estimated effort:** 2-3 days

### Phase 6: Settings + Admin

**Tasks:**
- [x] Create `DevSettingsView.swift`:
  - Game mode toggle (random / specific)
  - Country picker (searchable list) for specific mode
  - System status dashboard (country counts by field)
- [x] Triple-tap gesture on version label to present DevSettingsView as sheet
- [x] Wire game mode to `@AppStorage("gameMode")` and `@AppStorage("specificCountry")`
- [x] `GameViewModel.startNewGame()` checks admin settings before random selection
- [x] Create `CountryBrowserView.swift`:
  - Searchable list of all 192 countries
  - Detail view: all data fields, silhouette image, flag
- [x] Version display in footer: app version from `Bundle.main`

**Success criteria:** Dev settings toggle works, specific country mode forces the chosen country, country browser shows all data accurately.

**Estimated effort:** 1-2 days

### Phase 7: App Store Preparation

**Tasks:**
- [ ] Design app icon (1024×1024, based on GLOBORAMA logo)
- [ ] Create launch screen
- [ ] Write App Store metadata:
  - App name: "Globorama" (or "GLOBORAMA")
  - Subtitle: "Geography Guessing Game"
  - Description (Norwegian primary, English secondary)
  - Keywords: geography, quiz, country, game, flags, trivia
  - Category: Games > Trivia
- [ ] Take screenshots on required device sizes (6.9", 6.7", 6.5")
- [ ] Write privacy policy (no data collected — fully offline, no analytics)
- [ ] Set up App Store Connect, create app listing
- [ ] Set age rating (no objectionable content)
- [ ] Test on physical device
- [ ] Archive and validate with Xcode
- [ ] Submit for review

**Success criteria:** App approved and published on App Store.

**Estimated effort:** 2-3 days

## Alternative Approaches Considered

(see brainstorm: `docs/brainstorms/2026-04-21-ios-native-app-brainstorm.md`)

1. **UIKit + MVC** — Rejected: more boilerplate, imperative style doesn't match the reactive game state pattern
2. **SwiftUI + UserDefaults only** — Rejected: game history/stats need queryable persistence (SwiftData)
3. **Modular Swift Packages** — Rejected: over-engineered for a single-developer game app

## System-Wide Impact

### State Lifecycle Risks

- **In-progress game is in-memory only.** Force-quit loses the current game. This is intentional — no orphaned state possible.
- **SwiftData only stores completed games.** `GameResult` is inserted only in `endGame()`. Abandoning a game (starting new mid-game) creates no record.
- **Language preference in `@AppStorage`** survives everything. Country display names recompute on language change.

### Error Propagation

- **JSON decode failure:** Falls back to 3 hardcoded Scandinavian countries (matching web behavior). Logged to console.
- **Missing image asset:** SwiftUI `Image` shows nothing. No crash. The web version shows a broken image placeholder.
- **SwiftData write failure:** Game continues, stats just don't persist. Non-blocking.

### API Surface Parity

No API or backend. Fully self-contained. The only external-facing surface is the two URLs opened in Safari (Google Maps, Norli).

## Acceptance Criteria

### Functional Requirements

- [ ] Player can play a full game: see silhouette, type guess with autocomplete, receive distance/direction feedback
- [ ] All 6 hints unlock progressively and display correct data
- [ ] All 192 countries are playable with correct silhouettes, flags, and metadata
- [ ] Game ends correctly on win (correct guess), loss (10 attempts), and give up — all three reveal country + all hints
- [ ] Language toggle between Norwegian and English works, persists across launches
- [ ] Statistics track games played, win rate, average guesses, consecutive win streak, best streak
- [ ] Game history shows all past games with country, result, guesses, date
- [ ] Dev settings accessible via triple-tap, game mode toggle works
- [ ] Google Maps and Norli links open correctly in Safari
- [ ] Recently played countries (last 10) excluded from random selection

### Non-Functional Requirements

- [ ] App launches in under 2 seconds (JSON decode + image catalog)
- [ ] App bundle size under 15MB (optimized JSON ~1MB + images ~4MB + binary)
- [ ] Supports Dynamic Type (accessibility)
- [ ] Works on iPhone SE (3rd gen) through iPhone 16 Pro Max
- [ ] Portrait orientation only
- [ ] Fully offline — no network required for gameplay
- [ ] iOS 17.0+ minimum deployment target

### Quality Gates

- [ ] Unit tests for: Haversine distance/direction, streak calculation, game state transitions
- [ ] UI tested on 3 device sizes in Simulator (SE, 15, 16 Pro Max)
- [ ] Both languages tested end-to-end
- [ ] No crashes on any game flow (play, win, lose, give up, new game, repeat)
- [ ] SwiftData persistence verified across app restart

## Dependencies & Prerequisites

- **Xcode 16+** (for iOS 17 SDK, SwiftData, String Catalogs)
- **Apple Developer account** ($99/year for App Store distribution)
- **Physical iPhone** for final testing before submission
- **Python 3** for the data preparation script (one-time use)

## Risk Analysis & Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| `bordersNo` data is empty for all countries | Norwegian users see English border names | High (confirmed) | Accept English border names for v1, or manually translate 155 country-border pairs |
| App Store rejection for "too simple" | Can't distribute | Low | Game has depth: 192 countries, 6 hints, stats, bilingual |
| SwiftData bugs on iOS 17.0 | Crashes or data loss | Medium | Test on iOS 17.4+ (most stable), set deployment target to 17.2 if issues found |
| Large Asset Catalog slows Xcode | Slow builds | Low | Split into `Silhouettes.xcassets` and `Flags.xcassets` if needed |
| Geometry center calculation differs from web | Distance/direction values change slightly | Low | Pre-compute centers using same bounding-box algorithm as web |

## Data Preparation Script

A one-time Python script (`Scripts/prepare_ios_data.py`) that:

1. Reads `countries_data_no.json` (has `name_no` for all 192 countries)
2. For each country:
   - Computes `centerLat`/`centerLon` from geometry bounding box midpoint (matching `calculateCenter()` in `main.js:449-490`)
   - Flattens `capital_coordinates` → `capitalLat`, `capitalLon`
   - Strips `geometry` field
   - Strips `iso_code` field (unused)
   - Converts all keys to camelCase
   - Reads `borders_no` from English file if available
3. Outputs `countries.json` with all 192 entries

**Validation:** Compare center coordinates against web version for 5 sample countries (Norway, Egypt, Brazil, Japan, Australia) to ensure matching values.

## Success Metrics

| Metric | Target |
|--------|--------|
| App Store approval | First submission |
| App launch time | < 2 seconds |
| App bundle size | < 15 MB |
| Crash-free rate | 99.5%+ |
| Game completion rate | Trackable via stats feature |

## Future Considerations (Post-v1)

- iPad-optimized layout
- Share results (Wordle-style emoji grid)
- Daily challenge (same country for all players)
- iCloud sync for stats
- Sound effects
- Difficulty modes (fewer attempts, no hints)
- Additional languages beyond NO/EN
- Widget showing daily challenge

## Sources & References

### Origin

- **Brainstorm document:** [docs/brainstorms/2026-04-21-ios-native-app-brainstorm.md](docs/brainstorms/2026-04-21-ios-native-app-brainstorm.md) — Key decisions carried forward: SwiftUI + MVVM + SwiftData architecture, iOS 17+ target, pre-computed country centers, full port with stats feature.

### Internal References

- Core game logic: `js/main.js` (1781 lines, 47 methods)
- Admin panel: `js/admin.js` (487 lines)
- Translations: `translations.json` (49 keys × 2 languages)
- Country data: `countries_data_no.json` (192 countries, source of truth)
- CSS styling: `css/style.v2.css` (1253 lines, color palette and responsive breakpoints)

### External References

- Apple @Observable documentation: developer.apple.com/documentation/Observation
- SwiftData documentation: developer.apple.com/documentation/SwiftData
- String Catalogs guide: developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog
- App Store Review Guidelines: developer.apple.com/app-store/review/guidelines

### SpecFlow Analysis Findings

Key gaps identified and resolved:
- **End-game inconsistency (Gap 3.7):** Web `endGame(false)` doesn't reveal hints. iOS version unifies all end states.
- **Duplicate guesses (Gap 3.5):** Allowed but dimmed in autocomplete. Each burns an attempt (matching web).
- **Country repeats (Gap 3.8):** iOS excludes last 10 played countries from random selection (improvement over web).
- **Streak definition (Gap 3.10):** Consecutive wins, broken by loss or give-up. Abandoning doesn't count.
- **Norwegian borders empty (Gap 3.1):** Accept English border names for v1. Flag as known limitation.
- **Admin architecture (Gap 3.21):** Hidden dev settings via triple-tap gesture. No password.
