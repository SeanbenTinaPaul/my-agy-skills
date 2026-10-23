---
name: ollama-windows-management
description: Procedure for safely moving Ollama model storage to another drive on Windows and disabling auto-start.
---

# Ollama Windows — Move Models to Another Drive & Disable Auto-Start

## Purpose
Use this procedure to safely move Ollama model storage from the default Windows user directory to another drive, while ensuring:
- Ollama models are stored on a dedicated drive such as `D:\AI\Ollama\Models`
- Windows/SSD `C:` is not unnecessarily used for large model files
- Ollama does not automatically start after Windows login
- Ollama uses the intended model directory after reboot
- Existing models are preserved during migration
- Environment-variable conflicts between System and User scopes are detected before making changes

Official Ollama documentation confirms that on Windows the model location can be changed using the `OLLAMA_MODELS` environment variable, and that Ollama inherits both user and system environment variables.

## 1. Target Architecture
Recommended layout:
```text
C:\
├── Windows
├── Applications
├── Ollama program
└── User configuration

D:\
└── AI\
    └── Ollama\
        └── Models\
            ├── manifests\
            └── blobs\
```
Only the large model repository is moved. Do not move the entire Ollama installation unless there is a specific reason to do so.

## 2. Pre-flight: Make Sure Ollama Is Not Running
Before changing model location:
```powershell
Get-Process ollama -ErrorAction SilentlyContinue
```
Expected result: `(no output)`

If Ollama is running, quit Ollama from the system tray first. If it refuses to quit or you are doing this via command line, terminate both the server and the supervisor app simultaneously:
```cmd
taskkill /F /IM "ollama app.exe" /IM ollama.exe
```
Then verify again. Do not repeatedly kill individual PIDs if another process immediately recreates `ollama.exe`. This usually indicates that the Ollama Desktop application or startup mechanism is supervising/restarting the server.

## 3. IMPORTANT: Check All Environment Variable Scopes
Do not immediately create `OLLAMA_MODELS=D:\AI\Ollama\Models` without first checking whether `OLLAMA_MODELS` already exists.
Windows has multiple environment-variable scopes:
`Machine/System` + `User` -> `Process environment` -> `Ollama`

A previous installation or manual configuration may already have created `OLLAMA_MODELS=C:\some\old\path` at the System scope. A different value may also exist at the User scope. Therefore, inspect both scopes before changing anything.

## 4. Check Current Process Environment
Run:
```powershell
$env:OLLAMA_MODELS
```
Possible results:
- **Correct**: `D:\AI\Ollama\Models`
- **Old path**: `C:\Users\<user>\.ollama\models`
- **Empty**: No output means the current PowerShell process does not currently have `OLLAMA_MODELS`.

**Important**: The current process value alone is not enough to determine where the variable came from. Continue with the next checks.

## 5. Check User Environment Variables
Run:
```powershell
[Environment]::GetEnvironmentVariable("OLLAMA_MODELS", "User")
```
This checks the persistent environment variable belonging to the current Windows user.

## 6. Check System/Machine Environment Variables
Run:
```powershell
[Environment]::GetEnvironmentVariable("OLLAMA_MODELS", "Machine")
```
If this returns a value while the User scope also contains a different value, do not assume the configuration is clean. Both scopes must be examined and understood before proceeding.

