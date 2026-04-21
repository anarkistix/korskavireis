import Foundation

enum GameState: Equatable {
    case playing
    case won
    case lost
    case gaveUp

    var isGameOver: Bool {
        self != .playing
    }
}
