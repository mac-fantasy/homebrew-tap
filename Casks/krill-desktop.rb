cask "krill-desktop" do
  version "0.1.8"
  sha256 "cb31288d837785d8f71a2e1d281b908d9960012d117b926744a45395c7fa9641"

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
