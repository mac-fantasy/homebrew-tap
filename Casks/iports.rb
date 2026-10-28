cask "iports" do
  version "0.8.0"
  sha256 "8ea3bcb49d552d368d31754f6ef08d9b62b791c97c2e9241f8915ec159d55ab6"

  url "https://github.com/mac-fantasy/iPorts/releases/download/v#{version}/iPorts-#{version}-macos-universal.zip"
  name "iPorts"
  desc "Menu bar port and external device monitor"
  homepage "https://github.com/mac-fantasy/iPorts"

  auto_updates true
  depends_on macos: :sonoma

  app "iPorts.app"

  uninstall quit: "local.iports.app"

  zap trash: [
    "~/Library/Caches/local.iports.app",
    "~/Library/Preferences/local.iports.app.plist",
  ]
end
