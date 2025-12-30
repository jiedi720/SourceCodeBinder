# 1. 基础设置
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 定义简单的退出函数
function Stop-Run {
    Write-Host "--- 进程结束，按任意键关闭 ---" -ForegroundColor Gray
    $null = [Console]::ReadKey($true)
    exit
}

# 2. 核心逻辑
try {
    $path = "C:\Users\EJI1WX\OneDrive - Bosch Group\PythonProject\SourceCodeBinder"
    if (Test-Path $path) {
        Set-Location -Path $path
    } else {
        Write-Host "Error: Path not found!"
        Stop-Run
    }

    # 配置 Git
    git config user.name "jiedi720"
    Write-Host "--- Ready to Upload ---" -ForegroundColor Cyan

    # Git 流程
    git add .
    $msg = Read-Host "Enter Commit Message (Default: Daily Update)"
    if ([string]::IsNullOrWhiteSpace($msg)) { $msg = "Daily Update" }

    git commit -m $msg
    Write-Host "--- Pushing to GitHub ---" -ForegroundColor Yellow
    git push -u origin main --force

    # 结果判断 (注意格式，不要换行)
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Success!" -ForegroundColor Green
    } else {
        Write-Host "Failed!" -ForegroundColor Red
    }

} catch {
    Write-Host "Critical Error Occurred!" -ForegroundColor Red
    Write-Host $_.Exception.Message
}

# 3. 停留在窗口
Stop-Run