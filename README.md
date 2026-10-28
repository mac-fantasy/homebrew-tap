# ClipBar Homebrew Tap

[ClipBar](https://github.com/lljxww/ClipBar) 的 Homebrew Cask 安装源，由项目维护者维护。支持 macOS 13 及以上版本、Apple Silicon 和 Intel。

## 安装

```bash
brew install --cask lljxww/clipbar/clipbar
```

Homebrew 会自动添加此 tap，并将 `ClipBar.app` 安装到「应用程序」目录。也可以先添加 tap：

```bash
brew tap lljxww/clipbar
brew install --cask lljxww/clipbar/clipbar
```

当前应用使用 ad-hoc 签名，尚未做 Apple Developer ID 签名和公证。macOS 可能阻止首次打开；请确认安装来源后，在「系统设置 → 隐私与安全性」中按系统提示允许打开。此 tap 不会移除下载隔离属性或修改系统安全设置。

如果已手动安装 ClipBar，请先退出应用，并将已有的 `/Applications/ClipBar.app` 移到其他位置，再使用 Homebrew 安装。剪贴板历史保存在用户资料库中。

## 更新

ClipBar 内置 Sparkle 自动更新。使用 Homebrew 手动更新时，因为 Cask 标记了 `auto_updates true`，需要加上 `--greedy`：

```bash
brew update
brew upgrade --cask --greedy lljxww/clipbar/clipbar
```

此仓库的 GitHub Actions 每 6 小时检查一次 ClipBar 最新稳定版 Release，下载并核对 GitHub 提供的 SHA-256、Release 中的 `SHA256SUMS` 和实际安装包，再更新 Cask。可在 Actions 中手动运行 **Update Cask** 立即同步；不需要额外配置 secret。GitHub 可能在公共仓库长期没有活动时暂停定时工作流，届时可手动重新启用。

## 卸载

```bash
brew uninstall --cask lljxww/clipbar/clipbar
```

以上命令保留剪贴板历史和设置。若要同时删除全部历史、图片缓存和设置：

```bash
brew uninstall --cask --zap lljxww/clipbar/clipbar
```

## 本地维护

```bash
python3 scripts/update-cask.py
brew style Casks/clipbar.rb
```

本 tap 分发项目发布的原始安装包。Homebrew 官方仓库的收录要求见 [Acceptable Casks](https://docs.brew.sh/Acceptable-Casks)。
