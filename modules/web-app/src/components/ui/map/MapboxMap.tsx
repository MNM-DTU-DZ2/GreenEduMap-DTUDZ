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
