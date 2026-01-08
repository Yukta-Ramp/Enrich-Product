# Product Enrichment V2 - Backend Setup Script
# Run this script to set up the backend environment

Write-Host "Setting up Product Enrichment V2 Backend..." -ForegroundColor Green

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your Azure OpenAI credentials"
Write-Host "2. Run: uvicorn app.main:app --reload --port 8000"
Write-Host "`nAPI Documentation will be available at: http://localhost:8000/docs" -ForegroundColor Cyan
