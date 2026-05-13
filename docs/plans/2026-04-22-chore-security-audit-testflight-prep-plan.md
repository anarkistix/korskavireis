---
title: "Security Audit & TestFlight Deployment Preparation"
type: chore
status: active
date: 2026-04-22
---

# Security Audit & TestFlight Deployment Preparation

## Overview

Perform an extensive security audit of the Globorama iOS app and prepare it for TestFlight deployment. The app is a SwiftUI geography guessing game (iOS 17+, Swift 6.0) with zero networking, zero third-party dependencies, SwiftData for game history, and UserDefaults for preferences.

**Security audit result: 0 critical, 0 high, 1 medium, 4 low, 4 informational findings.** The app has a remarkably small attack surface. The primary work is hardening debug features and preparing deployment configuration.

## Problem Statement

The app is functionally complete but has not been hardened for production or configured for App Store / TestFlight distribution. Specific issues:

1. **DevSettingsView ships in production** — accessible via triple-tap easter egg, exposes all country answers
2. **App icon has an alpha channel** — Apple rejects icons with transparency
3. **No PrivacyInfo.xcprivacy** — required since May 2024 for apps using UserDefaults
4. **No ITSAppUsesNonExemptEncryption** — causes manual export compliance dialog per build
5. **DEVELOPMENT_TEAM empty in project.yml** — blocks signing and archiving
6. **print() statements in release** — leak internal error details to system console
7. **Hardcoded version string** — footer shows `"v1.0.0"` instead of reading from Bundle
8. **URL construction uses .urlQueryAllowed** — permits `&` in country names like "Trinidad & Tobago"
9. **No scheme validation on Google Maps URLs** — defense-in-depth gap
10. **Privacy policy not hosted** — App Store Connect requires a live URL

## Proposed Solution

Three-phase approach: (1) security hardening, (2) deployment configuration, (3) build and upload.

## Technical Approach

### Implementation Phases

#### Phase 1: Security Hardening

Code changes to address all audit findings. These are independent of each other and can be done in parallel, except where noted.

##### Task 1.1: Guard DevSettingsView behind `#if DEBUG`

**Files to modify:**

- `Globorama/Globorama/Views/Game/GameView.swift` — wrap `@State private var showDevSettings`, `@State private var versionTapCount`, the `.sheet(isPresented: $showDevSettings)` modifier, and the triple-tap gesture handler (lines 6-7, 27-29, 190-199) in `#if DEBUG`
- `Globorama/Globorama/Views/Settings/DevSettingsView.swift` — wrap entire file contents in `#if DEBUG`
- `Globorama/Globorama/Views/Settings/CountryBrowserView.swift` — wrap entire file contents in `#if DEBUG` (only reachable through DevSettingsView)
- `Globorama/Globorama/ViewModels/GameViewModel.swift` — wrap the specific-country game mode path in `startNewGame()` (lines 76-80) in `#if DEBUG`, so Release always uses random mode

```swift
// GameView.swift — footer version label, Release build
Text("v\(Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0.0")")
    .font(.caption2)
    .foregroundStyle(.white.opacity(0.4))

// GameView.swift — footer version label, Debug build
#if DEBUG
Text("v\(Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0.0")")
    .font(.caption2)
    .foregroundStyle(.white.opacity(0.4))
    .onTapGesture {
        versionTapCount += 1
        if versionTapCount >= 3 {
            versionTapCount = 0
            showDevSettings = true
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            versionTapCount = 0
        }
    }
#endif
```

```swift
// GameViewModel.swift — startNewGame()
func startNewGame() {
    #if DEBUG
    let gameMode = UserDefaults.standard.string(forKey: "gameMode") ?? "random"
    if gameMode == "specific",
       let specificName = UserDefaults.standard.string(forKey: "specificCountry"),
       let country = countries.first(where: { $0.name == specificName || $0.nameNo == specificName }) {
        currentCountry = country
    } else {
        selectRandomCountry()
    }
    #else
    selectRandomCountry()
    #endif

    gameState = .playing
    attempts = 0
    // ... rest unchanged
}
```

