cask "shrimpapi-email" do
  version "0.2.2"
  sha256 "08c2e5e36f1315b643fb61420129097b0dd52905b69e93c84409c02253c4a104"

  url "https://github.com/mac-fantasy/shrimpapi-email/releases/download/v#{version}/ShrimpAPI.Email-#{version}-macos-universal.zip"
  name "ShrimpAPI Email"
  desc "Cloudflare SMTP email client with personalized HTML templates"
  homepage "https://github.com/mac-fantasy/shrimpapi-email"

  depends_on :macos

  app "ShrimpAPI Email.app"

  uninstall quit: "com.shrimpapi.email"

  zap trash: "~/Library/Application Support/com.shrimpapi.email"
end
