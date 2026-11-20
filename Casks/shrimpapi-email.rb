cask "shrimpapi-email" do
  version "0.2.1"
  sha256 "74435ea0dfa2218173808b2a6bd8f6b68afde8baf5d9cd2e5979f5c96b4c6e82"

  url "https://github.com/mac-fantasy/shrimpapi-email/releases/download/v#{version}/ShrimpAPI.Email-#{version}-macos-universal.zip"
  name "ShrimpAPI Email"
  desc "Cloudflare SMTP email client with personalized HTML templates"
  homepage "https://github.com/mac-fantasy/shrimpapi-email"

  depends_on :macos

  app "ShrimpAPI Email.app"

  uninstall quit: "com.shrimpapi.email"

  zap trash: "~/Library/Application Support/com.shrimpapi.email"
end
