"use client";
import Link from "next/link";
import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import {
  CheckCircleIcon,
  BoltIcon,
  BoxIcon,
  GroupIcon,
  ChevronDownIcon,
} from "@/icons";
import PublicHeader from "@/components/common/PublicHeader";
import { MapPin, School, Wind, Zap, TrendingUp, Users, Globe, Lightbulb, Activity, BookOpen, ArrowRight, Map, Brain, MessageCircle, BarChart3, Heart, Sparkles, GraduationCap } from "lucide-react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

// Set Mapbox token
if (typeof window !== "undefined") {
  const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;
  if (token) {
    mapboxgl.accessToken = token;
  }
}

// Mock data for preview - Enhanced with more realistic data
const previewData = {
  aqi: [
    { name: "Quận 1", lat: 10.7769, lng: 106.7009, value: 85 },
    { name: "Quận 2", lat: 10.7833, lng: 106.7500, value: 72 },
    { name: "Quận 3", lat: 10.7833, lng: 106.6833, value: 92 },
    { name: "Quận 4", lat: 10.7550, lng: 106.7100, value: 78 },
    { name: "Quận 5", lat: 10.7700, lng: 106.6800, value: 88 },
    { name: "Quận 6", lat: 10.7450, lng: 106.6600, value: 95 },
    { name: "Quận 7", lat: 10.7300, lng: 106.7200, value: 68 },
    { name: "Quận 8", lat: 10.7250, lng: 106.6950, value: 105 },
    { name: "Quận 10", lat: 10.7900, lng: 106.6600, value: 82 },
    { name: "Quận 11", lat: 10.8100, lng: 106.6500, value: 90 },
    { name: "Quận 12", lat: 10.8633, lng: 106.6333, value: 82 },
    { name: "Bình Tân", lat: 10.7589, lng: 106.6000, value: 125 },
    { name: "Bình Thạnh", lat: 10.8200, lng: 106.7400, value: 75 },
    { name: "Gò Vấp", lat: 10.8400, lng: 106.6700, value: 88 },
  ],
  schools: [
        { name: "THPT Nguyễn Thị Minh Khai", lat: 10.7769, lng: 106.7009 },
    { name: "THCS Lê Quý Đôn", lat: 10.7889, lng: 106.6992 },
    { name: "THPT Gia Định", lat: 10.8100, lng: 106.6800 },
    { name: "THCS Tạ Uyên", lat: 10.7600, lng: 106.7100 },
    { name: "THPT Marie Curie", lat: 10.8000, lng: 106.7200 },
  ],
  solar: [
    { name: "Trạm NLMT Quận 1", lat: 10.7711, lng: 106.7056 },
    { name: "Trạm NLMT Quận 2", lat: 10.7900, lng: 106.7400 },
    { name: "Trạm NLMT Quận 7", lat: 10.7350, lng: 106.7250 },
    { name: "Trạm NLMT Quận 12", lat: 10.8611, lng: 106.6361 },
    { name: "Trạm NLMT Bình Thạnh", lat: 10.8200, lng: 106.7350 },
  ],
};

// Statistics for the landing page
const stats = [
  { label: "Quận/Huyện", value: "24+", icon: Globe },
  { label: "Trường học", value: "1000+", icon: School },
  { label: "Điểm quan sát", value: "500+", icon: Activity },
  { label: "Người dùng", value: "5000+", icon: Users },
];

// Animated Counter Component
function AnimatedCounter({ target, suffix = "" }: { target: number; suffix?: string }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let animationFrame: number;
    let currentValue = 0;
    const startTime = Date.now();
    const duration = 2000; // 2 seconds

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      currentValue = Math.floor(target * progress);
      setCount(currentValue);

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      } else {
        setCount(target);
      }
    };

    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, [target]);

  return (
    <span>
      {count}
      {suffix}
    </span>
  );
}

