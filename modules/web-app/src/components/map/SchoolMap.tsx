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

// Đã bỏ Mapbox. Component này chỉ hiển thị ô tìm kiếm + message, không còn phụ thuộc mapbox-gl.

import SchoolSearch from "@/components/search/SchoolSearch";

export default function SchoolMap() {
  return (
    <div className="relative flex h-full w-full flex-col items-center justify-center rounded-lg border border-dashed border-gray-300 bg-white/60 p-6 text-sm text-gray-600">
      <p className="mb-3 font-semibold text-gray-700">
        SchoolMap (Mapbox) đã được tắt.
      </p>
      <p className="mb-4 text-xs text-gray-500">
        Vui lòng sử dụng bản đồ chính tại{" "}
        <a href="/map" className="text-success-600 underline">
          /map
        </a>.
      </p>
      <div className="w-full max-w-xs sm:max-w-md">
        <SchoolSearch onSelectSchool={() => {}} />
      </div>
    </div>
  );
}
