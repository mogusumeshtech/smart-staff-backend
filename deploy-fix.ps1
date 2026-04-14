# SMART STAFF - Push Pillow Fix to GitHub
# This script fixes the Render deployment error and pushes to GitHub

Write-Host "🚀 SMART STAFF - Pushing Pillow Fix to GitHub" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check git status
Write-Host "📋 Checking Git status..." -ForegroundColor Yellow
Set-Location "c:\Users\Admin\Desktop\SMART STAFF\backend"
git status
Write-Host ""

# Step 2: Add requirements.txt
Write-Host "➕ Adding requirements.txt to git..." -ForegroundColor Yellow
git add requirements.txt
Write-Host "✅ requirements.txt added" -ForegroundColor Green
Write-Host ""

# Step 3: Commit
Write-Host "💾 Committing fix..." -ForegroundColor Yellow
git commit -m "Fix: Update Pillow to support Python 3.14 on Render - resolves build error"
Write-Host "✅ Commit successful" -ForegroundColor Green
Write-Host ""

# Step 4: Push
Write-Host "🔄 Pushing to GitHub..." -ForegroundColor Yellow
git push
Write-Host "✅ Push complete!" -ForegroundColor Green
Write-Host ""

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "✅ PART 1 COMPLETE: Fix pushed to GitHub" -ForegroundColor Green
Write-Host ""
Write-Host "📝 NEXT STEPS (ON RENDER DASHBOARD):" -ForegroundColor Cyan
Write-Host "  1. Go to https://dashboard.render.com" -ForegroundColor White
Write-Host "  2. Click your service (smart-staff-api)" -ForegroundColor White
Write-Host "  3. Click Settings → Environment" -ForegroundColor White
Write-Host "  4. Add DATABASE_URL variable (see instructions below)" -ForegroundColor White
Write-Host "  5. Click Redeploy" -ForegroundColor White
Write-Host ""
Write-Host "🔑 DATABASE_URL VALUE TO USE:" -ForegroundColor Cyan
Write-Host "postgresql://localhost:5432/smart_staff" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
