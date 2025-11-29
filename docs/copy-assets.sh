#!/bin/bash
# Script để copy assets vào docs/assets trước khi chạy mkdocs serve

# Tạo thư mục nếu chưa có
mkdir -p docs/assets

# Copy assets từ root vào docs/assets
cp -r assets/* docs/assets/ 2>/dev/null || true

echo "✅ Đã copy assets vào docs/assets/"

