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

'use client';

// Đã bỏ Mapbox. Component này chỉ là placeholder, không còn phụ thuộc mapbox-gl.

interface MapboxMapProps {
  className?: string;
}

const MapboxMap: React.FC<MapboxMapProps> = ({ className = '' }) => {
  return (
    <div
      className={`flex h-full w-full items-center justify-center rounded-lg border border-dashed border-gray-300 bg-white/60 p-4 text-sm text-gray-500 ${className}`}
    >
      Bản đồ demo (Mapbox) đã được tắt. Hãy sử dụng bản đồ chính tại{" "}
      <a href="/map" className="text-success-600 underline">
        /map
      </a>.
    </div>
  );
};

export default MapboxMap;
