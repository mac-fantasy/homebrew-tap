cask "mac-monitor" do
  version "0.1.0"
  sha256 "2659f4799c0a27b1c11435f0f08478b1d49e02783ab894d25b2b8d0caf170674"

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
