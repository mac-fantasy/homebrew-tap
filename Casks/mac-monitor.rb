cask "mac-monitor" do
  version "0.2.0"
  sha256 "da18938e06961fad773e25b41f50b91ca214b5463cef4b38068625cfadb83d59"

  url "https://github.com/mac-fantasy/mac-monitor/releases/download/v#{version}/MacMonitor-v#{version}-arm64.zip"
  name "Mac Monitor"
  desc "Menu bar CPU, GPU, memory, and process monitor"
  homepage "https://github.com/mac-fantasy/mac-monitor"

  depends_on arch: :arm64
  depends_on macos: :sonoma

  app "MacMonitor.app"

  uninstall quit: "com.liangjw.mac-monitor"

  zap trash: "~/Library/Preferences/com.liangjw.mac-monitor.plist"
end
