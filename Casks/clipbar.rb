cask "clipbar" do
  version "1.1.0"
  sha256 "045699c52a00d5917aaace84d896a5a1161166bd655e95aab0d508d18e7ac587"

  url "https://github.com/mac-fantasy/ClipBar/releases/download/v#{version}/ClipBar-#{version}-macOS-universal.zip"
  name "ClipBar"
  desc "Menu bar clipboard history manager"
  homepage "https://github.com/mac-fantasy/ClipBar"

  auto_updates true
  depends_on macos: :ventura

  app "ClipBar.app"

  uninstall quit: "local.ClipBar"

  zap trash: [
    "~/Library/Application Support/ClipBar",
    "~/Library/Caches/local.ClipBar",
    "~/Library/Preferences/local.ClipBar.plist",
  ]
end
