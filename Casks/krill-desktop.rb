cask "krill-desktop" do
  version "0.2.1"
  sha256 "81fbe8be3eaff199f402557e35d161e3d034c809dbfb9538aedfcbe162289f97"

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
