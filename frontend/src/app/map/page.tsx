"use client";

import { useState, Suspense, useEffect, useRef } from "react";
import PublicHeader from "@/components/common/PublicHeader";
import MapSidebar from "@/components/map/MapSidebar";
import SearchBar from "@/components/map/SearchBar";
import DetailPanel from "@/components/map/DetailPanel";
import { AirQualityData } from "@/hooks/useAirQuality";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

// Set Mapbox token
if (typeof window !== "undefined") {
  const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;
  if (token) {
    mapboxgl.accessToken = token;
  }
}

// Mock data for TP.HCM
const mockDataTPHCM = [
  { id: 1, ward_name: "Phường Bến Nghé", district: "Quận 1", city: "Ho Chi Minh City", latitude: 10.7769, longitude: 106.7009, aqi: 85, pm25: 35, pm10: 55 },
  { id: 2, ward_name: "Phường Đa Kao", district: "Quận 1", city: "Ho Chi Minh City", latitude: 10.7889, longitude: 106.6992, aqi: 92, pm25: 38, pm10: 60 },
  { id: 3, ward_name: "Phường Cầu Kho", district: "Quận 1", city: "Ho Chi Minh City", latitude: 10.7589, longitude: 106.6733, aqi: 78, pm25: 32, pm10: 50 },
  { id: 4, ward_name: "Phường Cô Giang", district: "Quận 1", city: "Ho Chi Minh City", latitude: 10.7633, longitude: 106.6917, aqi: 88, pm25: 36, pm10: 58 },
  { id: 5, ward_name: "Phường Nguyễn Thái Bình", district: "Quận 1", city: "Ho Chi Minh City", latitude: 10.7711, longitude: 106.7056, aqi: 95, pm25: 40, pm10: 62 },
  { id: 6, ward_name: "Phường Phạm Ngũ Lão", district: "Quận 1", city: "Ho Chi Minh City", latitude: 10.7689, longitude: 106.6944, aqi: 82, pm25: 34, pm10: 53 },
  { id: 7, ward_name: "Phường Cầu Ông Lãnh", district: "Quận 1", city: "Ho Chi Minh City", latitude: 10.7611, longitude: 106.6889, aqi: 90, pm25: 37, pm10: 59 },
  { id: 8, ward_name: "Phường Tân Định", district: "Quận 1", city: "Ho Chi Minh City", latitude: 10.7911, longitude: 106.6917, aqi: 87, pm25: 35, pm10: 56 },
  { id: 9, ward_name: "Phường Bến Thành", district: "Quận 1", city: "Ho Chi Minh City", latitude: 10.7722, longitude: 106.6981, aqi: 105, pm25: 42, pm10: 65 },
  { id: 10, ward_name: "Phường An Phú Đông", district: "Quận 12", city: "Ho Chi Minh City", latitude: 10.8633, longitude: 106.6333, aqi: 72, pm25: 30, pm10: 48 },
  { id: 11, ward_name: "Phường Đông Hưng Thuận", district: "Quận 12", city: "Ho Chi Minh City", latitude: 10.8589, longitude: 106.6417, aqi: 75, pm25: 31, pm10: 49 },
  { id: 12, ward_name: "Phường Hiệp Thành", district: "Quận 12", city: "Ho Chi Minh City", latitude: 10.8667, longitude: 106.6389, aqi: 80, pm25: 33, pm10: 52 },
  { id: 13, ward_name: "Phường Tân Chánh Hiệp", district: "Quận 12", city: "Ho Chi Minh City", latitude: 10.8611, longitude: 106.6361, aqi: 78, pm25: 32, pm10: 51 },
  { id: 14, ward_name: "Phường Thạnh Lộc", district: "Quận 12", city: "Ho Chi Minh City", latitude: 10.8556, longitude: 106.6444, aqi: 85, pm25: 35, pm10: 55 },
  { id: 15, ward_name: "Phường Bình Hưng Hòa", district: "Quận Bình Tân", city: "Ho Chi Minh City", latitude: 10.7589, longitude: 106.6000, aqi: 115, pm25: 45, pm10: 70 },
  { id: 16, ward_name: "Phường Bình Hưng Hòa A", district: "Quận Bình Tân", city: "Ho Chi Minh City", latitude: 10.7611, longitude: 106.6022, aqi: 120, pm25: 47, pm10: 72 },
  { id: 17, ward_name: "Phường Bình Trị Đông", district: "Quận Bình Tân", city: "Ho Chi Minh City", latitude: 10.7633, longitude: 106.6056, aqi: 125, pm25: 49, pm10: 75 },
  { id: 18, ward_name: "Phường Tân Tạo", district: "Quận Bình Tân", city: "Ho Chi Minh City", latitude: 10.7556, longitude: 106.5978, aqi: 135, pm25: 53, pm10: 80 },
  { id: 19, ward_name: "Phường An Lạc", district: "Quận Bình Tân", city: "Ho Chi Minh City", latitude: 10.7500, longitude: 106.5933, aqi: 145, pm25: 57, pm10: 85 },
  { id: 20, ward_name: "Phường An Lạc A", district: "Quận Bình Tân", city: "Ho Chi Minh City", latitude: 10.7478, longitude: 106.5911, aqi: 150, pm25: 59, pm10: 88 },
];