export default function HomePage() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<mapboxgl.Map | null>(null);
  const [isMapLoaded, setIsMapLoaded] = useState(false);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  // Initialize Map Preview
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
      zoom: 10.5,
      pitch: 35,
      bearing: -15,
    });

    mapRef.current = map;

    map.on("load", () => {
      setIsMapLoaded(true);

      // AQI Heatmap GeoJSON
      const aqiGeoJSON = {
        type: "FeatureCollection" as const,
        features: previewData.aqi.map((item) => ({
          type: "Feature" as const,
          geometry: {
            type: "Point" as const,
            coordinates: [item.lng, item.lat],
          },
          properties: {
            value: item.value,
            name: item.name,
          },
        })),
      };

      // Add AQI Heatmap
      map.addSource("preview-aqi-heatmap", {
        type: "geojson",
        data: aqiGeoJSON,
      });

      map.addLayer({
        id: "preview-aqi-heatmap",
        type: "heatmap",
        source: "preview-aqi-heatmap",
        maxzoom: 15,
        paint: {
          "heatmap-weight": [
            "interpolate",
            ["linear"],
            ["get", "value"],
            0, 0,
            200, 1,
          ],
          "heatmap-color": [
            "interpolate",
            ["linear"],
            ["heatmap-density"],
            0, "rgba(34, 197, 94, 0)",
            0.3, "rgba(34, 197, 94, 0.4)",
            0.5, "rgba(234, 179, 8, 0.6)",
            0.7, "rgba(249, 115, 22, 0.7)",
            1, "rgba(239, 68, 68, 0.8)",
          ],
          "heatmap-radius": 40,
          "heatmap-opacity": 0.6,
        },
      });

      // Add Schools
      const schoolsGeoJSON = {
        type: "FeatureCollection" as const,
        features: previewData.schools.map((item) => ({
          type: "Feature" as const,
          geometry: {
            type: "Point" as const,
            coordinates: [item.lng, item.lat],
          },
          properties: { name: item.name },
        })),
      };

      map.addSource("preview-schools", {
        type: "geojson",
        data: schoolsGeoJSON,
      });

      map.addLayer({
        id: "preview-schools-layer",
        type: "circle",
        source: "preview-schools",
        paint: {
          "circle-radius": 8,
          "circle-color": "#a855f7",
          "circle-stroke-width": 2,
          "circle-stroke-color": "#fff",
        },
      });

      // Add Solar
      const solarGeoJSON = {
        type: "FeatureCollection" as const,
        features: previewData.solar.map((item) => ({
          type: "Feature" as const,
          geometry: {
            type: "Point" as const,
            coordinates: [item.lng, item.lat],
          },
          properties: { name: item.name },
        })),
      };

      map.addSource("preview-solar", {
        type: "geojson",
        data: solarGeoJSON,
      });

      map.addLayer({
        id: "preview-solar-layer",
        type: "circle",
        source: "preview-solar",
        paint: {
          "circle-radius": 8,
          "circle-color": "#f59e0b",
          "circle-stroke-width": 2,
          "circle-stroke-color": "#fff",
        },
      });
    });

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 overflow-x-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-0 right-0 w-[800px] h-[800px] rounded-full opacity-20 bg-gradient-to-br from-success-400/40 to-transparent blur-3xl"
          animate={{
            x: mousePosition.x * 0.02,
            y: mousePosition.y * 0.02,
          }}
          transition={{ type: "spring", stiffness: 50, damping: 30 }}
        />
        <motion.div
          className="absolute bottom-0 left-0 w-[600px] h-[600px] rounded-full opacity-20 bg-gradient-to-br from-blue-light-400/30 to-transparent blur-3xl"
          animate={{
            x: -mousePosition.x * 0.015,
            y: -mousePosition.y * 0.015,
          }}
          transition={{ type: "spring", stiffness: 50, damping: 30 }}
        />
      </div>

      {/* Navigation */}
      <PublicHeader />

      {/* Hero Section */}
      <section className="relative pt-24 pb-20 overflow-hidden sm:pt-40 sm:pb-40">
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-br from-white via-success-50/30 to-blue-light-50/20 dark:from-gray-950 dark:via-success-950/20 dark:to-blue-light-950/10" />
          <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-[0.02] dark:opacity-[0.05]" />
        </div>

        <div className="relative px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-2 px-4 py-2 mb-8 rounded-full bg-gradient-to-r from-success-50 to-blue-light-50 dark:from-success-500/10 dark:to-blue-light-500/10 border border-success-200/50 dark:border-success-800/50 shadow-lg backdrop-blur-sm"
            >
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-success-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-success-500"></span>
              </span>
              <span className="text-sm font-semibold bg-gradient-to-r from-success-600 to-blue-light-600 dark:from-success-400 dark:to-blue-light-400 bg-clip-text text-transparent">
                Nền tảng quản lý môi trường thông minh
              </span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.1 }}
              className="mb-6 font-black text-gray-900 text-5xl sm:text-6xl lg:text-7xl dark:text-white leading-tight"
            >
              Khám phá và{" "}
              <span className="bg-gradient-to-r from-success-600 via-success-500 to-blue-light-500 bg-clip-text text-transparent animate-gradient">
                hành động xanh
              </span>
              {" "}cùng cộng đồng
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="max-w-3xl mx-auto mb-12 text-lg sm:text-xl text-gray-600 dark:text-gray-300 leading-relaxed"
            >
              GreenEduMap là nền tảng tích hợp bản đồ 3D thời gian thực, dữ liệu môi trường,
              chỉ số giáo dục và đề xuất hành động xanh thông minh từ AI. Cùng chúng tôi xây dựng
              thành phố bền vững ngay từ bây giờ.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="flex flex-col items-center justify-center gap-4 sm:flex-row mb-16"
            >
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Link
                  href="/map"
                  className="inline-flex items-center justify-center px-8 py-4 text-base font-semibold text-white transition-all rounded-xl shadow-2xl bg-gradient-to-r from-success-600 via-success-500 to-blue-light-500 hover:shadow-2xl hover:shadow-success-500/40 group"
                >
                  Khám phá bản đồ
                  <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                </Link>
              </motion.div>
              <motion.a
                href="#features"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="inline-flex items-center justify-center px-8 py-4 text-base font-semibold text-gray-700 transition-all bg-white/60 backdrop-blur-sm border border-gray-300 rounded-xl shadow-lg hover:bg-white/80 hover:shadow-xl dark:bg-gray-800/60 dark:text-gray-300 dark:border-gray-700 dark:hover:bg-gray-800/80"
              >
                Tìm hiểu thêm
                <motion.div
                  animate={{ y: [0, 5, 0] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                >
                  <ChevronDownIcon className="w-5 h-5 ml-2" />
                </motion.div>
              </motion.a>
            </motion.div>

            {/* Quick Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-16"
            >
              {stats.map((stat, index) => {
                const numericValue = parseInt(stat.value.replace('+', ''));
                return (
                  <motion.div
                    key={index}
                    whileHover={{ y: -8, scale: 1.05 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    initial={{ opacity: 0, y: 20 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                    className="p-6 rounded-xl bg-gradient-to-br from-white to-gray-50 dark:from-gray-800/50 dark:to-gray-900/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50 hover:border-success-300 dark:hover:border-success-700 transition-all shadow-lg hover:shadow-xl group"
                  >
                    <div className="flex items-center justify-center mb-4 p-3 rounded-lg bg-gradient-to-br from-success-100 to-blue-light-100 dark:from-success-900/20 dark:to-blue-light-900/20 group-hover:shadow-lg transition-all">
                      <stat.icon className="w-7 h-7 text-success-600 group-hover:scale-110 transition-transform" />
                    </div>
                    <motion.div
                      className="text-3xl sm:text-4xl font-black text-transparent bg-gradient-to-r from-success-600 to-blue-light-500 bg-clip-text mb-2"
                    >
                      <AnimatedCounter target={numericValue} suffix="+" />
                    </motion.div>
                    <div className="text-sm font-medium text-gray-600 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-gray-100 transition-colors">
                      {stat.label}
                    </div>
                  </motion.div>
                );
              })}
            </motion.div>
          </div>

          {/* Map Preview */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="mt-20 sm:mt-28"
          >
            <div className="relative">
              {/* Glow Effect */}
              <div className="absolute -inset-1 bg-gradient-to-r from-success-600/30 via-blue-light-600/20 to-success-600/30 rounded-3xl blur-2xl opacity-75 group-hover:opacity-100 transition duration-1000 animate-pulse" />

              <Link href="/map" className="block group cursor-pointer relative">
                <div className="relative p-1.5 mx-auto rounded-2xl bg-gradient-to-r from-success-500 via-success-600 to-blue-light-500 max-w-6xl shadow-2xl hover:shadow-2xl hover:shadow-success-500/50 transition-all duration-500 group-hover:scale-[1.02] border border-white/20">
                  <div className="overflow-hidden bg-white rounded-xl dark:bg-gray-900">
                    <div className="aspect-video relative bg-gradient-to-br from-gray-100 to-gray-50 dark:from-gray-800 dark:to-gray-900">
                      <div ref={mapContainer} className="w-full h-full pointer-events-none" />

                      {/* Overlay Gradient */}
                      {isMapLoaded && (
                        <div className="absolute inset-0 bg-gradient-to-t from-black/30 via-transparent to-transparent pointer-events-none" />
                      )}

                      {/* Top Left - Feature Highlights */}
                      {isMapLoaded && (
                        <motion.div
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: 1.2, duration: 0.6 }}
                          className="absolute top-6 left-6 space-y-3 pointer-events-none max-w-sm"
                        >
                          <div className="px-4 py-3 bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl rounded-xl shadow-lg border border-white/20 hover:border-success-300 transition-all"
                          >
                            <div className="flex items-center gap-3">
                              <div className="p-2 rounded-lg bg-success-100 dark:bg-success-900/30">
                                <Wind className="w-5 h-5 text-success-600" />
                              </div>
                              <div>
                                <div className="text-xs font-semibold text-gray-600 dark:text-gray-400">
                                  Chất lượng không khí
                                </div>
                                <div className="text-sm font-bold text-gray-900 dark:text-white">
                                  14 quận được giám sát
                                </div>
                              </div>
                            </div>
                          </div>
                        </motion.div>
                      )}

                      {/* Bottom Left - Stats */}
                      {isMapLoaded && (
                        <motion.div
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 1.4, duration: 0.6 }}
                          className="absolute bottom-6 left-6 pointer-events-none space-y-2"
                        >
                          <div className="flex gap-2">
                            <div className="px-3 py-2 bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl rounded-lg shadow-lg border border-white/20 flex items-center gap-2">
                              <School className="w-4 h-4 text-purple-600 flex-shrink-0" />
                              <span className="text-xs font-semibold text-gray-900 dark:text-white">
                                {previewData.schools.length} Trường học
                              </span>
                            </div>
                            <div className="px-3 py-2 bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl rounded-lg shadow-lg border border-white/20 flex items-center gap-2">
                              <Zap className="w-4 h-4 text-amber-500 flex-shrink-0" />
                              <span className="text-xs font-semibold text-gray-900 dark:text-white">
                                {previewData.solar.length} Điểm năng lượng
                              </span>
                            </div>
                          </div>
                        </motion.div>
                      )}

                      {/* Bottom Right - Legend */}
                      {isMapLoaded && (
                        <motion.div
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: 1.6, duration: 0.6 }}
                          className="absolute bottom-6 right-6 pointer-events-none"
                        >
                          <div className="px-4 py-3 bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl rounded-xl shadow-lg border border-white/20">
                            <h4 className="text-xs font-semibold text-gray-900 dark:text-white mb-3">
                              Heatmap AQI
                            </h4>
                            <div className="flex gap-2 text-xs">
                              <div className="flex items-center gap-1.5">
                                <div className="w-3 h-3 rounded-full bg-green-500" />
                                <span className="text-gray-700 dark:text-gray-300">Tốt</span>
                              </div>
                              <div className="flex items-center gap-1.5">
                                <div className="w-3 h-3 rounded-full bg-red-500" />
                                <span className="text-gray-700 dark:text-gray-300">Xấu</span>
                              </div>
                            </div>
                          </div>
                        </motion.div>
                      )}

                      {/* Center - Call to Action */}
                      {isMapLoaded && (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: 1, duration: 0.6 }}
                          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none"
                        >
                          <motion.div
                            animate={{ y: [0, 10, 0] }}
                            transition={{ duration: 2, repeat: Infinity }}
                            className="flex flex-col items-center gap-3"
                          >
                            <div className="p-4 rounded-full bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl shadow-2xl border border-white/30">
                              <MapPin className="w-8 h-8 text-success-600" />
                            </div>
                            <div className="px-6 py-3 bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 text-center">
                              <div className="font-bold text-gray-900 dark:text-white text-sm sm:text-base">
                                Nhấn để khám phá
                              </div>
                              <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                                Bản đồ tương tác 3D
                              </div>
                            </div>
                          </motion.div>
                        </motion.div>
                      )}

                      {/* Hover Overlay */}
                      <div className="absolute inset-0 bg-gradient-to-t from-success-900/0 via-transparent to-success-600/0 opacity-0 group-hover:opacity-10 transition-opacity duration-300 pointer-events-none rounded-xl" />
                    </div>
                  </div>
                </div>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-950 sm:py-40 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-[0.02] dark:opacity-[0.03]" />

        <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8 relative">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-20"
          >
            <h2 className="mb-4 font-black text-gray-900 text-4xl sm:text-5xl dark:text-white">
              Tính năng{" "}
              <span className="bg-gradient-to-r from-success-600 to-blue-light-500 bg-clip-text text-transparent">
                vượt trội
              </span>
            </h2>
            <p className="max-w-2xl mx-auto text-lg text-gray-600 dark:text-gray-400">
              Công nghệ AI tiên tiến kết hợp dữ liệu môi trường, giáo dục và cộng đồng
            </p>
          </motion.div>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
            {[
              {
                icon: Map,
                title: "Bản đồ 3D thời gian thực",
                desc: "Theo dõi chất lượng không khí (AQI), nhiệt độ, năng lượng xanh trên bản đồ 3D tương tác.",
                gradient: "from-success-500 to-success-600",
                bgGradient: "from-success-50 to-success-100 dark:from-success-500/10 dark:to-success-600/10",
                delay: 0,
              },
              {
                icon: Brain,
                title: "Gợi ý AI thông minh",
                desc: "Nhận đề xuất hành động xanh cá nhân hóa dựa trên vị trí và dữ liệu môi trường.",
                gradient: "from-amber-500 to-amber-600",
                bgGradient: "from-amber-50 to-amber-100 dark:from-amber-500/10 dark:to-amber-600/10",
                delay: 0.1,
              },
              {
                icon: GraduationCap,
                title: "Khóa học môi trường",
                desc: "Học các khóa học về môi trường, phát triển bền vững từ các trường học và chuyên gia.",
                gradient: "from-blue-light-500 to-blue-light-600",
                bgGradient: "from-blue-light-50 to-blue-light-100 dark:from-blue-light-500/10 dark:to-blue-light-500/20",
                delay: 0.2,
              },
              {
                icon: MessageCircle,
                title: "Chat với GreenBot",
                desc: "Trò chuyện với AI GreenBot để nhận tư vấn về môi trường và hành động xanh.",
                gradient: "from-orange-500 to-orange-600",
                bgGradient: "from-orange-50 to-orange-100 dark:from-orange-500/10 dark:to-orange-600/10",
                delay: 0.3,
              },
              {
                icon: BarChart3,
                title: "Thống kê & Phân tích",
                desc: "Xem biểu đồ so sánh khu vực, xu hướng môi trường và tác động hành động xanh.",
                gradient: "from-purple-500 to-purple-600",
                bgGradient: "from-purple-50 to-purple-100 dark:from-purple-500/10 dark:to-purple-600/10",
                delay: 0.4,
              },
              {
                icon: Heart,
                title: "Cộng đồng tham gia",
                desc: "Gửi ý tưởng xanh, chia sẻ kinh nghiệm và kết nối với cộng đồng yêu môi trường.",
                gradient: "from-pink-500 to-pink-600",
                bgGradient: "from-pink-50 to-pink-100 dark:from-pink-500/10 dark:to-pink-600/10",
                delay: 0.5,
              },
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: feature.delay }}
                whileHover={{ y: -15, rotateX: 5, rotateY: 5 }}
                style={{ perspective: 1000 }}
                className="relative p-8 overflow-hidden transition-all bg-gradient-to-br from-white to-gray-50 border border-gray-200 group rounded-2xl hover:shadow-2xl dark:from-gray-800/50 dark:to-gray-900/50 dark:border-gray-700 dark:hover:border-success-600/50 backdrop-blur-sm"
              >
                {/* Animated Gradient Border */}
                <div className="absolute inset-0 rounded-2xl p-[1px] bg-gradient-to-r from-transparent via-success-500 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

                {/* Background Gradient Overlay */}
                <div className={`absolute inset-0 bg-gradient-to-br ${feature.bgGradient} opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl`} />

                {/* Spotlight Effect */}
                <motion.div
                  className="absolute -inset-full bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-20 blur-2xl"
                  animate={{ x: ['-100%', '100%'] }}
                  transition={{ duration: 3, repeat: Infinity }}
                />

                <div className="relative z-10">
                  <motion.div
                    whileHover={{ rotate: 360, scale: 1.15 }}
                    transition={{ duration: 0.7, type: "spring", stiffness: 100 }}
                    className={`flex items-center justify-center w-16 h-16 mb-6 rounded-xl bg-gradient-to-br ${feature.gradient} shadow-xl group-hover:shadow-2xl transition-shadow`}
                  >
                    <feature.icon className="w-8 h-8 text-white" />
                  </motion.div>

                  <motion.h3
                    whileHover={{ x: 5 }}
                    className="mb-3 text-xl font-bold text-gray-900 dark:text-white group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-success-600 group-hover:to-blue-light-500 group-hover:bg-clip-text transition-all"
                  >
                    {feature.title}
                  </motion.h3>

                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed group-hover:text-gray-900 dark:group-hover:text-gray-100 transition-colors">
                    {feature.desc}
                  </p>

                  {/* Hover Action Button */}
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    whileHover={{ opacity: 1, y: 0 }}
                    className="mt-4 flex items-center gap-2 text-sm font-semibold text-success-600 dark:text-success-400 opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <span>Khám phá</span>
                    <motion.svg
                      animate={{ x: [0, 5, 0] }}
                      transition={{ duration: 1.5, repeat: Infinity }}
                      className="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </motion.svg>
                  </motion.div>
                </div>

                {/* Bottom Gradient Bar */}
                <motion.div
                  className={`absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r ${feature.gradient}`}
                  initial={{ scaleX: 0 }}
                  whileHover={{ scaleX: 1 }}
                  transition={{ duration: 0.3 }}
                  style={{ originX: 0 }}
                />
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-20 overflow-hidden sm:py-32">
        <div className="absolute inset-0 bg-gradient-to-br from-success-600 via-success-500 to-blue-light-500"></div>
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>

        <div className="relative px-4 mx-auto text-center max-w-7xl sm:px-6 lg:px-8">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="mb-6 font-bold text-white text-title-sm sm:text-title-md drop-shadow-lg"
          >
            Sẵn sàng{" "}
            <span className="bg-gradient-to-r from-white to-brand-100 bg-clip-text text-transparent">
              hành động xanh
            </span>
            ?
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="max-w-2xl mx-auto mb-10 text-lg text-white/90 sm:text-xl drop-shadow"
          >
            Tham gia cùng chúng tôi để xây dựng một thành phố xanh,
            bền vững và thân thiện với môi trường hơn.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="flex flex-col items-center justify-center gap-4 sm:flex-row"
          >
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link
                href="/map"
                className="inline-flex items-center justify-center w-full px-8 py-4 text-base font-semibold transition-all bg-white rounded-xl shadow-2xl text-success-700 hover:bg-success-50 hover:shadow-white/30 sm:w-auto group"
              >
                Khám phá ngay
                <motion.svg
                  className="w-5 h-5 ml-2"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  whileHover={{ x: 5 }}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 7l5 5m0 0l-5 5m5-5H6"
                  />
                </motion.svg>
              </Link>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link
                href="/feedback"
                className="inline-flex items-center justify-center w-full px-8 py-4 text-base font-semibold text-white transition-all border-2 border-white/50 backdrop-blur-sm rounded-xl hover:bg-white/10 hover:border-white sm:w-auto"
              >
                Gửi ý tưởng xanh
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-24 bg-gradient-to-b from-white to-gray-50 dark:from-gray-900 dark:to-gray-950 sm:py-40 overflow-hidden">
        <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8 mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h2 className="mb-4 font-black text-gray-900 text-4xl sm:text-5xl dark:text-white">
              Lời chứng thực từ cộng đồng
            </h2>
            <p className="max-w-2xl mx-auto text-lg text-gray-600 dark:text-gray-400">
              Những câu chuyện thành công từ những người sử dụng GreenEduMap
            </p>
          </motion.div>
        </div>

        {/* Testimonials Row 1 - Scroll Left */}
        <div className="mb-12 overflow-hidden">
          <motion.div
            animate={{ x: [0, -1920] }}
            transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
            className="flex gap-6"
          >
            {[
              {
                name: "Nguyễn Văn A",
                company: "Eco Living Vietnam",
                avatar: "NA",
                quote: "GreenEduMap đã giúp tôi hiểu rõ hơn về chất lượng không khí khu vực tôi sống.",
              },
              {
                name: "Trần Thị B",
                company: "Green Initiative HCM",
                avatar: "TB",
                quote: "Công cụ này thật sự hữu ích để lên kế hoạch các hoạt động môi trường.",
              },
              {
                name: "Phạm Minh C",
                company: "Sustainable Future",
                avatar: "PM",
                quote: "AI recommendations giúp tôi chọn hành động xanh phù hợp nhất.",
              },
              {
                name: "Lê Hoàng D",
                company: "EcoSchool Network",
                avatar: "LH",
                quote: "Dữ liệu thời gian thực trên bản đồ 3D rất ấn tượng và dễ hiểu.",
              },
              {
                name: "Võ Thị E",
                company: "Green Community",
                avatar: "VT",
                quote: "Tôi yêu cách GreenEduMap kết nối giáo dục và hành động thực tế.",
              },
              {
                name: "Đặng Văn F",
                company: "Urban Eco Solutions",
                avatar: "ĐV",
                quote: "Platform này là giải pháp hoàn hảo cho quản lý môi trường thành phố.",
              },
              {
                name: "Hồ Thị G",
                company: "Climate Action VN",
                avatar: "HT",
                quote: "Cộng đồng tham gia trên GreenEduMap rất năng động và sáng tạo.",
              },
              {
                name: "Bùi Minh H",
                company: "Green Tech Startup",
                avatar: "BM",
                quote: "Giao diện thân thiện giúp tôi dễ dàng theo dõi tiến độ.",
              },
              {
                name: "Nông Thị I",
                company: "Sustainable Education",
                avatar: "NT",
                quote: "Các khóa học môi trường trên platform rất chất lượng và thực tế.",
              },
              {
                name: "Tạ Văn J",
                company: "Green Vision Asia",
                avatar: "TV",
                quote: "GreenEduMap là ứng dụng tốt nhất mà tôi từng sử dụng cho đời sống xanh.",
              },
            ].map((testimonial, idx) => (
              <div
                key={`row1-${idx}`}
                className="flex-shrink-0 w-80 p-6 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg hover:shadow-xl transition-all"
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-14 h-14 rounded-full bg-gradient-to-br from-success-500 to-blue-light-500 flex items-center justify-center text-white font-bold text-lg shadow-lg">
                    {testimonial.avatar}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold text-gray-900 dark:text-white text-sm">
                      {testimonial.name}
                    </h4>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      {testimonial.company}
                    </p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-300 italic">
                  "{testimonial.quote}"
                </p>
                <div className="flex gap-1 mt-4">
                  {[...Array(5)].map((_, i) => (
                    <svg key={i} className="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
                      <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                    </svg>
                  ))}
                </div>
              </div>
            ))}
            {/* Duplicate for infinite loop */}
            {[
              {
                name: "Nguyễn Văn A",
                company: "Eco Living Vietnam",
                avatar: "NA",
                quote: "GreenEduMap đã giúp tôi hiểu rõ hơn về chất lượng không khí khu vực tôi sống.",
              },
              {
                name: "Trần Thị B",
                company: "Green Initiative HCM",
                avatar: "TB",
                quote: "Công cụ này thật sự hữu ích để lên kế hoạch các hoạt động môi trường.",
              },
              {
                name: "Phạm Minh C",
                company: "Sustainable Future",
                avatar: "PM",
                quote: "AI recommendations giúp tôi chọn hành động xanh phù hợp nhất.",
              },
              {
                name: "Lê Hoàng D",
                company: "EcoSchool Network",
                avatar: "LH",
                quote: "Dữ liệu thời gian thực trên bản đồ 3D rất ấn tượng và dễ hiểu.",
              },
              {
                name: "Võ Thị E",
                company: "Green Community",
                avatar: "VT",
                quote: "Tôi yêu cách GreenEduMap kết nối giáo dục và hành động thực tế.",
              },
              {
                name: "Đặng Văn F",
                company: "Urban Eco Solutions",
                avatar: "ĐV",
                quote: "Platform này là giải pháp hoàn hảo cho quản lý môi trường thành phố.",
              },
              {
                name: "Hồ Thị G",
                company: "Climate Action VN",
                avatar: "HT",
                quote: "Cộng đồng tham gia trên GreenEduMap rất năng động và sáng tạo.",
              },
              {
                name: "Bùi Minh H",
                company: "Green Tech Startup",
                avatar: "BM",
                quote: "Giao diện thân thiện giúp tôi dễ dàng theo dõi tiến độ.",
              },
              {
                name: "Nông Thị I",
                company: "Sustainable Education",
                avatar: "NT",
                quote: "Các khóa học môi trường trên platform rất chất lượng và thực tế.",
              },
              {
                name: "Tạ Văn J",
                company: "Green Vision Asia",
                avatar: "TV",
                quote: "GreenEduMap là ứng dụng tốt nhất mà tôi từng sử dụng cho đời sống xanh.",
              },
            ].map((testimonial, idx) => (
              <div
                key={`row1-dup-${idx}`}
                className="flex-shrink-0 w-80 p-6 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg hover:shadow-xl transition-all"
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-14 h-14 rounded-full bg-gradient-to-br from-success-500 to-blue-light-500 flex items-center justify-center text-white font-bold text-lg shadow-lg">
                    {testimonial.avatar}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold text-gray-900 dark:text-white text-sm">
                      {testimonial.name}
                    </h4>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      {testimonial.company}
                    </p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-300 italic">
                  "{testimonial.quote}"
                </p>
                <div className="flex gap-1 mt-4">
                  {[...Array(5)].map((_, i) => (
                    <svg key={i} className="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
                      <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                    </svg>
                  ))}
                </div>
              </div>
            ))}
          </motion.div>
        </div>

        {/* Testimonials Row 2 - Scroll Right */}
        <div className="overflow-hidden">
          <motion.div
            animate={{ x: [-1920, 0] }}
            transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
            className="flex gap-6"
          >
            {[
              {
                name: "Đinh Văn K",
                company: "Green Innovation Lab",
                avatar: "ĐK",
                quote: "Bản đồ 3D giúp tôi nhìn thấy cảnh quan môi trường theo cách hoàn toàn mới.",
              },
              {
                name: "Cao Thị L",
                company: "EcoEducation Foundation",
                avatar: "CT",
                quote: "Giáo dục môi trường được kết hợp với hành động thực tế quá tuyệt vời.",
              },
              {
                name: "Vũ Minh M",
                company: "City Sustainability",
                avatar: "VM",
                quote: "Công cụ phân tích dữ liệu của GreenEduMap giúp tôi đưa ra quyết định tốt hơn.",
              },
              {
                name: "Trương Thị N",
                company: "Green NGO Vietnam",
                avatar: "TT",
                quote: "Cộng đồng trên GreenEduMap rất hỗ trợ và tích cực.",
              },
              {
                name: "Hoàng Văn O",
                company: "Environmental Tech",
                avatar: "HV",
                quote: "GreenEduMap là nền tảng tốt nhất cho quản lý môi trường toàn diện.",
              },
              {
                name: "Mai Thị P",
                company: "Green School Network",
                avatar: "MT",
                quote: "Các khóa học trên platform rất phù hợp cho học sinh và giáo viên.",
              },
              {
                name: "Sơn Văn Q",
                company: "Sustainable City Project",
                avatar: "SV",
                quote: "Dữ liệu thời gian thực giúp tôi theo dõi tiến độ bảo vệ môi trường.",
              },
              {
                name: "Linh Thị R",
                company: "Green Business Solutions",
                avatar: "LT",
                quote: "Platform này thay đổi cách tôi suy nghĩ về phát triển bền vững.",
              },
              {
                name: "Quân Văn S",
                company: "Climate Change Institute",
                avatar: "QV",
                quote: "Công cụ AI của GreenEduMap rất thông minh và hữu ích.",
              },
              {
                name: "Yến Thị T",
                company: "Green Future Movement",
                avatar: "YT",
                quote: "Tôi khuyên bất kỳ ai quan tâm đến môi trường nên dùng GreenEduMap.",
              },
            ].map((testimonial, idx) => (
              <div
                key={`row2-${idx}`}
                className="flex-shrink-0 w-80 p-6 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg hover:shadow-xl transition-all"
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-14 h-14 rounded-full bg-gradient-to-br from-blue-light-500 to-success-500 flex items-center justify-center text-white font-bold text-lg shadow-lg">
                    {testimonial.avatar}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold text-gray-900 dark:text-white text-sm">
                      {testimonial.name}
                    </h4>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      {testimonial.company}
                    </p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-300 italic">
                  "{testimonial.quote}"
                </p>
                <div className="flex gap-1 mt-4">
                  {[...Array(5)].map((_, i) => (
                    <svg key={i} className="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
                      <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                    </svg>
                  ))}
                </div>
              </div>
            ))}
            {/* Duplicate for infinite loop */}
            {[
              {
                name: "Đinh Văn K",
                company: "Green Innovation Lab",
                avatar: "ĐK",
                quote: "Bản đồ 3D giúp tôi nhìn thấy cảnh quan môi trường theo cách hoàn toàn mới.",
              },
              {
                name: "Cao Thị L",
                company: "EcoEducation Foundation",
                avatar: "CT",
                quote: "Giáo dục môi trường được kết hợp với hành động thực tế quá tuyệt vời.",
              },
              {
                name: "Vũ Minh M",
                company: "City Sustainability",
                avatar: "VM",
                quote: "Công cụ phân tích dữ liệu của GreenEduMap giúp tôi đưa ra quyết định tốt hơn.",
              },
              {
                name: "Trương Thị N",
                company: "Green NGO Vietnam",
                avatar: "TT",
                quote: "Cộng đồng trên GreenEduMap rất hỗ trợ và tích cực.",
              },
              {
                name: "Hoàng Văn O",
                company: "Environmental Tech",
                avatar: "HV",
                quote: "GreenEduMap là nền tảng tốt nhất cho quản lý môi trường toàn diện.",
              },
              {
                name: "Mai Thị P",
                company: "Green School Network",
                avatar: "MT",
                quote: "Các khóa học trên platform rất phù hợp cho học sinh và giáo viên.",
              },
              {
                name: "Sơn Văn Q",
                company: "Sustainable City Project",
                avatar: "SV",
                quote: "Dữ liệu thời gian thực giúp tôi theo dõi tiến độ bảo vệ môi trường.",
              },
              {
                name: "Linh Thị R",
                company: "Green Business Solutions",
                avatar: "LT",
                quote: "Platform này thay đổi cách tôi suy nghĩ về phát triển bền vững.",
              },
              {
                name: "Quân Văn S",
                company: "Climate Change Institute",
                avatar: "QV",
                quote: "Công cụ AI của GreenEduMap rất thông minh và hữu ích.",
              },
              {
                name: "Yến Thị T",
                company: "Green Future Movement",
                avatar: "YT",
                quote: "Tôi khuyên bất kỳ ai quan tâm đến môi trường nên dùng GreenEduMap.",
              },
            ].map((testimonial, idx) => (
              <div
                key={`row2-dup-${idx}`}
                className="flex-shrink-0 w-80 p-6 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg hover:shadow-xl transition-all"
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-14 h-14 rounded-full bg-gradient-to-br from-blue-light-500 to-success-500 flex items-center justify-center text-white font-bold text-lg shadow-lg">
                    {testimonial.avatar}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold text-gray-900 dark:text-white text-sm">
                      {testimonial.name}
                    </h4>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      {testimonial.company}
                    </p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-300 italic">
                  "{testimonial.quote}"
                </p>
                <div className="flex gap-1 mt-4">
                  {[...Array(5)].map((_, i) => (
                    <svg key={i} className="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
                      <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                    </svg>
                  ))}
                </div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-gradient-to-b from-gray-900 to-gray-950 border-t border-gray-800">
        <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
            <div className="md:col-span-2">
              <motion.div
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                className="flex items-center gap-2 mb-4"
              >
                <img src="/images/logo/logo.svg" alt="GreenEduMap Logo" className="h-10 w-auto" />
              </motion.div>
              <p className="mb-4 text-gray-400">
                Bản đồ sống xanh & Giáo dục môi trường cho tương lai bền vững.
              </p>
              <p className="text-sm text-gray-500">
                © 2025 GreenEduMap. All rights reserved.
              </p>
            </div>

            <div>
              <h3 className="mb-4 text-sm font-semibold text-white uppercase tracking-wider">
                Khám phá
              </h3>
              <ul className="space-y-2">
                {[
                  { name: "Bản đồ", href: "/map" },
                  { name: "Hành động xanh", href: "/actions" },
                  { name: "Thống kê", href: "/stats" },
                ].map((item, index) => (
                  <motion.li
                    key={item.name}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <a
                      href={item.href}
                      className="text-gray-400 transition-colors hover:text-success-400 relative group inline-block"
                    >
                      {item.name}
                      <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-success-500 to-success-600 transition-all group-hover:w-full" />
                    </a>
                  </motion.li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="mb-4 text-sm font-semibold text-white uppercase tracking-wider">
                Liên hệ
              </h3>
              <ul className="space-y-2">
                {["Về chúng tôi", "Chat với AI", "Liên hệ"].map((item, index) => (
                  <motion.li
                    key={item}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <a
                      href={item === "Chat với AI" ? "/chat" : "#"}
                      className="text-gray-400 transition-colors hover:text-success-400 relative group inline-block"
                    >
                      {item}
                      <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-success-500 to-success-600 transition-all group-hover:w-full" />
                    </a>
                  </motion.li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
