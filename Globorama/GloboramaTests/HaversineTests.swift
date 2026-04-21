import Testing
@testable import Globorama

@Suite("Haversine Calculator")
struct HaversineTests {
    @Test("Oslo to Stockholm is approximately 417 km")
    func osloToStockholm() {
        let distance = HaversineCalculator.distance(
            fromLat: 59.91, fromLon: 10.75,
            toLat: 59.33, toLon: 18.07
        )
        #expect(distance > 400 && distance < 440)
    }

    @Test("Oslo to Tokyo is approximately 8400 km")
    func osloToTokyo() {
        let distance = HaversineCalculator.distance(
            fromLat: 59.91, fromLon: 10.75,
            toLat: 35.68, toLon: 139.69
        )
        #expect(distance > 8300 && distance < 8500)
    }

    @Test("Same point returns zero distance")
    func samePoint() {
        let distance = HaversineCalculator.distance(
            fromLat: 59.91, fromLon: 10.75,
            toLat: 59.91, toLon: 10.75
        )
        #expect(distance < 0.01)
    }

    @Test("Direction from Oslo to Stockholm is east")
    func directionEast() {
        let dir = HaversineCalculator.direction(
            fromLat: 59.91, fromLon: 10.75,
            toLat: 59.33, toLon: 18.07
        )
        #expect(dir == .east || dir == .southeast)
    }

    @Test("Direction from Oslo to Tromsø is north")
    func directionNorth() {
        let dir = HaversineCalculator.direction(
            fromLat: 59.91, fromLon: 10.75,
            toLat: 69.65, toLon: 18.96
        )
        #expect(dir == .north || dir == .northeast)
    }

    @Test("Direction from Oslo to London is southwest")
    func directionSouthwest() {
        let dir = HaversineCalculator.direction(
            fromLat: 59.91, fromLon: 10.75,
            toLat: 51.51, toLon: -0.13
        )
        #expect(dir == .southwest)
    }
}

@Suite("Game State")
struct GameStateTests {
    @Test("Playing is not game over")
    func playingNotOver() {
        #expect(!GameState.playing.isGameOver)
    }

    @Test("Won is game over")
    func wonIsOver() {
        #expect(GameState.won.isGameOver)
    }

    @Test("Lost is game over")
    func lostIsOver() {
        #expect(GameState.lost.isGameOver)
    }

    @Test("GaveUp is game over")
    func gaveUpIsOver() {
        #expect(GameState.gaveUp.isGameOver)
    }
}