// Mock temperature data
const mockTemperatureData = mockDataTPHCM.map((ward) => ({
  ...ward,
  temperature: 28 + Math.random() * 5, // 28-33°C
}));

// Mock school data
const mockSchoolData = [
  { id: 1, name: "THPT Nguyễn Thị Minh Khai", latitude: 10.7769, longitude: 106.7009, district: "Quận 1", students: 1200 },
  { id: 2, name: "THCS Lê Quý Đôn", latitude: 10.7889, longitude: 106.6992, district: "Quận 1", students: 850 },
  { id: 3, name: "TH Nguyễn Bỉnh Khiêm", latitude: 10.7633, longitude: 106.6917, district: "Quận 1", students: 650 },
  { id: 4, name: "THPT Trần Hưng Đạo", latitude: 10.7711, longitude: 106.7056, district: "Quận 1", students: 1100 },
  { id: 5, name: "THCS Nguyễn Du", latitude: 10.7689, longitude: 106.6944, district: "Quận 1", students: 900 },
  { id: 6, name: "THPT Nguyễn Thị Diệu", latitude: 10.8633, longitude: 106.6333, district: "Quận 12", students: 1300 },
  { id: 7, name: "THCS Tân Chánh Hiệp", latitude: 10.8611, longitude: 106.6361, district: "Quận 12", students: 750 },
  { id: 8, name: "THPT Bình Tân", latitude: 10.7589, longitude: 106.6000, district: "Quận Bình Tân", students: 1400 },
  { id: 9, name: "THCS Bình Hưng Hòa", latitude: 10.7611, longitude: 106.6022, district: "Quận Bình Tân", students: 800 },
  { id: 10, name: "TH An Lạc", latitude: 10.7500, longitude: 106.5933, district: "Quận Bình Tân", students: 600 },
];

// Mock tree data (green areas/parks)
const mockTreeData = [
  { id: 1, name: "Công viên Lê Văn Tám", latitude: 10.7769, longitude: 106.7009, district: "Quận 1", count: 250 },
  { id: 2, name: "Công viên 23/9", latitude: 10.7722, longitude: 106.6981, district: "Quận 1", count: 180 },
  { id: 3, name: "Công viên Tao Đàn", latitude: 10.7889, longitude: 106.6992, district: "Quận 1", count: 320 },
  { id: 4, name: "Công viên Gia Định", latitude: 10.8633, longitude: 106.6333, district: "Quận 12", count: 200 },
  { id: 5, name: "Công viên Bình Tân", latitude: 10.7589, longitude: 106.6000, district: "Quận Bình Tân", count: 150 },
];

// Mock solar data
const mockSolarData = [
  { id: 1, name: "Trạm NLMT Quận 1", latitude: 10.7711, longitude: 106.7056, district: "Quận 1", power: "150kW" },
  { id: 2, name: "Trạm NLMT Quận 12", latitude: 10.8611, longitude: 106.6361, district: "Quận 12", power: "200kW" },
  { id: 3, name: "Trạm NLMT Bình Tân", latitude: 10.7556, longitude: 106.5978, district: "Quận Bình Tân", power: "180kW" },
  { id: 4, name: "Trạm NLMT Tân Định", latitude: 10.7911, longitude: 106.6917, district: "Quận 1", power: "120kW" },
];

