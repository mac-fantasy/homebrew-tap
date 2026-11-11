cask "krill-desktop" do
  version "0.2.0"
  sha256 "28e4d617f6905c44c95381cfb9576d9dd60a740c71c1d5d0b7f0c1767467c31c"

  url "https://github.com/mac-fantasy/krill-desktop/releases/download/v#{version}/Krill.Desktop-#{version}-macos-arm64.zip"
  name "Krill Desktop"
  desc "Menu bar assistant for Krill account usage and balances"
  homepage "https://github.com/mac-fantasy/krill-desktop"

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :sequoia

  app "Krill Desktop.app"

  uninstall quit: "com.krill.desktop.macos"

  zap trash: "~/Library/Application Support/KrillDesktop"
end
