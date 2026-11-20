cask "shrimpapi-email" do
  version "0.2.0"
  sha256 "e412e88cdf76ce3855470ae6ab38c6b49c394092d409caab12b6d4d217fd20e0"

  url "https://github.com/mac-fantasy/shrimpapi-email/releases/download/v#{version}/ShrimpAPI.Email-#{version}-macos-universal.zip"
  name "ShrimpAPI Email"
  desc "Cloudflare SMTP email client with personalized HTML templates"
  homepage "https://github.com/mac-fantasy/shrimpapi-email"

  depends_on :macos

  app "ShrimpAPI Email.app"

  uninstall quit: "com.shrimpapi.email"

  zap trash: "~/Library/Application Support/com.shrimpapi.email"
end
