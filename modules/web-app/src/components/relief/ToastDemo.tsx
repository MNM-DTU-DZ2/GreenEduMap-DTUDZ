/*
 * GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
 * Copyright (C) 2025 DTU-DZ2 Team
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

"use client";

import { useToast } from "@/context/ToastContext";

/**
 * Demo component to test toast notifications
 * Có thể thêm vào dashboard để test
 */
export default function ToastDemo() {
  const { success, error, warning, info } = useToast();

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        🎨 Toast Notification Demo
      </h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button
          onClick={() => success("✅ Thao tác thành công!")}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          Success
        </button>

        <button
          onClick={() => error("❌ Có lỗi xảy ra!")}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          Error
        </button>

        <button
          onClick={() => warning("⚠️ Cảnh báo quan trọng!")}
          className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          Warning
        </button>

        <button
          onClick={() => info("ℹ️ Thông tin hữu ích")}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          Info
        </button>
      </div>

      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <button
          onClick={() => success("Hiển thị 3 giây", 3000)}
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors text-sm"
        >
          Quick Toast (3s)
        </button>

        <button
          onClick={() => error("Hiển thị 10 giây", 10000)}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors text-sm"
        >
          Long Toast (10s)
        </button>
      </div>

      <div className="mt-4">
        <button
          onClick={() => {
            success("Toast 1");
            setTimeout(() => error("Toast 2"), 200);
            setTimeout(() => warning("Toast 3"), 400);
            setTimeout(() => info("Toast 4"), 600);
          }}
          className="w-full bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          Multiple Toasts
        </button>
      </div>
    </div>
  );
}

