# 1. 环境初始化与编码设置
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Stop-Run {
    Write-Host "`n[Process Finished] Press any key to exit..." -ForegroundColor Gray
    $null = [Console]::ReadKey($true)
    exit
}

# 2. 博世 Px 代理逻辑：确保 Git 能联网
Write-Host ">> Checking Bosch PX Proxy..." -ForegroundColor Cyan
$pxPort = 3128
$pxAccessible = (Test-NetConnection -ComputerName 127.0.0.1 -Port $pxPort -ErrorAction SilentlyContinue).TcpTestSucceeded

if (!$pxAccessible) {
    Write-Host ">> Starting PX Proxy..." -ForegroundColor Yellow
    # 这里的参数根据你提供的脚本进行了还原
    Start-Process -FilePath "C:\Program Files\Px\px.exe" -WindowStyle Hidden -ArgumentList "--pac=http://rbins-ap.bosch.com/hk.pac", "--foreground=1", "--log=4"
    Start-Sleep -Seconds 3
} else {
    Write-Host ">> PX Proxy is already running." -ForegroundColor Green
}

# 注入代理环境变量给当前的 Git 进程使用
$env:http_proxy = "http://127.0.0.1:$pxPort"
$env:https_proxy = "http://127.0.0.1:$pxPort"

try {
    # 3. 切换到项目目录
    $path = "C:\Users\EJI1WX\OneDrive - Bosch Group\PythonProject\SourceCodeBinder"
    Set-Location -Path $path

    # 4. 配置身份
    git config user.name "jiedi720"
    Write-Host "`n--- Ready to Upload SourceCodeBinder ---" -ForegroundColor Cyan

    # 5. Git 流程
    Write-Host ">> Adding files..."
    git add .

    $msg = Read-Host "Enter Commit Message (Default: Daily Update)"
    if ([string]::IsNullOrWhiteSpace($msg)) { $msg = "Daily Update" }

    Write-Host ">> Committing..."
    git commit -m $msg

    Write-Host ">> Pushing to GitHub (via PX Proxy)..." -ForegroundColor Yellow
    # 强制推送
    git push -u origin main --force

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Success! Files are now on GitHub." -ForegroundColor Green
    } else {
        Write-Host "`n❌ Failed! Even with PX, there's a connection issue." -ForegroundColor Red
    }

} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Stop-Run