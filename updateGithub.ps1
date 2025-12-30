# 设置 UTF8 编码
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Stop-Run {
    Write-Host "`n[Process Finished] Press any key to exit..." -ForegroundColor Gray
    $null = [Console]::ReadKey($true)
    exit
}

try {
    $path = "C:\Users\EJI1WX\OneDrive - Bosch Group\PythonProject\SourceCodeBinder"
    Set-Location -Path $path

    # 配置身份
    git config user.name "jiedi720"
    Write-Host "--- Ready to Upload ---" -ForegroundColor Cyan

    # 执行流程
    git add .
    $msg = Read-Host "Enter Commit Message (Default: Daily Update)"
    if ([string]::IsNullOrWhiteSpace($msg)) { $msg = "Daily Update" }

    git commit -m $msg
    Write-Host "--- Pushing to GitHub ---" -ForegroundColor Yellow
    git push -u origin main --force

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Success!" -ForegroundColor Green
    } else {
        Write-Host "Failed! Check network or proxy." -ForegroundColor Red
    }
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Stop-Run