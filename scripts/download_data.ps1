# =========================================================================
# Script: download_data.ps1
# Description: Tải và giải nén bộ dữ liệu PUBG từ Kaggle bằng Kaggle CLI
# =========================================================================

$ErrorActionPreference = "Stop"

Write-Host ">>> [1/3] Kiểm tra công cụ Kaggle CLI..." -ForegroundColor Cyan
if (-not (Get-Command kaggle -ErrorAction SilentlyContinue)) {
    Write-Error "Không tìm thấy Kaggle CLI. Vui lòng cài đặt và xác thực kaggle.json trước khi chạy."
}

$rawDir = "data\raw"
if (-not (Test-Path $rawDir)) {
    New-Item -ItemType Directory -Force -Path $rawDir | Out-Null
}

$targetZip = Join-Path $rawDir "train_V2.csv.zip"
$targetCsv = Join-Path $rawDir "train_V2.csv"

if (Test-Path $targetCsv) {
    Write-Host ">>> Bộ dữ liệu $targetCsv đã tồn tại. Bỏ qua bước tải." -ForegroundColor Green
} else {
    Write-Host ">>> [2/3] Đang tải train_V2.csv từ Kaggle Competition 'pubg-finish-placement-prediction'..." -ForegroundColor Cyan
    kaggle competitions download -c pubg-finish-placement-prediction -f train_V2.csv -p $rawDir

    Write-Host ">>> [3/3] Đang giải nén tập tin..." -ForegroundColor Cyan
    Expand-Archive -Path $targetZip -DestinationPath $rawDir -Force
    Write-Host ">>> Giải nén thành công $targetCsv!" -ForegroundColor Green
}
