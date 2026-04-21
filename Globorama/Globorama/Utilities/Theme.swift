import SwiftUI

enum Theme {
    static let teal = Color(red: 0.216, green: 0.580, blue: 0.565)           // #379490
    static let darkTeal = Color(red: 0.090, green: 0.318, blue: 0.341)       // #175157
    static let cream = Color(red: 0.980, green: 0.957, blue: 0.816)          // #faf4d0
    static let purpleStart = Color(red: 0.400, green: 0.494, blue: 0.918)    // #667eea
    static let purpleEnd = Color(red: 0.463, green: 0.294, blue: 0.635)      // #764ba2
    static let success = Color(red: 0.157, green: 0.655, blue: 0.271)        // #28a745
    static let error = Color(red: 0.863, green: 0.208, blue: 0.271)          // #dc3545
    static let info = Color(red: 0.090, green: 0.635, blue: 0.722)           // #17a2b8

    static let purpleGradient = LinearGradient(
        colors: [purpleStart, purpleEnd],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )

    static let hintCardBackground = Color(red: 0.973, green: 0.976, blue: 0.980) // #f8f9fa
    static let hintCardBorder = Color(red: 0.914, green: 0.925, blue: 0.933)     // #e9ecef
}
