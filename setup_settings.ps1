# Migration script for Settings Tab feature (Windows PowerShell)

Write-Host "🔧 Running database migrations for Settings Tab..." -ForegroundColor Cyan
Write-Host ""

# Navigate to script directory
Set-Location $PSScriptRoot

# Create migrations
Write-Host "📝 Creating migrations..." -ForegroundColor Yellow
python manage.py makemigrations chat_moderator

# Apply migrations
Write-Host "✅ Applying migrations..." -ForegroundColor Green
python manage.py migrate

Write-Host ""
Write-Host "✨ Migrations complete! You can now use the Settings tab." -ForegroundColor Green
Write-Host "🚀 Restart your Django server if it's running." -ForegroundColor Cyan
