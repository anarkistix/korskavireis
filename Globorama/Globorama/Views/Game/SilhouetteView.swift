import SwiftUI

struct SilhouetteView: View {
    let country: Country?

    var body: some View {
        if let country {
            Image(country.silhouetteAssetName)
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(maxWidth: 350, maxHeight: 250)
                .padding(8)
        } else {
            ProgressView()
                .frame(height: 200)
        }
    }
}
