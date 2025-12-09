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

// Placeholder MapView: Mapbox implementation đã được gỡ bỏ để tránh phụ thuộc `mapbox-gl`.
// Component này chỉ hiển thị thống kê đơn giản từ danh sách markers.

type MarkerType = "request" | "center" | "distribution";

interface ReliefMarker {
  id: number | string;
  title: string;
  type: MarkerType;
  priority?: string | null;
  status?: string | null;
}

interface MapViewProps {
  markers?: ReliefMarker[];
}

export default function MapView({ markers = [] }: MapViewProps) {
  const totals = {
    request: markers.filter((m) => m.type === "request").length,
    center: markers.filter((m) => m.type === "center").length,
    distribution: markers.filter((m) => m.type === "distribution").length,
  };

  const urgentRequests = markers.filter(
    (m) => m.type === "request" && (m.priority === "cao" || m.priority === "high"),
  ).length;

  return (
    <div className="flex h-full w-full flex-col justify-between rounded-lg border border-dashed border-gray-300 bg-white/70 p-4 text-sm text-gray-700">
      <div>
        <p className="mb-2 font-semibold">Bản đồ cứu trợ (Mapbox) đã được tắt.</p>
        <p className="mb-4 text-xs text-gray-500">
          Dữ liệu vẫn được hiển thị dạng thống kê. Sau này có thể chuyển sang MapTiler giống
          trang <a href="/map" className="text-success-600 underline">/map</a>.
        </p>
      </div>
      <div className="space-y-1 text-xs">
        <div className="flex items-center justify-between">
          <span>Yêu cầu cứu trợ</span>
          <span className="font-semibold">{totals.request}</span>
        </div>
        <div className="flex items-center justify-between">
          <span>Trung tâm cứu trợ</span>
          <span className="font-semibold">{totals.center}</span>
        </div>
        <div className="flex items-center justify-between">
          <span>Phân phối nguồn lực</span>
          <span className="font-semibold">{totals.distribution}</span>
        </div>
        {urgentRequests > 0 && (
          <div className="mt-2 rounded bg-red-100 px-2 py-1 text-[11px] font-medium text-red-600">
            Ưu tiên cao: {urgentRequests}
          </div>
        )}
      </div>
    </div>
  );
}


