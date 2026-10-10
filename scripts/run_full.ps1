# =========================================================================
# Script: run_full.ps1
# Description: Chạy pipeline PySpark ở chế độ Full (Toàn bộ 4.446.966 bản ghi)
# =========================================================================

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Red
Write-Host "KHỞI CHẠY BIG DATA PIPELINE PUBG (CHẾ ĐỘ TOÀN BỘ FULL DATASET)" -ForegroundColor Red
Write-Host "==========================================================" -ForegroundColor Red
Write-Host "Lưu ý: Chế độ này xử lý toàn bộ 4.446.966 dòng dữ liệu (~660 MB CSV)." -ForegroundColor Yellow

$env:PYTHONIOENCODING = "utf-8"

python src\pipeline.py --mode full

Write-Host ">>> Pipeline Full hoàn tất! Mở Dashboard bằng lệnh:" -ForegroundColor Cyan
Write-Host "streamlit run dashboard\app.py" -ForegroundColor Yellow