- [x] Verify Release scheme compiles cleanly after changes
- [x] Verify Debug scheme still shows DevSettingsView on triple-tap

##### Task 1.2: Fix URL construction security

**File:** `Globorama/Globorama/ViewModels/GameViewModel.swift`

Replace `openNorli()` (lines 228-233) to use `URLComponents` for proper query parameter encoding:

```swift
func openNorli() {
    guard let country = currentCountry else { return }
    let name = country.displayName(for: language)
    var components = URLComponents(string: "https://www.norli.no/search")
    components?.queryItems = [URLQueryItem(name: "query", value: name)]
    guard let url = components?.url else { return }
    openURL(url)
}
```

Add scheme validation to `openGoogleMaps()` (lines 222-226):

```swift
func openGoogleMaps() {
    guard let urlString = currentCountry?.googleMapsUrl,
          let url = URL(string: urlString),
          url.scheme == "https" else { return }
    openURL(url)
}
```

##### Task 1.3: Replace print() with os.Logger

**File:** `Globorama/Globorama/Utilities/CountryDataLoader.swift` (lines 6, 12-13)

```swift
import os

private let logger = Logger(subsystem: Bundle.main.bundleIdentifier ?? "com.mariusarnesen.globorama", category: "data")

// Replace:
//   print("countries.json not found in bundle")
// With:
logger.error("countries.json not found in bundle")

// Replace:
//   print("Failed to decode countries.json: \(error)")
// With:
logger.error("Failed to decode countries.json: \(error)")
```

##### Task 1.4: Read version from Bundle

**File:** `Globorama/Globorama/Views/Game/GameView.swift` (line 187-188)

Replace hardcoded `"v1.0.0"` with dynamic Bundle read. The version label in the footer should display `"v{marketingVersion}"` format:

```swift
private var appVersion: String {
    let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0.0"
    return "v\(version)"
}
```

Use `appVersion` in the footer text.

##### Task 1.5: Fix app icon alpha channel

**File:** `Globorama/Scripts/generate_app_icon.py`

The icon is created as RGBA (line 32: `Image.new("RGBA", ...)`), and the globe uses alpha compositing for the circular mask. Apple rejects icons with alpha channels.

Fix: flatten the RGBA image onto an opaque RGB background before saving:

```python
# Before saving, flatten to RGB (no alpha channel)
final = Image.new("RGB", (SIZE, SIZE), BG_TEAL)
final.paste(icon, mask=icon.split()[3])
final.save(out_path, "PNG")
```

- [x] Regenerate the icon after script change
- [x] Verify with: `python3 -c "from PIL import Image; img = Image.open('path/to/icon.png'); print(img.mode)"` — must output `RGB`, not `RGBA`

##### Task 1.6: Handle SwiftData save errors

**File:** `Globorama/Globorama/ViewModels/GameViewModel.swift` (line 256)

Replace silent `try?` with logged error:

```swift
do {
    try context.save()
} catch {
    Logger.game.error("Failed to save game result: \(error)")
}
```

Add a `Logger` extension or use the one from CountryDataLoader.

---

#### Phase 2: Deployment Configuration

##### Task 2.1: Add PrivacyInfo.xcprivacy

Create `Globorama/Globorama/PrivacyInfo.xcprivacy`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyTrackingDomains</key>
    <array/>
    <key>NSPrivacyCollectedDataTypes</key>
    <array/>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
```

**Note:** After Phase 1 Task 1.1, the `gameMode` and `specificCountry` UserDefaults reads in `startNewGame()` are behind `#if DEBUG`. Only `selectedLanguage` ships in Release. `CA92.1` ("app reads/writes data accessible only to the app itself") covers this correctly.

##### Task 2.2: Update project.yml for TestFlight

**File:** `Globorama/project.yml`

