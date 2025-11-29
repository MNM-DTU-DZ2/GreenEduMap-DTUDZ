@echo off
REM Script để copy assets vào docs/assets trước khi chạy mkdocs serve

REM Tạo thư mục nếu chưa có
if not exist "docs\assets" mkdir docs\assets

REM Copy assets từ root vào docs/assets
xcopy /E /I /Y assets docs\assets

echo ✅ Đã copy assets vào docs/assets/

