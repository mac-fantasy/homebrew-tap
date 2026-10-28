# lljxww Homebrew Tap

统一维护 [lljxww](https://github.com/lljxww) 的 Mac 工具安装源。每个应用有独立的 Cask，安装包继续由各项目的 GitHub Releases 发布。

## 应用与安装

| 应用 | 项目 | 安装命令 |
| --- | --- | --- |
| ClipBar | [菜单栏剪贴板历史工具](https://github.com/lljxww/ClipBar) | `brew install --cask lljxww/tap/clipbar` |

使用完整名称安装时，Homebrew 会自动添加此 tap 并信任指定的 Cask。也可以先运行 `brew tap lljxww/tap`，再使用上表中的完整安装命令。参见 [Homebrew Tap Trust](https://docs.brew.sh/Tap-Trust)。

ClipBar 支持 macOS 13 及以上、Apple Silicon 和 Intel。当前 ClipBar 使用 ad-hoc 签名，尚未做 Apple Developer ID 签名和公证；macOS 可能阻止首次打开，请确认安装来源后按「系统设置 → 隐私与安全性」中的提示允许打开。各应用的签名和系统要求以各自项目说明为准。

如果已手动安装 ClipBar，请先退出应用，并将已有的 `/Applications/ClipBar.app` 移到其他位置后再使用 Homebrew 安装。剪贴板历史保存在用户资料库中。

## 从旧 ClipBar tap 切换

已通过 `lljxww/clipbar/clipbar` 安装的用户可以执行：

```bash
brew update
brew tap lljxww/tap
brew reinstall --cask lljxww/tap/clipbar
brew untap lljxww/clipbar
```

重新安装会退出 ClipBar 并更新安装来源，保留剪贴板历史和设置。旧仓库保留 `tap_migrations.json` 和迁移说明；新的 tap 需要独立的信任授权，旧入口可能先提示添加或信任新安装源，请优先使用以上命令。

## 更新与卸载

```bash
brew update
brew upgrade --cask --greedy lljxww/tap/clipbar
brew uninstall --cask lljxww/tap/clipbar
```

ClipBar 内置 Sparkle 自动更新，Cask 标记了 `auto_updates true`，因此通过 Homebrew 手动升级时需要 `--greedy`。普通卸载保留历史和设置；`brew uninstall --cask --zap lljxww/tap/clipbar` 会同时删除这些数据。

## 自动同步 Release

GitHub Actions 的 **Update Casks** 每 6 小时检查 `apps.json` 中所有项目的最新稳定版 Release，也可以手动运行。它下载实际安装包，核对 GitHub 的 SHA-256 digest 及配置的校验清单，再修改对应 Cask 的版本号与 SHA-256。全部选中应用通过校验后才写入文件；出现异常时工作流失败并保留已有定义。

工作流只使用本仓库的 `GITHUB_TOKEN`，不需要各应用配置跨仓库 secret。公共仓库长期没有活动时，GitHub 可能暂停定时工作流，届时可手动重新启用。

## 接入其他项目

可直接复制 [其他项目接入提示词](docs/ONBOARDING_PROMPT.zh-CN.md)，交给其他项目中的大模型执行。维护约定见 [AGENTS.md](AGENTS.md)。

1. 在 `Casks/<token>.rb` 添加应用的独立 Cask，使用项目正式 Release 的下载地址和实际校验值。
2. 在 `apps.json` 追加自动更新配置，保留已有应用：

   ```json
   {
     "another-app": {
       "repository": "lljxww/AnotherApp",
       "asset": "AnotherApp-{version}-macOS-universal.zip",
       "checksums": "SHA256SUMS"
     }
   }
   ```

   以上名称仅作示例。`asset` 支持 `{version}` 和 `{tag}`；`checksums` 可省略，省略时要求 GitHub 提供安装包的 SHA-256 digest。校验清单支持标准 `shasum -a 256` / `sha256sum` 格式。默认接受 `v1.2.3` 或 `1.2.3` 格式的稳定 tag；其他 tag 格式可通过带 `version` 命名捕获组的 `tag_pattern` 配置。

3. 更新应用列表、源项目安装说明，并验证后提交。

```bash
python3 -m unittest discover -s tests
python3 scripts/update-casks.py          # 同步全部应用
python3 scripts/update-casks.py clipbar  # 只同步 ClipBar
brew style Casks/*.rb
```

当前更新器适用于单一安装包、一个顶层 `version` 和一个顶层 `sha256` 的 Cask。若新项目分架构发布或使用其他版本组织方式，需要保留正确的 Cask 结构并扩展更新器及测试，不应套用错误的通用包配置。