// API fetch function
async function fetchData(endpoint: string) {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ""}${endpoint}`);
    if (!res.ok) throw new Error(`Error fetching ${endpoint}`);
    return await res.json();
  } catch (e) {
    console.error(e);
    return null;
  }
}

type HeatmapLayerType = "aqi" | "temperature";

function MapContent() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<mapboxgl.Map | null>(null);
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

  // Fetch data from API or use mock data
  const [schoolData, setSchoolData] = useState<any>(null);
  const [treeData, setTreeData] = useState<any>(null);
  const [solarData, setSolarData] = useState<any>(null);

  useEffect(() => {
    (async () => {
      // Try to fetch from API, fallback to mock data
      const schools = await fetchData("/api/schools");
      const trees = await fetchData("/api/trees");
      const solar = await fetchData("/api/solar");

      setSchoolData(
        schools ||
          ({
            type: "FeatureCollection",
            features: mockSchoolData.map((school) => ({
              type: "Feature",
              geometry: {
                type: "Point",
                coordinates: [school.longitude, school.latitude],
              },
              properties: {
                id: school.id,
                name: school.name,
                district: school.district,
                students: school.students,
              },
            })),
          } as any)
      );

      setTreeData(
        trees ||
          ({
            type: "FeatureCollection",
            features: mockTreeData.map((tree) => ({
              type: "Feature",
              geometry: {
                type: "Point",
                coordinates: [tree.longitude, tree.latitude],
              },
              properties: {
                id: tree.id,
                name: tree.name,
                district: tree.district,
                count: tree.count,
              },
            })),
          } as any)
      );

      setSolarData(
        solar ||
          ({
            type: "FeatureCollection",
            features: mockSolarData.map((solar) => ({
              type: "Feature",
              geometry: {
                type: "Point",
                coordinates: [solar.longitude, solar.latitude],
              },
              properties: {
                id: solar.id,
                name: solar.name,
                district: solar.district,
                power: solar.power,
              },
            })),
          } as any)
      );
    })();
  }, []);

  // Convert mock data to GeoJSON for heatmaps
  const aqiGeoJSON = {
    type: "FeatureCollection" as const,
    features: mockDataTPHCM.map((ward) => ({
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
    features: mockTemperatureData.map((ward) => ({
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
    if (!map || !isMapLoaded || !schoolData || !treeData || !solarData) return;

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

      map.loadImage(iconUrl, (error, image) => {
        if (error || !image) {
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
          return;
        }

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
      });
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
    addIconLayer(
      "solar",
      "/images/sun.png",
      solarData,
      "Năng lượng mặt trời"
    );

    // Click handlers for icon layers
    ["schools-layer", "trees-layer", "solar-layer"].forEach((layerId) => {
      const clickHandler = (e: mapboxgl.MapLayerMouseEvent) => {
        const feature = e.features?.[0];
        if (!feature) return;

        const props = feature.properties!;
        const geometry = feature.geometry as GeoJSON.Point;
        const coords = geometry.coordinates as [number, number];

        // Show popup
        new mapboxgl.Popup()
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

    // Search in mock data
    const found =
      mockDataTPHCM.find(
        (ward) =>
          ward.ward_name.toLowerCase().includes(query.toLowerCase()) ||
          ward.district?.toLowerCase().includes(query.toLowerCase())
      ) ||
      mockSchoolData.find((school) =>
        school.name.toLowerCase().includes(query.toLowerCase())
      ) ||
      mockTreeData.find((tree) =>
        tree.name.toLowerCase().includes(query.toLowerCase())
      ) ||
      mockSolarData.find((solar) =>
        solar.name.toLowerCase().includes(query.toLowerCase())
      );

    if (found && map) {
      map.flyTo({
        center: [found.longitude, found.latitude],
        zoom: 14,
        duration: 1500,
      });
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
