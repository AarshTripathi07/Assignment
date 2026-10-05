# Refresh PATH to include newly installed Git
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "Pushing all project files to GitHub..." -ForegroundColor Cyan
git push -u origin main
