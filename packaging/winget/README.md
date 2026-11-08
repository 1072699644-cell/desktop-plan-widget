# winget 清单（骨架，未完成）

这是把 Plan Card 提交到 [winget-pkgs](https://github.com/microsoft/winget-pkgs) 的三件套。
文件都在这里，但**还不能直接提交**——下面标了必须你自己填的东西。

## 先说清楚这条路的问题

winget 的 portable 包装的是"绿色软件 + 一个命令"。Plan Card 是 `.pyw` 脚本，
**必须先装 Python 3.8+** 才能跑。winget 不会替你装 Python。

这意味着两条路：

| 方案 | 可行性 | 说明 |
|---|---|---|
| portable zip 指向 `.pyw` | 存疑 | 依赖用户已关联 `.pyw` 到 pythonw.exe。多数装过 Python 的机器可以，但没有 Python 的裸机会失败，评审可能质疑 |
| portable zip 指向一个 `.cmd` 启动器 | 较稳 | 包里放 `plancard.cmd`，内容先检查 `pythonw` 是否存在，不存在就给提示。**推荐走这条** |

推荐做法：在发布用的 zip 里加一个 `plancard.cmd`：

```bat
@echo off
where pythonw >nul 2>nul
if errorlevel 1 (
  echo Plan Card needs Python 3.8+. Install it from https://www.python.org/downloads/
  pause
  exit /b 1
)
start "" pythonw "%~dp0plan_card.pyw"
```

然后把 `installer.yaml` 里的 `NestedInstallerFiles` 改成指向 `plancard.cmd`，
`PortableCommandAlias` 用 `plancard`。

## 提交前必须做的四件事

1. **打 tag。** 清单里的 `InstallerUrl` 指向一个 release zip，现在仓库还没有 tag：
   ```
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **算出 SHA256。** 下载压缩包后：
   ```powershell
   (Get-FileHash .\v1.0.0.zip -Algorithm SHA256).Hash
   ```
   填进 `PlanCard.PlanCard.installer.yaml` 的 `InstallerSha256`。**这个值每次发版都要重算**。

3. **确认 PackageIdentifier 可用。** 提交前先搜一遍，避免撞车：
   ```
   winget search PlanCard
   ```

4. **提交 PR。** 目录结构必须是：
   ```
   manifests/p/PlanCard/PlanCard/1.0.0/
       PlanCard.PlanCard.yaml
       PlanCard.PlanCard.installer.yaml
       PlanCard.PlanCard.locale.en-US.yaml
   ```
   然后用 `winget validate` 本地校验：
   ```powershell
   winget validate --manifest .\packaging\winget\
   ```

## 预期收益

诚实说：winget 里搜得到你，约等于每天可能有一两个人 `winget search sticky` / `winget search plan`
时看到你的名字。不会带来爆发，但成本很低、结果长期有效。

## 现在还没做的

- [ ] 上面那个 `plancard.cmd` 启动器
- [ ] git tag
- [ ] SHA256
- [ ] `winget validate` 跑通
- [ ] 提 PR
