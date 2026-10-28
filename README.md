# Mac Fantasy Homebrew Tap

[mac-fantasy](https://github.com/mac-fantasy) 的统一 Mac 工具安装源。每个应用有独立的 Cask，安装包继续由各项目的 GitHub Releases 发布。

## 应用与安装

| 应用 | 系统与架构 | 安装命令 |
| --- | --- | --- |
| [ClipBar](https://github.com/mac-fantasy/ClipBar) | macOS 13+，Apple Silicon / Intel | `brew install --cask mac-fantasy/tap/clipbar` |
| [iPorts](https://github.com/mac-fantasy/iPorts) | macOS 14+，Apple Silicon / Intel | `brew install --cask mac-fantasy/tap/iports` |
| [Mac Monitor](https://github.com/mac-fantasy/mac-monitor) | macOS 14+，Apple Silicon | `brew install --cask mac-fantasy/tap/mac-monitor` |
| [Krill Desktop](https://github.com/mac-fantasy/krill-desktop) | macOS 14+，Apple Silicon / Intel | `brew install --cask mac-fantasy/tap/krill-desktop` |

使用完整名称安装时，Homebrew 会自动添加此 tap 并信任指定的 Cask。也可以先运行 `brew tap mac-fantasy/tap`，再使用上表中的完整安装命令。参见 [Homebrew Tap Trust](https://docs.brew.sh/Tap-Trust)。

当前这些应用使用 ad-hoc 签名，尚未做 Apple Developer ID 签名和公证。macOS 可能阻止首次打开，请确认安装来源后按「系统设置 → 隐私与安全性」中的提示允许打开。具体要求以各项目说明为准。

如果已手动安装同名应用，请先退出并将「应用程序」中的旧 `.app` 移到其他位置后再使用 Homebrew 安装。普通卸载保留用户数据；只有明确使用 `--zap` 时才按对应 Cask 清理设置或缓存。

## 从个人账号的 tap 切换

仓库由 `lljxww/homebrew-tap` 转入 `mac-fantasy/homebrew-tap`。已通过 `lljxww/tap/clipbar` 或更早的 `lljxww/clipbar/clipbar` 安装的用户可以执行：

```bash
brew tap mac-fantasy/tap
brew reinstall --cask mac-fantasy/tap/clipbar
```

重新安装会退出 ClipBar 并更新安装来源，保留剪贴板历史和设置。完成后可移除本机仍存在的旧 tap：`brew untap lljxww/tap`、`brew untap lljxww/clipbar`。

如果旧 tap 的 GitHub 重定向导致 Homebrew 报名称冲突，可先用 `brew untap --force lljxww/tap` 移除旧安装源，再运行上述切换命令；这不会卸载应用或清理数据。GitHub 转移保留旧仓库重定向，但 Homebrew 对新 tap / Cask 需要独立信任，请优先使用新的完整名称命令。

旧的 [lljxww/homebrew-clipbar](https://github.com/lljxww/homebrew-clipbar) 继续留在个人账号，保留迁移说明和指向 `mac-fantasy/tap` 的映射。

## 更新与卸载

```bash
brew update
brew upgrade --cask mac-fantasy/tap/mac-monitor
brew upgrade --cask --greedy mac-fantasy/tap/clipbar mac-fantasy/tap/iports mac-fantasy/tap/krill-desktop
```

ClipBar、iPorts 和 Krill Desktop 可以自行更新，Cask 标记了 `auto_updates true`，通过 Homebrew 手动升级时需要 `--greedy`。Mac Monitor 当前没有内置更新器。

```bash
brew uninstall --cask mac-fantasy/tap/clipbar
```

普通卸载保留历史和设置。`brew uninstall --cask --zap mac-fantasy/tap/clipbar` 会同时删除该 Cask 声明的数据，请按实际需要使用；其他应用同理。

Krill Desktop `0.1.5` 起使用组织的新更新地址。旧客户端严格校验原仓库 URL，可能无法识别迁移后的附件，需要通过 Homebrew 或新 Release 安装一次新版；账号凭据和偏好目录继续使用原位置。

## 自动同步 Release

GitHub Actions 的 **Update Casks** 每 6 小时检查 `apps.json` 中所有项目的最新稳定版 Release，也可以手动运行。它下载实际安装包，核对 GitHub 的 SHA-256 digest 及配置的校验清单，再更新对应 Cask。全部选中应用通过校验后才写入文件；校验失败时保留已有定义。

工作流只使用本仓库的 `GITHUB_TOKEN`，不需要各应用配置跨仓库 secret。公共仓库长期没有活动时，GitHub 可能暂停定时工作流，届时可手动重新启用。发布后需要立即同步时可运行：

```bash
gh workflow run update-casks.yml --repo mac-fantasy/homebrew-tap
```

## 接入其他项目

可直接复制 [其他项目接入提示词](docs/ONBOARDING_PROMPT.zh-CN.md)，交给其他项目中的大模型执行。维护约定见 [AGENTS.md](AGENTS.md)。

1. 在 `Casks/<token>.rb` 添加应用的独立 Cask，使用项目正式 Release 的下载地址和实际校验值。
2. 向 `apps.json` 追加配置，保留已有应用。例如：

   ```json
   {
     "another-app": {
       "repository": "mac-fantasy/AnotherApp",
       "asset": "AnotherApp-{version}-macOS-universal.zip",
       "checksums": "SHA256SUMS"
     }
   }
   ```

   以上名称仅作示例。`asset` 和 `checksums` 支持 `{version}` 与 `{tag}`。`checksums` 可省略，省略时要求 GitHub 提供安装包的 SHA-256 digest；清单支持标准 `shasum -a 256` / `sha256sum` 格式。

   默认接受 `v1.2.3` 或 `1.2.3` 格式的稳定 tag。其他格式可通过带 `version` 命名捕获组的 `tag_pattern` 配置；`version_components` 可将数字版本补齐到指定段数。若原始 tag 与应用版本不同，可设置 `url_from_asset: true`，让更新器同时更新已验证的下载 URL，并保留 Homebrew 的版本插值；Mac Monitor 的两段 tag 使用这种配置。

3. 更新应用列表、源项目安装说明，并验证后提交。

```bash
python3 -m unittest discover -s tests
python3 scripts/update-casks.py          # 同步全部应用
python3 scripts/update-casks.py clipbar  # 只同步 ClipBar
brew style Casks/*.rb
```

当前更新器适用于单一安装包、一个顶层 `version` 和一个顶层 `sha256` 的 Cask。若新项目分架构发布，需要保留正确的 Cask 结构并扩展更新器及测试，不应套用错误的通用包配置。
