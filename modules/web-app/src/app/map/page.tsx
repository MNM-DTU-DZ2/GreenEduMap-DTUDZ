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

import { useState, Suspense, useEffect, useRef } from "react";
import PublicHeader from "@/components/common/PublicHeader";
import MapSidebar from "@/components/map/MapSidebar";
import SearchBar from "@/components/map/SearchBar";
import DetailPanel from "@/components/map/DetailPanel";
import { AirQualityData } from "@/hooks/useAirQuality";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

// MapTiler configuration
const MAPTILER_API_KEY = process.env.NEXT_PUBLIC_MAPTILER_API_KEY || "dpmkld1oGcbPpGtsRgKX";
const MAPTILER_STYLE = `https://api.maptiler.com/maps/streets-v2/style.json?key=${MAPTILER_API_KEY}`;

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";
type HeatmapLayerType = "aqi" | "temperature";

function MapContent() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const [isMapLoaded, setIsMapLoaded] = useState(false);
  const [heatmapLayer, setHeatmapLayer] = useState<HeatmapLayerType>("aqi");
  const [showIconLayers, setShowIconLayers] = useState({
    trees: true,
    schools: true,
    solar: true,
  });
  const [selectedWard, setSelectedWard] = useState<AirQualityData | null>(null);
  const [isDetailPanelOpen, setIsDetailPanelOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [hoveredWard, setHoveredWard] = useState<AirQualityData | null>(null);
  const [iconInfo, setIconInfo] = useState<{ title: string; content: string; type: string } | null>(null);

  // Dữ liệu icon layers
  const [schoolData, setSchoolData] = useState<any>(null);
  const [treeData, setTreeData] = useState<any>(null);
  const [solarData, setSolarData] = useState<any>(null);

  // Dữ liệu heatmap (AQI + Nhiệt độ)
  const [aqiPoints, setAqiPoints] = useState<any[]>([]);
  const [temperaturePoints, setTemperaturePoints] = useState<any[]>([]);

  // Dữ liệu tìm kiếm (để dùng trong search)
  const [allSchools, setAllSchools] = useState<any[]>([]);
  const [allZones, setAllZones] = useState<any[]>([]);
  const [allResources, setAllResources] = useState<any[]>([]);

  useEffect(() => {
    // 1) Lấy dữ liệu thật cho heatmap từ Environment Service
    (async () => {
      try {
        // Air quality
        const resAqi = await fetch(`${API_BASE}/api/v1/air-quality?limit=500`);
        if (resAqi.ok) {
          const response: any = await resAqi.json();
          const items: any[] = Array.isArray(response) ? response : (response.data || []);
          console.log('📊 AQI:', items.length, 'points');
          if (Array.isArray(items) && items.length > 0) {
            setAqiPoints(
              items
                .filter((m) => m.latitude && m.longitude && m.aqi !== null && m.aqi !== undefined)
                .map((m, idx) => ({
                  id: m.id ?? idx,
                  ward_name: m.station_name || "Điểm đo",
                  district: m.district || "",
                  city: m.city || "Ho Chi Minh City",
                  latitude: m.latitude,
                  longitude: m.longitude,
                  aqi: Number(m.aqi),
                  pm25: m.pm25 ?? undefined,
                  pm10: m.pm10 ?? undefined,
                })),
            );
          }
        } else {
          console.warn("Failed to fetch AQI data:", resAqi.statusText);
        }

        // Weather (dùng để vẽ heatmap nhiệt độ)
        const resWeather = await fetch(`${API_BASE}/api/v1/weather?limit=500`);
        if (resWeather.ok) {
          const response: any = await resWeather.json();
          const items: any[] = Array.isArray(response) ? response : (response.data || []);
          console.log('🌤️ Weather:', items.length, 'points');
          if (Array.isArray(items) && items.length > 0) {
            setTemperaturePoints(
              items
                .filter((w) => w.latitude && w.longitude && w.temperature !== null && w.temperature !== undefined)
                .map((w, idx) => ({
                  id: w.id ?? idx,
                  ward_name: w.city_name || "Khu vực",
                  district: w.district || "",
                  city: w.city || "Ho Chi Minh City",
                  latitude: w.latitude,
                  longitude: w.longitude,
                  temperature: Number(w.temperature),
                })),
            );
          }
        } else {
          console.warn("Failed to fetch weather data:", resWeather.statusText);
        }
      } catch (err) {
        console.error("Error loading real-time AQI/Weather:", err);
      }
    })();

    // 2) Lấy dữ liệu thật cho Schools từ Education Service
    (async () => {
      try {
        const resSchools = await fetch(`${API_BASE}/api/v1/schools?limit=500`);
        if (resSchools.ok) {
          const response: any = await resSchools.json();
          const schools: any[] = Array.isArray(response) ? response : (response.data || []);
          console.log('🏫 Schools:', schools.length);
          if (Array.isArray(schools) && schools.length > 0) {
            const validSchools = schools.filter((s) => s.latitude && s.longitude);
            console.log(`✅ Loaded ${validSchools.length} schools with location`);
            setAllSchools(schools);
            setSchoolData({
              type: "FeatureCollection",
              features: validSchools.map((school) => ({
                type: "Feature",
                geometry: {
                  type: "Point",
                  coordinates: [school.longitude, school.latitude],
                },
                properties: {
                  id: school.id,
                  name: school.name,
                  district: school.district || "",
                  students: school.total_students || 0,
                },
              })),
            });
          } else {
            console.warn("⚠️ No schools data or empty array");
          }
        } else {
          console.warn("Failed to fetch schools:", resSchools.statusText);
        }
      } catch (err) {
        console.error("Error loading schools:", err);
      }
    })();

    // 3) Lấy dữ liệu thật cho Green Zones (Trees/Parks) từ Resource Service
    (async () => {
      try {
        const resZones = await fetch(`${API_BASE}/api/v1/green-zones?limit=500`);
        if (resZones.ok) {
          const response: any = await resZones.json();
          const zones: any[] = Array.isArray(response) ? response : (response.data || []);
          console.log('🌳 Zones:', zones.length);
          if (Array.isArray(zones) && zones.length > 0) {
            const validZones = zones.filter((z) => z.latitude && z.longitude);
            console.log(`✅ Loaded ${validZones.length} green zones with location`);
            setAllZones(zones);
            setTreeData({
              type: "FeatureCollection",
              features: validZones.map((zone) => ({
                type: "Feature",
                geometry: {
                  type: "Point",
                  coordinates: [zone.longitude, zone.latitude],
                },
                properties: {
                  id: zone.id,
                  name: zone.name,
                  district: zone.address || "",
                  count: zone.tree_count || 0,
                },
              })),
            });
          } else {
            console.warn("⚠️ No green zones data or empty array");
          }
        } else {
          console.warn("Failed to fetch green zones:", resZones.statusText);
        }
      } catch (err) {
        console.error("Error loading green zones:", err);
      }
    })();

    // 4) Lấy dữ liệu thật cho Solar Resources từ Resource Service
    (async () => {
      try {
        const resResources = await fetch(`${API_BASE}/api/v1/green-resources?limit=500`);
        if (resResources.ok) {
          const resources: any[] = await resResources.json();
          if (Array.isArray(resources) && resources.length > 0) {
            setAllResources(resources);

            // Filter solar resources và fetch zones để lấy location
            const solarResources = resources.filter((r) =>
              r.type && (r.type.toLowerCase().includes("solar") || r.type.toLowerCase().includes("nlm"))
            );

            if (solarResources.length > 0) {
              // Fetch zones để lấy location cho solar resources
              const zoneIds = [...new Set(solarResources.map((r) => r.zone_id).filter(Boolean))];
              const zonesMap = new Map<string, any>();

              // Fetch zones
              const resZones = await fetch(`${API_BASE}/api/v1/green-zones?limit=500`);
              if (resZones.ok) {
                const zones: any[] = await resZones.json();
                zones.forEach((zone) => {
                  zonesMap.set(zone.id, zone);
                });
              }

              // Map solar resources với zone locations
              const solarFeatures = solarResources
                .map((resource) => {
                  const zone = zonesMap.get(resource.zone_id);
                  if (!zone || !zone.latitude || !zone.longitude) return null;

                  return {
                    type: "Feature",
                    geometry: {
                      type: "Point",
                      coordinates: [zone.longitude, zone.latitude],
                    },
                    properties: {
                      id: resource.id,
                      name: resource.name || `Trạm NLMT ${zone.name}`,
                      district: zone.address || "",
                      power: `${resource.quantity || 0} ${resource.unit || "kW"}`,
                    },
                  };
                })
                .filter(Boolean);

              setSolarData({
                type: "FeatureCollection",
                features: solarFeatures,
              });
            }
          }
        } else {
          console.warn("Failed to fetch green resources:", resResources.statusText);
        }
      } catch (err) {
        console.error("Error loading green resources:", err);
      }
    })();
  }, []);

  // Convert data to GeoJSON for heatmaps
  const aqiGeoJSON = {
    type: "FeatureCollection" as const,
    features: aqiPoints.map((ward) => ({
      type: "Feature" as const,
      geometry: {
        type: "Point" as const,
        coordinates: [ward.longitude, ward.latitude],
      },
      properties: {
        value: ward.aqi,
        ...ward,
      },
    })),
  };

  const temperatureGeoJSON = {
    type: "FeatureCollection" as const,
    features: temperaturePoints.map((ward) => ({
      type: "Feature" as const,
      geometry: {
        type: "Point" as const,
        coordinates: [ward.longitude, ward.latitude],
      },
      properties: {
        value: ward.temperature,
        ...ward,
      },
    })),
  };

  // Initialize Map
  useEffect(() => {
    if (!mapContainer.current || mapRef.current) return;

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: MAPTILER_STYLE,
      center: [106.6297, 10.8231], // TP.HCM
      zoom: 11,
      pitch: 45,
      bearing: -17.6,
    });

    mapRef.current = map;

    // Add error handler
    map.on("error", (e) => {
      console.error('❌ Map error:', e);
    });

    // Fallback: Set isMapLoaded to true after 3 seconds if load event doesn't fire
    const loadTimeout = setTimeout(() => {
      if (!isMapLoaded) {
        console.warn('⚠️ Map load timeout - forcing isMapLoaded to true');
        setIsMapLoaded(true);
      }
    }, 3000);

    map.on("load", () => {
      clearTimeout(loadTimeout);
      console.log('✅ Map loaded successfully!');
      setIsMapLoaded(true);

      // Add AQI Heatmap Source & Layer
      map.addSource("aqi-heatmap", {
        type: "geojson",
        data: aqiGeoJSON,
      });

      map.addLayer({
        id: "aqi-heatmap",
        type: "heatmap",
        source: "aqi-heatmap",
        maxzoom: 15,
        layout: { visibility: "visible" },
        paint: {
          "heatmap-weight": [
            "interpolate",
            ["linear"],
            ["get", "value"],
            0,
            0,
            50,
            0.3,
            100,
            0.6,
            150,
            0.9,
            200,
            1,
          ],
          "heatmap-color": [
            "interpolate",
            ["linear"],
            ["heatmap-density"],
            0,
            "rgba(34, 197, 94, 0)",
            0.2,
            "rgba(34, 197, 94, 0.5)",
            0.4,
            "rgba(234, 179, 8, 0.7)",
            0.6,
            "rgba(249, 115, 22, 0.8)",
            0.8,
            "rgba(239, 68, 68, 0.9)",
            1,
            "rgba(168, 85, 247, 1)",
          ],
          "heatmap-radius": 50,
          "heatmap-opacity": 0.8,
        },
      });

      // Add Temperature Heatmap Source & Layer
      map.addSource("temperature-heatmap", {
        type: "geojson",
        data: temperatureGeoJSON,
      });

      map.addLayer({
        id: "temperature-heatmap",
        type: "heatmap",
        source: "temperature-heatmap",
        maxzoom: 15,
        layout: { visibility: "none" },
        paint: {
          "heatmap-weight": [
            "interpolate",
            ["linear"],
            ["get", "value"],
            0,
            0,
            25,
            0.3,
            30,
            0.7,
            35,
            1,
            40,
            1,
          ],
          "heatmap-color": [
            "interpolate",
            ["linear"],
            ["heatmap-density"],
            0,
            "rgba(59, 130, 246, 0)",
            0.4,
            "rgba(59, 130, 246, 0.6)",
            0.6,
            "rgba(251, 191, 36, 0.8)",
            1,
            "rgba(239, 68, 68, 1)",
          ],
          "heatmap-radius": 50,
          "heatmap-opacity": 0.8,
        },
      });

      // Add AQI Circles for click interaction
      map.addLayer({
        id: "aqi-circles",
        type: "circle",
        source: "aqi-heatmap",
        paint: {
          "circle-radius": [
            "interpolate",
            ["linear"],
            ["get", "value"],
            0,
            5,
            200,
            30,
          ],
          "circle-color": [
            "interpolate",
            ["linear"],
            ["get", "value"],
            0,
            "#22c55e",
            50,
            "#22c55e",
            100,
            "#eab308",
            150,
            "#f97316",
            200,
            "#ef4444",
            300,
            "#a855f7",
          ],
          "circle-opacity": 0,
          "circle-stroke-width": 0,
        },
      });

      // Click handler for AQI circles
      map.on("click", "aqi-circles", (e) => {
        const feature = e.features?.[0];
        if (!feature) return;

        const wardData = feature.properties as any;
        const ward: AirQualityData = {
          id: wardData.id,
          ward_name: wardData.ward_name,
          district: wardData.district,
          city: wardData.city || "Ho Chi Minh City",
          latitude: wardData.latitude,
          longitude: wardData.longitude,
          aqi: wardData.aqi,
          pm25: wardData.pm25,
          pm10: wardData.pm10,
          measurement_date: new Date().toISOString(),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };

        setSelectedWard(ward);
        setIsDetailPanelOpen(true);
      });

      // Hover handler for AQI circles
      map.on("mouseenter", "aqi-circles", () => {
        map.getCanvas().style.cursor = "pointer";
      });

      map.on("mouseleave", "aqi-circles", () => {
        map.getCanvas().style.cursor = "";
      });

      map.on("mousemove", "aqi-circles", (e) => {
        const feature = e.features?.[0];
        if (!feature) return;

        const wardData = feature.properties as any;
        const ward: AirQualityData = {
          id: wardData.id,
          ward_name: wardData.ward_name,
          district: wardData.district,
          city: wardData.city || "Ho Chi Minh City",
          latitude: wardData.latitude,
          longitude: wardData.longitude,
          aqi: wardData.aqi,
          pm25: wardData.pm25,
          pm10: wardData.pm10,
          measurement_date: new Date().toISOString(),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };

        setHoveredWard(ward);
      });
    });

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  // Add icon layers when data is loaded
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !isMapLoaded) {
      console.log("⏳ Waiting for map to load...", { map: !!map, isMapLoaded, schoolData: !!schoolData, treeData: !!treeData, solarData: !!solarData });
      return;
    }
    if (!schoolData || !treeData) {
      console.log("⏳ Waiting for data...", { schoolData: !!schoolData, treeData: !!treeData, solarData: !!solarData });
      return;
    }
    console.log("✅ Adding icon layers to map...", {
      schools: schoolData.features?.length || 0,
      trees: treeData.features?.length || 0,
      solar: solarData?.features?.length || 0,
    });

    const addIconLayer = (
      id: string,
      iconUrl: string,
      data: any,
      label: string
    ) => {
      // Remove existing layer and source if they exist
      if (map.getLayer(`${id}-layer`)) {
        map.removeLayer(`${id}-layer`);
      }
      if (map.getSource(id)) {
        map.removeSource(id);
      }

      map.addSource(id, { type: "geojson", data });

      // Load icon image using Promise-based approach (MapLibre GL JS)
      (async () => {
        try {
          const image = await new Promise<HTMLImageElement | ImageBitmap>((resolve, reject) => {
            const img = new Image();
            img.crossOrigin = "anonymous";
            img.onload = () => resolve(img);
            img.onerror = reject;
            img.src = iconUrl;
          });

          if (!map.hasImage(`${id}-icon`)) {
            map.addImage(`${id}-icon`, image);
          }

          map.addLayer({
            id: `${id}-layer`,
            type: "symbol",
            source: id,
            layout: {
              "icon-image": `${id}-icon`,
              "icon-size": 0.08,
              "icon-allow-overlap": true,
              "text-field": ["get", "name"],
              "text-offset": [0, 1.5],
              "text-size": 11,
              "text-anchor": "top",
              "text-optional": true,
              visibility: showIconLayers[id as keyof typeof showIconLayers] ? "visible" : "none",
            },
            paint: {
              "text-color": id === "schools" ? "#7c3aed" : id === "trees" ? "#16a34a" : "#d97706",
              "text-halo-color": "#fff",
              "text-halo-width": 1,
            },
          });
        } catch (error) {
          console.error(`Error loading ${id} icon:`, error);
          // Fallback: use circle
          map.addLayer({
            id: `${id}-layer`,
            type: "circle",
            source: id,
            paint: {
              "circle-radius": 8,
              "circle-color": id === "schools" ? "#a855f7" : id === "trees" ? "#22c55e" : "#f59e0b",
              "circle-stroke-width": 2,
              "circle-stroke-color": "#fff",
            },
            layout: {
              visibility: showIconLayers[id as keyof typeof showIconLayers] ? "visible" : "none",
            },
          });
        }
      })();
    };

    addIconLayer(
      "schools",
      "/images/education.png",
      schoolData,
      "Trường học"
    );
    addIconLayer(
      "trees",
      "/images/tree.png",
      treeData,
      "Cây xanh"
    );

    // Only add solar layer if data is available
    if (solarData) {
      addIconLayer(
        "solar",
        "/images/sun.png",
        solarData,
        "Năng lượng mặt trời"
      );
    }

    // Click handlers for icon layers
    ["schools-layer", "trees-layer", "solar-layer"].forEach((layerId) => {
      const clickHandler = (e: maplibregl.MapLayerMouseEvent) => {
        const feature = e.features?.[0];
        if (!feature) return;

        const props = feature.properties!;
        const geometry = feature.geometry as GeoJSON.Point;
        const coords = geometry.coordinates as [number, number];

        // Show popup
        new maplibregl.Popup()
          .setLngLat(coords)
          .setHTML(`<strong>${props.name}</strong><br/>${props.district || ""}`)
          .addTo(map);

        // Set info for detail panel
        const type = layerId.replace("-layer", "");
        let content = "";
        if (type === "schools") {
          content = `Số học sinh: ${props.students || "N/A"}`;
        } else if (type === "trees") {
          content = `Số cây: ${props.count || "N/A"}`;
        } else if (type === "solar") {
          content = `Công suất: ${props.power || "N/A"}`;
        }

        setIconInfo({
          title: props.name as string,
          content,
          type,
        });

        // Also set selected ward if it's a ward-related data
        if (props.ward_name) {
          const ward: AirQualityData = {
            id: props.id,
            ward_name: props.ward_name,
            district: props.district,
            city: props.city || "Ho Chi Minh City",
            latitude: props.latitude,
            longitude: props.longitude,
            aqi: props.aqi,
            pm25: props.pm25,
            pm10: props.pm10,
            measurement_date: new Date().toISOString(),
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          };
          setSelectedWard(ward);
          setIsDetailPanelOpen(true);
        }
      };

      map.on("click", layerId, clickHandler);

      // Hover handlers
      map.on("mouseenter", layerId, () => {
        map.getCanvas().style.cursor = "pointer";
      });
      map.on("mouseleave", layerId, () => {
        map.getCanvas().style.cursor = "";
      });
    });
  }, [schoolData, treeData, solarData, isMapLoaded, showIconLayers]);

  // Update heatmap layer visibility
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !isMapLoaded) return;

    map.setLayoutProperty(
      "aqi-heatmap",
      "visibility",
      heatmapLayer === "aqi" ? "visible" : "none"
    );
    map.setLayoutProperty(
      "temperature-heatmap",
      "visibility",
      heatmapLayer === "temperature" ? "visible" : "none"
    );
  }, [heatmapLayer, isMapLoaded]);

  // Update icon layer visibility
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !isMapLoaded) return;

    ["schools-layer", "trees-layer", "solar-layer"].forEach((layerId) => {
      if (map.getLayer(layerId)) {
        const key = layerId.replace("-layer", "") as keyof typeof showIconLayers;
        map.setLayoutProperty(
          layerId,
          "visibility",
          showIconLayers[key] ? "visible" : "none"
        );
      }
    });
  }, [showIconLayers, isMapLoaded]);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    const map = mapRef.current;
    if (!map || !query.trim()) return;

    const queryLower = query.toLowerCase();

    // Search in real data
    const found =
      // Search in AQI points
      aqiPoints.find(
        (ward) =>
          ward.ward_name?.toLowerCase().includes(queryLower) ||
          ward.district?.toLowerCase().includes(queryLower)
      ) ||
      // Search in schools
      allSchools.find((school) =>
        school.name?.toLowerCase().includes(queryLower) ||
        school.district?.toLowerCase().includes(queryLower)
      ) ||
      // Search in green zones
      allZones.find((zone) =>
        zone.name?.toLowerCase().includes(queryLower) ||
        zone.address?.toLowerCase().includes(queryLower)
      ) ||
      // Search in resources
      allResources.find((resource) =>
        resource.name?.toLowerCase().includes(queryLower)
      );

    if (found && map) {
      const lat = found.latitude;
      const lng = found.longitude;
      if (lat && lng) {
        map.flyTo({
          center: [lng, lat],
          zoom: 14,
          duration: 1500,
        });
      }
    }
  };

  return (
    <div className="relative w-full h-screen overflow-hidden">
      {/* Header */}
      <PublicHeader />

      {/* Map Container */}
      <div className="absolute inset-0 pt-20 sm:pt-24">
        <div ref={mapContainer} className="w-full h-full" />

        {/* Hover Tooltip */}
        {hoveredWard && (
          <div className="absolute top-28 left-96 p-3 bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl rounded-lg shadow-xl z-20 max-w-xs">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
              {hoveredWard.ward_name}
            </h3>
            <div className="text-sm space-y-1">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">AQI:</span>
                <span className="font-semibold text-gray-900 dark:text-white">
                  {hoveredWard.aqi.toFixed(1)}
                </span>
              </div>
              {hoveredWard.district && (
                <div className="text-gray-600 dark:text-gray-400">
                  {hoveredWard.district}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Enhanced Sidebar with Heatmap & Icon Controls */}
        <div className="absolute left-0 top-20 sm:top-24 bottom-0 w-80 bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl shadow-2xl z-10 overflow-y-auto">
          <div className="p-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Lớp dữ liệu
            </h2>

            {/* Heatmap Layer Selection */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wide mb-3">
                Heatmap
              </h3>
              <div className="space-y-2">
                <label className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer transition-colors">
                  <input
                    type="radio"
                    name="heatmap"
                    checked={heatmapLayer === "aqi"}
                    onChange={() => setHeatmapLayer("aqi")}
                    className="w-4 h-4 text-success-600 focus:ring-success-500"
                  />
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    AQI (Chất lượng không khí)
                  </span>
                </label>
                <label className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer transition-colors">
                  <input
                    type="radio"
                    name="heatmap"
                    checked={heatmapLayer === "temperature"}
                    onChange={() => setHeatmapLayer("temperature")}
                    className="w-4 h-4 text-success-600 focus:ring-success-500"
                  />
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    Nhiệt độ
                  </span>
                </label>
              </div>
            </div>

            {/* Icon Layers */}
            <div>
              <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wide mb-3">
                Icon Layers
              </h3>
              <div className="space-y-2">
                {[
                  { key: "trees" as const, label: "Cây xanh" },
                  { key: "schools" as const, label: "Trường học" },
                  { key: "solar" as const, label: "Năng lượng mặt trời" },
                ].map((item) => (
                  <label
                    key={item.key}
                    className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={showIconLayers[item.key]}
                      onChange={() =>
                        setShowIconLayers({
                          ...showIconLayers,
                          [item.key]: !showIconLayers[item.key],
                        })
                      }
                      className="w-5 h-5 text-success-600 rounded focus:ring-success-500 focus:ring-2"
                    />
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {item.label}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            {/* Legend */}
            <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
              <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                Thang màu {heatmapLayer === "aqi" ? "AQI" : "Nhiệt độ"}
              </h4>
              <div
                className="h-3 w-full rounded-full mb-2"
                style={{
                  background:
                    heatmapLayer === "aqi"
                      ? "linear-gradient(90deg, #22c55e, #eab308, #f97316, #ef4444, #a855f7)"
                      : "linear-gradient(90deg, #3b82f6, #fbbf24, #ef4444)",
                }}
              />
              <div className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                {heatmapLayer === "aqi" ? (
                  <>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded bg-green-500" />
                      <span>Tốt (0-50)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded bg-yellow-500" />
                      <span>Trung bình (51-100)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded bg-orange-500" />
                      <span>Không tốt (101-150)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded bg-red-500" />
                      <span>Ô nhiễm (151-200)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded bg-purple-500" />
                      <span>Rất ô nhiễm (&gt;200)</span>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded bg-blue-500" />
                      <span>Mát (25-28°C)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded bg-yellow-500" />
                      <span>Ấm (29-32°C)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded bg-red-500" />
                      <span>Nóng (&gt;32°C)</span>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Search Bar */}
        <SearchBar onSearch={handleSearch} />

        {/* Detail Panel */}
        <DetailPanel
          ward={selectedWard}
          isOpen={isDetailPanelOpen}
          onClose={() => {
            setIsDetailPanelOpen(false);
            setIconInfo(null);
          }}
        />

        {/* Icon Info Panel (when clicking on icons) */}
        {iconInfo && !isDetailPanelOpen && (
          <div className="absolute top-20 sm:top-24 right-0 bottom-0 w-80 bg-white dark:bg-gray-900 shadow-2xl z-40 overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {iconInfo.title}
                </h2>
                <button
                  onClick={() => setIconInfo(null)}
                  className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors text-gray-600 dark:text-gray-400"
                  aria-label="Đóng"
                >
                  ×
                </button>
              </div>
              <div className="p-4 bg-success-50 dark:bg-success-900/20 rounded-lg">
                <p className="text-gray-900 dark:text-white">{iconInfo.content}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function MapPage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-gray-600 dark:text-gray-400">Đang tải bản đồ...</div>
        </div>
      }
    >
      <MapContent />
    </Suspense>
  );
}
