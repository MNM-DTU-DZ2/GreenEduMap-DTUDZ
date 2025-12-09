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

// Đã bỏ Mapbox. Component này hiển thị placeholder đơn giản, không còn phụ thuộc mapbox-gl.

export interface Coordinates {
  lat: number;
  lng: number;
}

interface MapLocationPickerProps {
  value: Coordinates | null;
  onChange: (coords: Coordinates | null) => void;
  isActive: boolean;
  interactive?: boolean;
  height?: number;
  markerColor?: string;
  instructions?: string;
}

const MapLocationPicker: React.FC<MapLocationPickerProps> = ({
  value,
}) => {
  return (
    <div className="flex h-[260px] w-full flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-gray-300 bg-gray-50 text-center text-sm text-gray-500 dark:border-white/[0.08] dark:bg-gray-900/40 dark:text-gray-400">
      <p>Bản đồ chọn vị trí (Mapbox) đã được tắt.</p>
      {value && (
        <p className="text-xs text-gray-600 dark:text-gray-300">
          Vị trí hiện tại: lat {value.lat}, lng {value.lng}
        </p>
      )}
    </div>
  );
};

export default MapLocationPicker;
