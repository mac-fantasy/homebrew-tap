cask "krill-desktop" do
  version "0.1.6"
  sha256 "8615a83743f5226374a2e439b650e056de1e4e48c5b60cac56544ec7def2da31"

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