Changes needed:

```yaml
settings:
  base:
    DEVELOPMENT_TEAM: N6FECHVY7S  # was ""
    # Keep SWIFT_VERSION at 6.0 but Apple does not require Swift 6 language mode
```

Under `targets.Globorama.info.properties`, add:

```yaml
ITSAppUsesNonExemptEncryption: false
```

Ensure `PrivacyInfo.xcprivacy` is picked up by sources (it should auto-detect as a resource if placed in the `Globorama/` source directory).

- [x] Run `xcodegen generate` after changes
- [x] Verify `PrivacyInfo.xcprivacy` appears in Copy Bundle Resources build phase
- [x] Verify `ITSAppUsesNonExemptEncryption` appears in generated Info.plist

##### Task 2.3: Increment build number

**File:** `Globorama/project.yml` (line 34)

Set `CURRENT_PROJECT_VERSION` to an appropriate value. For the first TestFlight upload, `1` is fine. Document that this must be incremented before each subsequent upload.

##### Task 2.4: Host privacy policy

The privacy policy exists at `Globorama/AppStore/privacy-policy.md`. It needs to be accessible at a public URL for App Store Connect.

Options (user decides):
- **GitHub Pages** — create a simple site from the repo
- **GitHub raw file** — use the raw.githubusercontent.com URL (works but looks unprofessional)
- **Simple static hosting** — Netlify, Vercel, or any static host

The URL must be provided in App Store Connect under "Privacy Policy URL".

---

#### Phase 3: Build & Upload

##### Task 3.1: Register app in App Store Connect

Manual steps (cannot be automated):

