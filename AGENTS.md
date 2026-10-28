# Unified Homebrew tap

- Canonical repository: `lljxww/homebrew-tap`; Homebrew tap: `lljxww/tap`.
- Put each application in `Casks/<token>.rb`. Installation uses `brew install --cask lljxww/tap/<token>`.
- Read `README.md`, `apps.json`, and the existing updater before adding an app. Preserve all existing entries, casks, workflows, and unrelated local changes.
- Download the real upstream release asset and compute its SHA-256. Check application name, bundle ID, architectures, minimum macOS version, and update behavior from the actual bundle or installer. Never fabricate checksums, use `sha256 :no_check` for a versioned release, or disable Gatekeeper/quarantine in a cask.
- `apps.json` configures `scripts/update-casks.py`; do not create another per-app tap or replace the shared updater with a project-specific one. The updater currently supports one archive and one top-level version/checksum per cask. Extend it and add meaningful verification tests when a different release layout requires it.
- Use `auto_updates true` only when the app actually updates itself. Keep ordinary uninstall separate from `zap`; list only confirmed application-owned data paths in `zap`.
- Verify with `python3 -m unittest discover -s tests`, `python3 scripts/update-casks.py <token>`, and `brew style Casks/<token>.rb`. On macOS, also use Homebrew info, online audit, and installation dry-run for the fully qualified cask. Do not overwrite or uninstall the user's existing app just to test packaging.
- For an old per-app tap, publish the destination first, then preserve the old repository with migration instructions and `tap_migrations.json`. Remove its duplicate Cask and update automation after the destination works. Check trust behavior before promising automatic migration.
- Before pushing, fetch and integrate remote changes without force-pushing or discarding other apps. Commit only the intended changes and report exact installation commands and verification results.
