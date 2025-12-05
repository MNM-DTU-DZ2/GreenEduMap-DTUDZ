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