1. Log in to [App Store Connect](https://appstoreconnect.apple.com)
2. Click "My Apps" > "+" > "New App"
3. Fill required fields:
   - **Platform:** iOS
   - **Name:** Globorama
   - **Primary Language:** Norwegian (or English — user decides)
   - **Bundle ID:** `com.mariusarnesen.globorama` (must match project)
   - **SKU:** `GLOBORAMA_IOS`
4. Select **Primary Category:** Games > Trivia
5. Complete **Age Rating** questionnaire (no objectionable content)
6. Set **Price:** Free
7. Enter **Privacy Policy URL** from Task 2.4
8. Complete **App Privacy** section: select "Data Not Collected"

##### Task 3.2: Prepare App Store metadata

Reference: `Globorama/AppStore/metadata.md` (already exists with descriptions and keywords)

Still needed:
- [ ] Support URL (required by App Store Connect)
- [ ] Copyright: `2026 Happygolucky Software` (matches footer)
- [ ] Screenshots: minimum 1 for 6.7" iPhone (1290 x 2796 px) — capture on iPhone 15 Pro Max simulator
- [ ] App Review contact info (name, email, phone)

##### Task 3.3: Archive and upload

1. Open `Globorama.xcodeproj` in Xcode
2. Select "Any iOS Device (arm64)" as destination
3. Product > Archive
4. In Organizer, select archive > Distribute App > TestFlight & App Store
5. Upload

- [ ] Verify archive succeeds without warnings
- [ ] Verify upload passes App Store Connect processing (email confirmation within ~30 min)
- [ ] Add internal testers in TestFlight

---

## Acceptance Criteria

### Functional Requirements

- [x] DevSettingsView and CountryBrowserView are excluded from Release builds (`#if DEBUG`)
- [x] Release build always uses random game mode (no specific-country path)
- [x] App icon has no alpha channel (RGB mode, not RGBA)
- [x] PrivacyInfo.xcprivacy declares UserDefaults usage with reason CA92.1
- [x] ITSAppUsesNonExemptEncryption is set to false
- [x] DEVELOPMENT_TEAM is set in project.yml
- [x] Version string in footer reads from Bundle, not hardcoded
- [x] No print() statements in Release build (replaced with os.Logger)
- [x] URL construction uses URLComponents for Norli search
- [x] Google Maps URL validates https scheme
- [ ] Privacy policy hosted at a public URL

### Non-Functional Requirements

- [x] Release scheme compiles and runs without warnings
- [x] Debug scheme retains all dev features (DevSettingsView, print logging)
- [ ] App archives successfully in Xcode
- [ ] Build uploads to App Store Connect without errors
- [ ] TestFlight build installs and runs on a physical device

### Quality Gates

- [ ] Existing HaversineTests pass
- [ ] Manual test: play a full game (win, lose, give up) in Release build
- [ ] Manual test: language toggle works in Release build
- [ ] Manual test: stats sheet displays correctly in Release build
- [ ] Manual test: Google Maps and Norli links open correctly after game

---

## Security Audit Summary

| Severity | Count | Findings |
|----------|-------|----------|
| CRITICAL | 0 | — |
| HIGH | 0 | — |
| MEDIUM | 1 | DevSettingsView in production (Task 1.1) |
| LOW | 4 | Silent persistence failures (Task 1.6), print statements (Task 1.3), URL encoding (Task 1.2), no scheme validation (Task 1.2) |
| INFO | 4 | DEVELOPMENT_TEAM mismatch (Task 2.2), no explicit SwiftData encryption (acceptable), UserDefaults key naming (no action), countries.json clean (no action) |

**Overall Risk: LOW** — No networking, no PII, no third-party dependencies, no secrets.

---

## Dependencies & Prerequisites

- Apple Developer Program membership (active, $99/year)
- Xcode 16+ installed (required for iOS 18 SDK — current submission mandate)
- Physical iOS device for final testing (recommended but not required for TestFlight upload)
- Privacy policy hosted at a public URL before App Store Connect setup
- Python 3 + Pillow for icon regeneration

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| App icon alpha channel rejection | HIGH | Blocks upload | Task 1.5 — flatten to RGB before saving |
| Missing PrivacyInfo.xcprivacy rejection | HIGH | Blocks upload | Task 2.1 — add manifest |
| Geopolitically sensitive content (Taiwan, etc.) | LOW | Rejection in specific markets | Accept for TestFlight (internal only); revisit before public release |
| Content licensing for silhouette/flag images | MEDIUM | Legal/rejection risk | Verify image sources are freely licensed before App Store submission |
| SwiftData schema migration (future) | LOW | Crash on update | Not needed for v1.0.0; add VersionedSchema before any model changes |
| `#if DEBUG` changes break Release build | LOW | Build failure | Compile and test Release scheme after changes |

## Future Considerations

- **SwiftData VersionedSchema**: Set up before any GameResult model changes
- **Build number automation**: Script to increment CURRENT_PROJECT_VERSION before each archive
- **Geopolitical review**: Audit silhouette boundaries for disputed territories before wide App Store release
- **Content licensing audit**: Verify all flag and silhouette image sources
- **iPad layout**: Currently portrait-locked; consider native iPad support
- **Accessibility**: VoiceOver testing, Dynamic Type support

## Sources & References

### Internal References

- Security audit: `GameViewModel.swift`, `CountryDataLoader.swift`, `GameView.swift`, `DevSettingsView.swift`
- Existing metadata: `Globorama/AppStore/metadata.md`
- Existing privacy policy draft: `Globorama/AppStore/privacy-policy.md`
- Icon generation: `Globorama/Scripts/generate_app_icon.py`
- Project config: `Globorama/project.yml`

### External References

- [Apple: Adding a privacy manifest](https://developer.apple.com/documentation/bundleresources/adding-a-privacy-manifest-to-your-app-or-third-party-sdk)
- [Apple TN3183: Required reason API entries](https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest)
- [Apple: App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Apple: App icons HIG](https://developer.apple.com/design/human-interface-guidelines/app-icons)
- [Apple: TestFlight](https://developer.apple.com/testflight/)
- [Apple: Upcoming SDK requirements](https://developer.apple.com/news/upcoming-requirements/)
