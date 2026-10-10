# =========================================================================
# Script: run_quick.ps1
# Description: Chạy pipeline PySpark ở chế độ Quick (94.428 bản ghi / 1.000 trận)
# =========================================================================

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Green
Write-Host "KHỞI CHẠY BIG DATA PIPELINE PUBG (CHẾ ĐỘ QUICK DEMO)" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

# Thiết lập biến môi trường
$env:PYTHONIOENCODING = "utf-8"

python src\pipeline.py --mode quick

Write-Host ">>> Pipeline Quick hoàn tất! Để mở Dashboard, chạy:" -ForegroundColor Cyan
Write-Host "streamlit run dashboard\app.py" -ForegroundColor Yellow
