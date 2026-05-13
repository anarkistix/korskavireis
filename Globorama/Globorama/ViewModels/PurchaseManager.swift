import Foundation
import Observation
import os
import StoreKit

enum PurchaseState: Equatable {
    case idle
    case loading
    case error(String)
}

@Observable
@MainActor
class PurchaseManager {
    var isUnlocked: Bool = false
    var product: Product?
    var purchaseState: PurchaseState = .idle

    @ObservationIgnored
    private var transactionListenerTask: Task<Void, Never>?
    @ObservationIgnored
    private let logger = Logger(subsystem: "com.mariusarnesen.globorama", category: "purchase")

    private static let productID = "com.mariusarnesen.globorama.unlimited"
    private static let unlockKey = "com.mariusarnesen.globorama.unlocked"

    init() {
        isUnlocked = UserDefaults.standard.bool(forKey: Self.unlockKey)
        transactionListenerTask = Task { [weak self] in
            await self?.listenForTransactions()
        }
        Task { [weak self] in
            await self?.loadProduct()
            await self?.updateEntitlementStatus()
        }
    }

    deinit {
        transactionListenerTask?.cancel()
    }

    func loadProduct() async {
        do {
            let products = try await Product.products(for: [Self.productID])
            logger.info("Loaded \(products.count) products for ID \(Self.productID)")
            product = products.first
            if product == nil {
                logger.warning("No product found for \(Self.productID)")
            }
        } catch {
            logger.error("Failed to load products: \(error)")
            product = nil
        }
    }

    func purchase() async {
        if product == nil {
            logger.info("Product nil at purchase time, retrying load...")
            await loadProduct()
        }
        guard let product else {
            purchaseState = .error("Product not available — check StoreKit configuration")
            return
        }

        purchaseState = .loading

        do {
            let result = try await product.purchase()
            switch result {
            case .success(let verification):
                switch verification {
                case .verified(let transaction):
                    await transaction.finish()
                    setUnlocked(true)
                    purchaseState = .idle
                case .unverified:
                    purchaseState = .error("Purchase could not be verified")
                }
            case .pending:
                purchaseState = .idle
            case .userCancelled:
                purchaseState = .idle
            @unknown default:
                purchaseState = .idle
            }
        } catch {
            purchaseState = .error(error.localizedDescription)
        }
    }

    func restorePurchases() async {
        purchaseState = .loading
        do {
            try await AppStore.sync()
            await updateEntitlementStatus()
            purchaseState = .idle
        } catch {
            purchaseState = .error(error.localizedDescription)
        }
    }

    private func updateEntitlementStatus() async {
        var entitled = false
        for await result in Transaction.currentEntitlements {
            if case .verified(let transaction) = result,
               transaction.productID == Self.productID,
               transaction.revocationDate == nil {
                entitled = true
                break
            }
        }
        setUnlocked(entitled)
    }

    private func listenForTransactions() async {
        for await result in Transaction.updates {
            if case .verified(let transaction) = result {
                await transaction.finish()
                await updateEntitlementStatus()
            }
        }
    }

    private func setUnlocked(_ value: Bool) {
        isUnlocked = value
        UserDefaults.standard.set(value, forKey: Self.unlockKey)
    }

    #if DEBUG
    func resetPurchase() {
        setUnlocked(false)
    }
    #endif
}
