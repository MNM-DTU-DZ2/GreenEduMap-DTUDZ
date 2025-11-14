"use client";

import { useState, Suspense, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import PublicHeader from "@/components/common/PublicHeader";
import { MapPin, TrendingUp, Leaf, School, X } from "lucide-react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

// Set Mapbox token
if (typeof window !== "undefined") {
  const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;
  if (token) {
    mapboxgl.accessToken = token;
  }
}

// Mock data for AI correlation between environment and education
const mockAIData = [
  {
    id: 1,
    ward_name: "Phường Bến Nghé",
    district: "Quận 1",
    latitude: 10.7769,
    longitude: 106.7009,
    aqi: 85,
    education_score: 82,
    correlation: 0.75,
    recommended_actions: ["Trồng cây xanh", "Cải thiện hệ thống thông gió"],
    impact_score: 8.5,
  },
  {
    id: 2,
    ward_name: "Phường Đa Kao",
    district: "Quận 1",
    latitude: 10.7889,
    longitude: 106.6992,
    aqi: 92,
    education_score: 78,
    correlation: 0.68,
    recommended_actions: ["Lắp đặt máy lọc không khí", "Giáo dục môi trường"],
    impact_score: 7.8,
  },
  {
    id: 3,
    ward_name: "Phường Bình Hưng Hòa",
    district: "Quận Bình Tân",
    latitude: 10.7589,
    longitude: 106.6000,
    aqi: 115,
    education_score: 72,
    correlation: 0.85,
    recommended_actions: ["Giảm khí thải giao thông", "Chương trình giáo dục xanh"],
    impact_score: 9.2,
  },
  {
    id: 4,
    ward_name: "Phường An Lạc",
    district: "Quận Bình Tân",
    latitude: 10.7500,
    longitude: 106.5933,
    aqi: 145,
    education_score: 68,
    correlation: 0.92,
    recommended_actions: ["Trồng cây xanh", "Cải thiện chất lượng không khí", "Giáo dục môi trường"],
    impact_score: 9.8,
  },
  {
    id: 5,
    ward_name: "Phường Tân Tạo",
    district: "Quận Bình Tân",
    latitude: 10.7556,
    longitude: 106.5978,
    aqi: 135,
    education_score: 70,
    correlation: 0.88,
    recommended_actions: ["Năng lượng tái tạo", "Giáo dục xanh"],
    impact_score: 9.5,
  },
];

function ActionsContent() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<mapboxgl.Map | null>(null);
  const [isMapLoaded, setIsMapLoaded] = useState(false);
  const [selectedWard, setSelectedWard] = useState<any>(null);
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const [hoveredWard, setHoveredWard] = useState<any>(null);

  // Convert mock data to GeoJSON
  const correlationGeoJSON = {
    type: "FeatureCollection" as const,
    features: mockAIData.map((ward) => ({
      type: "Feature" as const,
      geometry: {
        type: "Point" as const,
        coordinates: [ward.longitude, ward.latitude],
      },
      properties: {
        value: ward.correlation * 100, // Convert to percentage
        ...ward,
      },
    })),
  };

  // Initialize Map
  useEffect(() => {
    if (!mapContainer.current || mapRef.current) return;

    const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;
    if (!token) {
      console.error("Mapbox token not found");
      return;
    }

    mapboxgl.accessToken = token;

    const map = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/light-v11",
      center: [106.6297, 10.8231], // TP.HCM
      zoom: 11,
      pitch: 45,
      bearing: -17.6,
    });

    mapRef.current = map;

    map.on("load", () => {
      setIsMapLoaded(true);

      // Add Correlation Heatmap Source & Layer
      map.addSource("correlation-heatmap", {
        type: "geojson",
        data: correlationGeoJSON,
      });

      map.addLayer({
        id: "correlation-heatmap",
        type: "heatmap",
        source: "correlation-heatmap",
        maxzoom: 15,
        layout: { visibility: "visible" },
        paint: {
          "heatmap-weight": [
            "interpolate",
            ["linear"],
            ["get", "value"],
            0,
            0,
            60,
            0.3,
            80,
            0.7,
            100,
            1,
          ],
          "heatmap-color": [
            "interpolate",
            ["linear"],
            ["heatmap-density"],
            0,
            "rgba(34, 197, 94, 0)", // Green (low correlation)
            0.3,
            "rgba(34, 197, 94, 0.5)",
            0.5,
            "rgba(251, 191, 36, 0.7)", // Yellow (medium)
            0.7,
            "rgba(249, 115, 22, 0.8)", // Orange
            1,
            "rgba(239, 68, 68, 1)", // Red (high correlation)
          ],
          "heatmap-radius": 60,
          "heatmap-opacity": 0.85,
        },
      });

      // Add Circles for click interaction
      map.addLayer({
        id: "correlation-circles",
        type: "circle",
        source: "correlation-heatmap",
        paint: {
          "circle-radius": [
            "interpolate",
            ["linear"],
            ["get", "value"],
            0,
            8,
            100,
            25,
          ],
          "circle-color": [
            "interpolate",
            ["linear"],
            ["get", "value"],
            0,
            "#22c55e", // Green
            60,
            "#fbbf24", // Yellow
            80,
            "#f97316", // Orange
            100,
            "#ef4444", // Red
          ],
          "circle-opacity": 0.6,
          "circle-stroke-width": 2,
          "circle-stroke-color": "#fff",
        },
      });

      // Click handler
      map.on("click", "correlation-circles", (e) => {
        const feature = e.features?.[0];
        if (!feature) return;

        const wardData = feature.properties as any;
        // Find the full ward data from mockAIData to ensure all properties are available
        const fullWardData = mockAIData.find(w => w.id === wardData.id) || wardData;

        // Ensure recommended_actions is always an array
        let recommendedActions = [];
        if (Array.isArray(fullWardData.recommended_actions)) {
          recommendedActions = fullWardData.recommended_actions;
        } else if (typeof fullWardData.recommended_actions === 'string') {
          try {
            recommendedActions = JSON.parse(fullWardData.recommended_actions);
            if (!Array.isArray(recommendedActions)) {
              recommendedActions = [];
            }
          } catch {
            recommendedActions = [];
          }
        }

        const wardWithActions = {
          ...fullWardData,
          recommended_actions: recommendedActions
        };

        setSelectedWard(wardWithActions);
        setIsDetailOpen(true);

        // Show popup
        new mapboxgl.Popup()
          .setLngLat(e.lngLat)
          .setHTML(`
            <div class="p-2">
              <h3 class="font-semibold text-gray-900 mb-1">${wardWithActions.ward_name}</h3>
              <p class="text-sm text-gray-600">${wardWithActions.district}</p>
              <p class="text-sm mt-1">
                <span class="font-medium">Tương quan: </span>
                <span class="font-bold text-red-600">${(wardWithActions.correlation * 100).toFixed(0)}%</span>
              </p>
            </div>
          `)
          .addTo(map);
      });

      // Hover handlers
      map.on("mouseenter", "correlation-circles", () => {
        map.getCanvas().style.cursor = "pointer";
      });

      map.on("mouseleave", "correlation-circles", () => {
        map.getCanvas().style.cursor = "";
      });

      map.on("mousemove", "correlation-circles", (e) => {
        const feature = e.features?.[0];
        if (!feature) return;

        const wardData = feature.properties as any;
        setHoveredWard(wardData);
      });
    });

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  const handleWardClick = (ward: any) => {
    setSelectedWard(ward);
    setIsDetailOpen(true);

    // Fly to location on map
    if (mapRef.current && isMapLoaded) {
      mapRef.current.flyTo({
        center: [ward.longitude, ward.latitude],
        zoom: 14,
        duration: 1500,
      });
    }
  };

  const getCorrelationColor = (correlation: number) => {
    if (correlation >= 0.8) return "text-red-600 bg-red-50 dark:bg-red-900/20";
    if (correlation >= 0.6) return "text-orange-600 bg-orange-50 dark:bg-orange-900/20";
    return "text-green-600 bg-green-50 dark:bg-green-900/20";
  };

  const getAQIColor = (aqi: number) => {
    if (aqi > 150) return "text-red-600";
    if (aqi > 100) return "text-orange-600";
    if (aqi > 50) return "text-yellow-600";
    return "text-green-600";
  };

  // Calculate summary stats
  const avgCorrelation = mockAIData.reduce((sum, w) => sum + w.correlation, 0) / mockAIData.length;
  const avgAQI = mockAIData.reduce((sum, w) => sum + w.aqi, 0) / mockAIData.length;
  const avgEducation = mockAIData.reduce((sum, w) => sum + w.education_score, 0) / mockAIData.length;
  const totalActions = mockAIData.reduce((sum, w) => sum + w.recommended_actions.length, 0);

  return (
    <div className="relative w-full min-h-screen bg-gray-50 dark:bg-gray-900">
      <PublicHeader />

      <div className="pt-20 sm:pt-24">
        <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          {/* Intro Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <h2 className="mb-2 text-3xl font-bold text-gray-900 dark:text-white">
              Hành động xanh được đề xuất bởi AI
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Phân tích tương quan giữa môi trường và giáo dục để đề xuất hành động xanh hiệu quả
            </p>
          </motion.div>

          {/* Summary Cards */}
          <div className="grid grid-cols-1 gap-4 mb-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              {
                label: "Tương quan trung bình",
                value: `${(avgCorrelation * 100).toFixed(1)}%`,
                color: "success",
                icon: TrendingUp
              },
              {
                label: "AQI trung bình",
                value: avgAQI.toFixed(0),
                color: "warning",
                icon: MapPin
              },
              {
                label: "Chỉ số giáo dục",
                value: `${avgEducation.toFixed(0)}/100`,
                color: "purple",
                icon: School
              },
              {
                label: "Tổng hành động",
                value: totalActions.toString(),
                color: "success",
                icon: Leaf
              },
            ].map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                      {stat.label}
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      {stat.value}
                    </p>
                  </div>
                  <stat.icon className={`w-8 h-8 ${
                    stat.color === "success" ? "text-success-600 dark:text-success-400" :
                    stat.color === "warning" ? "text-warning-600 dark:text-warning-400" :
                    stat.color === "purple" ? "text-purple-600 dark:text-purple-400" :
                    "text-blue-600 dark:text-blue-400"
                  }`} />
                </div>
              </motion.div>
            ))}
          </div>

          {/* Map and Table Grid Layout */}
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3 mb-6">
            {/* Map Section - Takes 2 columns on large screens */}
            <div className="lg:col-span-2">
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="relative h-[500px] lg:h-[600px] bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden border border-gray-200 dark:border-gray-700"
              >
                <div ref={mapContainer} className="w-full h-full" />

                {/* Map Overlay Info */}
                {hoveredWard && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className="absolute top-4 left-4 p-3 bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl rounded-lg shadow-xl z-10 max-w-xs border border-gray-200 dark:border-gray-700"
                  >
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2 text-sm">
                      {hoveredWard.ward_name}
                    </h3>
                    <div className="space-y-1 text-xs">
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">AQI:</span>
                        <span className={`font-semibold ${getAQIColor(hoveredWard.aqi)}`}>
                          {hoveredWard.aqi}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">Giáo dục:</span>
                        <span className="font-semibold text-gray-900 dark:text-white">
                          {hoveredWard.education_score}/100
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">Tương quan:</span>
                        <span className={`font-semibold ${getCorrelationColor(hoveredWard.correlation).split(' ')[0]}`}>
                          {(hoveredWard.correlation * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                  </motion.div>
                )}

                {/* Legend */}
                <div className="absolute bottom-4 right-4 p-3 bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl rounded-lg shadow-xl z-10 border border-gray-200 dark:border-gray-700 max-w-[180px]">
                  <h4 className="text-xs font-semibold text-gray-900 dark:text-white mb-2">
                    Chú giải Tương quan
                  </h4>
                  <div className="space-y-1.5 text-xs">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-red-500 border border-white shadow-sm" />
                      <span className="text-gray-700 dark:text-gray-300">Cao (≥80%)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-orange-500 border border-white shadow-sm" />
                      <span className="text-gray-700 dark:text-gray-300">TB (60-79%)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-yellow-500 border border-white shadow-sm" />
                      <span className="text-gray-700 dark:text-gray-300">Thấp (40-59%)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-green-500 border border-white shadow-sm" />
                      <span className="text-gray-700 dark:text-gray-300">Rất thấp (&lt;40%)</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            </div>

            {/* Table Section - Takes 1 column on large screens */}
            <div className="lg:col-span-1">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden h-[500px] lg:h-[600px] flex flex-col"
              >
                <div className="p-4 border-b border-gray-200 dark:border-gray-700 sticky top-0 bg-white dark:bg-gray-800 z-10">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    Danh sách khu vực
                  </h3>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {mockAIData.length} khu vực được phân tích
                  </p>
                </div>
                <div className="overflow-y-auto flex-1">
                  <div className="divide-y divide-gray-200 dark:divide-gray-700">
                    {mockAIData.map((ward) => (
                      <div
                        key={ward.id}
                        onClick={() => handleWardClick(ward)}
                        onMouseEnter={() => setHoveredWard(ward)}
                        onMouseLeave={() => setHoveredWard(null)}
                        className="p-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <MapPin className="w-3.5 h-3.5 text-success-600 flex-shrink-0" />
                              <h4 className="text-sm font-semibold text-gray-900 dark:text-white">
                                {ward.ward_name}
                              </h4>
                            </div>
                            <p className="text-xs text-gray-600 dark:text-gray-400 ml-5">
                              {ward.district}
                            </p>
                          </div>
                          <span className={`px-2 py-0.5 text-xs font-semibold rounded-full ${getCorrelationColor(ward.correlation)} ml-2 flex-shrink-0`}>
                            {(ward.correlation * 100).toFixed(0)}%
                          </span>
                        </div>
                        <div className="grid grid-cols-2 gap-2 text-xs ml-5">
                          <div>
                            <span className="text-gray-600 dark:text-gray-400">AQI: </span>
                            <span className={`font-semibold ${getAQIColor(ward.aqi)}`}>
                              {ward.aqi}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-600 dark:text-gray-400">Giáo dục: </span>
                            <span className="font-semibold text-gray-900 dark:text-white">
                              {ward.education_score}/100
                            </span>
                          </div>
                        </div>
                        <div className="mt-2 ml-5">
                          <div className="flex flex-wrap gap-1">
                            {ward.recommended_actions.slice(0, 2).map((action, idx) => (
                              <span
                                key={idx}
                                className="px-1.5 py-0.5 text-xs bg-success-100 text-success-700 dark:bg-success-500/20 dark:text-success-400 rounded"
                              >
                                {action}
                              </span>
                            ))}
                            {ward.recommended_actions.length > 2 && (
                              <span className="px-1.5 py-0.5 text-xs text-gray-500">
                                +{ward.recommended_actions.length - 2}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            </div>
          </div>

          {/* Full Width Table (Optional - for detailed view) */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden border border-gray-200 dark:border-gray-700 mb-8"
          >
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Bảng dữ liệu chi tiết
              </h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-gray-900">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                      Phường/Xã
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                      Quận/Huyện
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                      AQI
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                      Giáo dục
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                      Tương quan
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                      Tác động
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                      Hành động
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {mockAIData.map((ward) => (
                    <tr
                      key={ward.id}
                      onClick={() => handleWardClick(ward)}
                      onMouseEnter={() => setHoveredWard(ward)}
                      onMouseLeave={() => setHoveredWard(null)}
                      className="hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                    >
                      <td className="px-4 py-3 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <MapPin className="w-4 h-4 text-success-600 flex-shrink-0" />
                          <span className="text-sm font-medium text-gray-900 dark:text-white">
                            {ward.ward_name}
                          </span>
                        </div>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                        {ward.district}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className={`text-sm font-semibold ${getAQIColor(ward.aqi)}`}>
                          {ward.aqi}
                        </span>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <School className="w-4 h-4 text-purple-600 flex-shrink-0" />
                          <span className="text-sm font-medium text-gray-900 dark:text-white">
                            {ward.education_score}/100
                          </span>
                        </div>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getCorrelationColor(ward.correlation)}`}>
                          {(ward.correlation * 100).toFixed(0)}%
                        </span>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <TrendingUp className="w-4 h-4 text-success-600 flex-shrink-0" />
                          <span className="text-sm font-semibold text-gray-900 dark:text-white">
                            {ward.impact_score}/10
                          </span>
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex flex-wrap gap-1">
                          {ward.recommended_actions.slice(0, 2).map((action, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 text-xs bg-success-100 text-success-700 dark:bg-success-500/20 dark:text-success-400 rounded"
                            >
                              {action}
                            </span>
                          ))}
                          {ward.recommended_actions.length > 2 && (
                            <span className="px-2 py-1 text-xs text-gray-500">
                              +{ward.recommended_actions.length - 2}
                            </span>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>

          {/* Detail Panel */}
          {isDetailOpen && selectedWard && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
              onClick={() => setIsDetailOpen(false)}
            >
              <motion.div
                initial={{ scale: 0.95 }}
                animate={{ scale: 1 }}
                onClick={(e) => e.stopPropagation()}
                className="w-full max-w-2xl bg-white dark:bg-gray-800 rounded-xl shadow-2xl overflow-hidden"
              >
                <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                  <div className="flex items-center justify-between">
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
                      {selectedWard.ward_name}
                    </h3>
                    <button
                      onClick={() => setIsDetailOpen(false)}
                      className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-400 transition-colors"
                      aria-label="Đóng"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                  <p className="mt-2 text-gray-600 dark:text-gray-400">
                    {selectedWard.district}
                  </p>
                </div>
                <div className="p-6 space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                      <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">AQI</div>
                      <div className={`text-2xl font-bold ${getAQIColor(selectedWard.aqi)}`}>
                        {selectedWard.aqi}
                      </div>
                    </div>
                    <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                      <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Giáo dục</div>
                      <div className="text-2xl font-bold text-gray-900 dark:text-white">
                        {selectedWard.education_score}/100
                      </div>
                    </div>
                  </div>

                  <div>
                    <h4 className="mb-3 text-lg font-semibold text-gray-900 dark:text-white">
                      Hành động được đề xuất
                    </h4>
                    <div className="space-y-2">
                      {Array.isArray(selectedWard.recommended_actions) && selectedWard.recommended_actions.length > 0 ? (
                        selectedWard.recommended_actions.map((action: string, idx: number) => (
                          <div
                            key={idx}
                            className="flex items-center gap-3 p-3 bg-success-50 dark:bg-success-900/20 rounded-lg"
                          >
                            <Leaf className="w-5 h-5 text-success-600" />
                            <span className="text-gray-900 dark:text-white">{action}</span>
                          </div>
                        ))
                      ) : (
                        <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                          <span className="text-gray-600 dark:text-gray-400">Không có hành động được đề xuất</span>
                        </div>
                      )}
                    </div>
                  </div>

                  <div>
                    <h4 className="mb-3 text-lg font-semibold text-gray-900 dark:text-white">
                      Phân tích tương quan
                    </h4>
                    <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-gray-600 dark:text-gray-400">Điểm tương quan:</span>
                        <span className={`px-3 py-1 text-sm font-semibold rounded-full ${getCorrelationColor(selectedWard.correlation)}`}>
                          {(selectedWard.correlation * 100).toFixed(0)}%
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-gray-600 dark:text-gray-400">Điểm tác động:</span>
                        <span className="text-lg font-bold text-gray-900 dark:text-white">
                          {selectedWard.impact_score}/10
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ActionsPage() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-600 dark:text-gray-400">Đang tải...</div>
      </div>
    }>
      <ActionsContent />
    </Suspense>
  );
}
