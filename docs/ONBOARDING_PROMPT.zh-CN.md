# 在其他项目中接入统一 Homebrew tap

在目标项目的仓库中，将以下提示词完整交给大模型。无需替换项目名：让它从当前仓库、实际应用包和 GitHub Releases 中识别。

```text
请将当前项目接入我维护的统一 Homebrew tap，并实际完成可安装的发布或迁移。

固定目标：
- GitHub 仓库：https://github.com/mac-fantasy/homebrew-tap
- Homebrew tap：mac-fantasy/tap
- 最终安装命令：brew install --cask mac-fantasy/tap/<当前应用的cask-token>
- 不要为本项目新建独立 tap，也不要把其他应用的 Cask 或配置覆盖掉。

我授权你修改当前项目及 mac-fantasy/homebrew-tap 中与接入有关的文件，在验证通过后提交并推送；若当前项目已有独立 tap，也授权你更新该旧 tap 的迁移说明和映射。保留其他人的未提交修改和远端新增内容，不要强制推送、删除或归档旧仓库。

请完成以下工作：

1. 识别并检查当前项目。
   阅读项目说明、AGENTS.md、构建和 Release 工作流，通过 git remote 与 GitHub 确认真实仓库。检查最新稳定版 Release 是否已有可公开下载的 macOS 安装包。下载实际附件，确认应用名、bundle ID、版本、最低 macOS 版本、支持架构、是否内置自动更新，以及已确认的应用数据目录。不要根据项目名称猜这些值。
   优先复用已有稳定版安装包。若缺少可分发的安装包，先完善必要的构建发布步骤；不要编造下载链接、发布结果或校验值。若缺少确实无法自行取得的权限或凭据，说明准确阻塞点。

2. 接入统一 tap。
   若本机已有 mac-fantasy/homebrew-tap 的工作副本，先检查并复用；否则克隆。读取该仓库的 AGENTS.md、README.md、apps.json、Casks/clipbar.rb、scripts/update-casks.py 和测试，遵循已有组织方式。
   在 Casks/<token>.rb 中添加本应用的 Cask，填写实际的 version、sha256、url、name、desc、homepage、app 或 installer、macOS/架构要求，以及必要的 uninstall 和 zap。下载地址应指向本项目正式 Release。SHA-256 必须来自实际下载并与发布方提供的 digest/校验清单核对；不要使用 sha256 :no_check。
   只有应用确实自行更新时才设置 auto_updates true。普通卸载保留用户数据，只有 --zap 才清理确认属于本应用的数据；不要写泛化的用户目录或共享文件路径。不要在 Cask 中关闭 Gatekeeper、移除 quarantine 或加入多余的 sudo/任意安装脚本。

3. 接入共用自动更新流程。
   向 apps.json 追加当前项目的配置，保留全部已有条目。当前格式以 Cask token 为键，字段为 repository、asset、可选 checksums、可选 tag_pattern；asset 和 checksums 支持 {version} 和 {tag}。默认识别 v1.2.3 或 1.2.3 稳定 tag。version_components 可补齐数字版本段数；原始 tag 与应用版本不同的项目可用 url_from_asset: true 同步实际下载 URL。具体以仓库当前 README 和实现为准。
   更新器当前支持一个安装包、一个顶层 version 和一个顶层 sha256。若当前项目使用分架构安装包、特殊校验格式或其他版本组织方式，请按真实发布方式扩展共用更新器并增加必要测试，保留已有项目行为；不要简单套用 ClipBar 的附件名或把共用工作流改回本项目专用。
   更新统一 tap 的 README 应用列表。沿用 tap 仓库每 6 小时检查 Release 的机制，不要要求每个源项目配置跨仓库 PAT。GitHub Release 安装包仍保存在各项目，不要复制进 tap 仓库。

4. 如有旧 tap，完成迁移。
   先发布并验证新 Cask，再修改旧 tap。保留旧仓库，在 README 写明新的安装命令与已安装用户的切换步骤，并按当前 Homebrew 支持方式添加 tap_migrations.json，例如 {"<token>": "mac-fantasy/tap"}。
   在目标可用后移除旧 tap 的重复 Cask，停止旧的版本同步工作流。若 token 也变化，使用实际目标 token 的迁移映射并验证。
   新版 Homebrew 对新 tap/Cask 需要独立信任，不要承诺旧命令会在任何机器上无交互自动迁移。为已由旧 tap 安装的用户验证 brew tap mac-fantasy/tap、brew reinstall --cask mac-fantasy/tap/<token> 的切换路径；不要使用 --zap 迁移，不要清除用户数据。

5. 更新当前项目文档。
   添加统一 tap 的安装、更新和卸载命令。若 auto_updates true，说明通过 Homebrew 手动更新需要 --greedy。如有签名或公证限制，准确写明当前状态。若系统中已有手动安装的同名应用，说明接入 Homebrew 前如何处理已有应用，避免宣称可以无条件覆盖安装。

6. 验证并发布。
   在统一 tap 中运行已有测试、python3 scripts/update-casks.py <token> 和 brew style Casks/<token>.rb。在可用的 macOS/Homebrew 环境中验证完整名称的 info、在线 audit 和 install --dry-run，并实际下载核对安装包。不要为了测试而覆盖、退出或卸载我正在使用的应用；如需解包检查，使用临时目录。
   核对旧入口的迁移行为并运行统一 tap 的 CI/更新工作流。提交前检查 diff，推送前获取远端最新内容并正常合并或变基，只提交本任务的修改。若其他项目同时接入导致冲突，合并所有应用条目，禁止用整份旧文件覆盖远端。
   最终报告：准确的安装/更新命令、Cask 与相关提交或工作流链接、是否迁移了旧 tap、执行过的验证，以及仍需我处理的真实限制。请实际完成工作，不要只给方案。
```