## 7. Recommended One-Shot Environment Audit
For troubleshooting, the following command is useful:
```powershell
Write-Host "=== OLLAMA_MODELS Environment Audit ==="
Write-Host "`n[Process]"
Write-Host $env:OLLAMA_MODELS
Write-Host "`n[User]"
Write-Host ([Environment]::GetEnvironmentVariable("OLLAMA_MODELS", "User"))
Write-Host "`n[Machine/System]"
Write-Host ([Environment]::GetEnvironmentVariable("OLLAMA_MODELS", "Machine"))
```
Also inspect the registry directly:
```powershell
Write-Host "`n=== User Registry ==="
Get-ItemProperty "HKCU:\Environment" -ErrorAction SilentlyContinue | Select-Object OLLAMA_MODELS
Write-Host "`n=== Machine Registry ==="
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -ErrorAction SilentlyContinue | Select-Object OLLAMA_MODELS
```
This makes it easier to detect an old System-level value that was created before the current User-level configuration.

## 8. Recommended Configuration
For a normal personal Windows installation, use the User scope:
```powershell
[Environment]::SetEnvironmentVariable("OLLAMA_MODELS", "D:\AI\Ollama\Models", "User")
```
Do not unnecessarily create a System-level variable. After changing persistent environment variables, open a new PowerShell window so that the new process inherits the updated environment.

Verify:
```powershell
$env:OLLAMA_MODELS
[Environment]::GetEnvironmentVariable("OLLAMA_MODELS", "User")
```
Expected: `D:\AI\Ollama\Models`

## 9. Check for an Existing System-Level Conflict
Run:
```powershell
[Environment]::GetEnvironmentVariable("OLLAMA_MODELS", "Machine")
```
If it returns an old path, do not blindly delete it. First establish whether it is intentionally used by another account, service, or deployment. For a normal single-user desktop installation, the preferred configuration is:
- **User**: `OLLAMA_MODELS = D:\AI\Ollama\Models`
- **Machine**: `OLLAMA_MODELS = <not defined>`

If the Machine-level variable is obsolete and confirmed unnecessary, it can be removed from an elevated PowerShell:
```powershell
[Environment]::SetEnvironmentVariable("OLLAMA_MODELS", $null, "Machine")
```

## 10. Create the Destination Directory
```powershell
New-Item -ItemType Directory -Force -Path "D:\AI\Ollama\Models"
Test-Path "D:\AI\Ollama\Models"
```

## 11. Preserve the Existing Model Directory
Before moving anything, create a backup/rollback copy. Example: `C:\Users\<user>\.ollama\models_backup`
Do not delete the backup immediately. The backup should remain until the entire migration has been verified, including a Windows reboot.

## 12. Move/Copy the Models
The important requirement is that the final model repository contains the Ollama model structure:
```text
D:\AI\Ollama\Models\
├── manifests\
└── blobs\
```
Do not rename individual blob files. Do not manually reorganize the hash-based blob files. The Ollama model repository must remain structurally intact.

## 13. Verify the Model Repository
Check:
```powershell
Get-ChildItem "D:\AI\Ollama\Models"
Get-ChildItem "D:\AI\Ollama\Models\manifests" -Recurse
```

## 14. Restart Ollama Cleanly
Quit Ollama completely from the system tray. Do not leave an old Ollama server running with the old environment. Then start Ollama again. Official Ollama documentation specifically recommends quitting the tray application and relaunching Ollama after changing environment variables on Windows.

## 15. Verify Models
Run:
```powershell
ollama list
```
The models should appear without needing to download them again. If Ollama shows an empty model list, do not immediately pull the models again. First stop Ollama and investigate the environment variables.

## 16. Verify GPU Usage
Run a model:
```powershell
ollama run <model>
```
Then from another PowerShell:
```powershell
ollama ps
```
Verify that the model is running on the intended GPU. On Windows, Ollama logs are located under `%LOCALAPPDATA%\Ollama\server.log`.

## 17. Disable Ollama Auto-Start
If the goal is `Windows boot -> Ollama OFF`, open:
`Task Manager -> Startup apps -> Ollama -> Disable`
Ollama's current Windows documentation explicitly recommends disabling the Ollama startup item from Task Manager when automatic login startup is not desired.

## 18. Verify the Startup Configuration
Run:
```powershell
Get-CimInstance Win32_StartupCommand | Where-Object { $_.Command -match "Ollama|ollama" } | Format-List Name,Command,Location,User
```
It may still show the startup link, but the authoritative practical check is whether Ollama actually starts after reboot.

## 19. FINAL REBOOT TEST
This step is mandatory before deleting the backup. Restart Windows. After login:
```powershell
Get-Process ollama -ErrorAction SilentlyContinue
```
Expected: `(no output)`
Then check:
```powershell
$env:OLLAMA_MODELS
```
Expected: `D:\AI\Ollama\Models`

## 20. Verify Models After Reboot
Run:
```powershell
ollama list
```
This is an important test because it verifies that the configuration survives a Windows reboot rather than only working inside the current PowerShell session.

## 21. Final Server/GPU Verification
Start Ollama intentionally. Run:
```powershell
ollama run <model>
```
Then `ollama ps`. Verify GPU is detected and expected model is used.

## 22. Only Now Delete the Old Backup
Do not delete `C:\Users\<user>\.ollama\models_backup` until all of these are true:
- [x] Models exist on D:
- [x] OLLAMA_MODELS User variable points to D:
- [x] No unintended System variable overrides/conflicts
- [x] Ollama models are visible
- [x] Models can run
- [x] GPU acceleration works
- [x] Windows has been rebooted
- [x] Ollama does not auto-start
- [x] Models are still accessible after reboot

## 23. Recommended Final Configuration
For a personal Windows desktop:
- **Environment Variables**: User = `D:\AI\Ollama\Models`, System = `<not defined>`
- **Startup**: Ollama -> Disabled
- **Storage**: `D:\AI\Ollama\Models\`
- **Runtime**: Windows boot -> Ollama OFF -> User starts Ollama when needed -> GPU acceleration

## 24. Troubleshooting Decision Tree
### ollama list is empty
Check `$env:OLLAMA_MODELS`, User, and Machine environment variables. Do not immediately download models again.

### Models appear manually but disappear after reboot
Check Ollama auto-start, environment variables, startup shortcut, which process launched `ollama.exe`, and server logs.

### ollama.exe keeps coming back after killing it
Do not repeatedly kill individual PIDs. Check startup/application supervision. Quit Ollama Desktop/tray first.

## 25. Important Principle
The most important troubleshooting principle is: **Never verify only `$env:OLLAMA_MODELS`**. Always verify Process + User + Machine scopes when diagnosing Windows environment-variable problems.
