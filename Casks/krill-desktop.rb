cask "krill-desktop" do
  version "0.1.7"
  sha256 "151084ab2a8858081d07e85bb25e88bb7b623a006170ea2f7286716993489651"

  url "https://github.com/mac-fantasy/krill-desktop/releases/download/v#{version}/Krill.Desktop-#{version}-macos-universal.zip"
  name "Krill Desktop"
  desc "Menu bar assistant for Krill account usage and balances"
  homepage "https://github.com/mac-fantasy/krill-desktop"

  auto_updates true
  depends_on macos: :sonoma

  app "Krill Desktop.app"

  uninstall quit: "com.krill.desktop.macos"

  zap trash: "~/Library/Application Support/KrillDesktop"
end
