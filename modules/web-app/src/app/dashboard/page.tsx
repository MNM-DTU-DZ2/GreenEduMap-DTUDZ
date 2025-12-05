"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { 
  Wind, 
  Cloud, 
  School, 
  TreePine, 
  Zap, 
  TrendingUp, 
  AlertTriangle,
  RefreshCw,
  MapPin
} from "lucide-react";
import PublicHeader from "@/components/common/PublicHeader";
import { useAirQualityLatest, useWeather } from "@/hooks/useAirQuality";
import { useSchools, useTopGreenSchools } from "@/hooks/useSchools";
import { useGreenZones, useGreenResources } from "@/hooks/useGreenZones";
import { useClusteringTask, usePredictionTask, useCorrelationTask } from "@/hooks/useAITasks";

// AQI Category Helper
function getAQICategory(aqi: number) {
  if (aqi <= 50) return { label: "Tốt", color: "text-green-600", bg: "bg-green-100 dark:bg-green-900/30" };
  if (aqi <= 100) return { label: "Trung bình", color: "text-yellow-600", bg: "bg-yellow-100 dark:bg-yellow-900/30" };
  if (aqi <= 150) return { label: "Không tốt", color: "text-orange-600", bg: "bg-orange-100 dark:bg-orange-900/30" };
  if (aqi <= 200) return { label: "Xấu", color: "text-red-600", bg: "bg-red-100 dark:bg-red-900/30" };
  return { label: "Rất xấu", color: "text-purple-600", bg: "bg-purple-100 dark:bg-purple-900/30" };
}

export default function DashboardPage() {
  const [refreshKey, setRefreshKey] = useState(0);

  // Fetch data from backend
  const { data: aqiData, isLoading: aqiLoading, refetch: refetchAQI } = useAirQualityLatest(10);
  const { data: weatherData, isLoading: weatherLoading } = useWeather(0, 5);
  const { data: schools, isLoading: schoolsLoading } = useSchools(0, 10);
  const { data: topSchools, isLoading: topSchoolsLoading } = useTopGreenSchools(5);
  const { data: greenZones, isLoading: zonesLoading } = useGreenZones(0, 10);
  const { data: greenResources, isLoading: resourcesLoading } = useGreenResources(0, 10);

  // AI Tasks
  const clusteringTask = useClusteringTask();
  const predictionTask = usePredictionTask();
  const correlationTask = useCorrelationTask();

  // Calculate stats
  const totalSchools = schools?.length || 0;
  const totalZones = greenZones?.length || 0;
  const totalResources = greenResources?.reduce((sum: number, r: any) => sum + (r.quantity || 0), 0) || 0;
  const avgAQI = aqiData?.data?.length 
    ? (aqiData.data.reduce((sum: number, item: any) => sum + (item.aqi || 0), 0) / aqiData.data.length).toFixed(1)
    : "N/A";

  const handleRefresh = () => {
    refetchAQI();
    setRefreshKey(prev => prev + 1);
  };

  const handleRunAI = async (type: "clustering" | "prediction" | "correlation") => {
    try {
      if (type === "clustering") {
        await clusteringTask.mutateAsync(3);
        alert("✅ Clustering task queued! Check AI Service logs.");
      } else if (type === "prediction") {
        await predictionTask.mutateAsync();
        alert("✅ Prediction task queued! Check AI Service logs.");
      } else {
        await correlationTask.mutateAsync("pearson");
        alert("✅ Correlation task queued! Check AI Service logs.");
      }
    } catch (error) {
      alert("❌ Failed to queue task: " + error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950">
      <PublicHeader />

      <div className="pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-black text-gray-900 dark:text-white mb-2">
              Dashboard
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Tổng quan hệ thống GreenEduMap
            </p>
          </div>
          <button
            onClick={handleRefresh}
            className="flex items-center gap-2 px-4 py-2 bg-success-600 text-white rounded-lg hover:bg-success-700 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Làm mới
          </button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {[
            {
              label: "AQI Trung bình",
              value: avgAQI,
              icon: Wind,
              color: "from-green-500 to-green-600",
              loading: aqiLoading,
            },
            {
              label: "Trường học",
              value: totalSchools,
              icon: School,
              color: "from-purple-500 to-purple-600",
              loading: schoolsLoading,
            },
            {
              label: "Khu vực xanh",
              value: totalZones,
              icon: TreePine,
              color: "from-success-500 to-success-600",
              loading: zonesLoading,
            },
            {
              label: "Tài nguyên",
              value: totalResources,
              icon: Zap,
              color: "from-amber-500 to-amber-600",
              loading: resourcesLoading,
            },
          ].map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg hover:shadow-xl transition-all"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-lg bg-gradient-to-br ${stat.color}`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
              </div>
              <div className="text-3xl font-black text-gray-900 dark:text-white mb-1">
                {stat.loading ? "..." : stat.value}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Latest AQI Data */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg"
          >
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Wind className="w-5 h-5 text-success-600" />
              Chất lượng không khí mới nhất
            </h2>
            {aqiLoading ? (
              <div className="text-gray-600 dark:text-gray-400">Đang tải...</div>
            ) : aqiData?.data && aqiData.data.length > 0 ? (
              <div className="space-y-3">
                {aqiData.data.slice(0, 5).map((item: any, index: number) => {
                  const category = getAQICategory(item.aqi || 0);
                  return (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-900/50"
                    >
                      <div className="flex items-center gap-3">
                        <MapPin className="w-4 h-4 text-gray-400" />
                        <div>
                          <div className="font-semibold text-gray-900 dark:text-white text-sm">
                            {item.station_name || `Station ${item.id}`}
                          </div>
                          <div className="text-xs text-gray-500">
                            PM2.5: {item.pm25?.toFixed(1) || "N/A"} µg/m³
                          </div>
                        </div>
                      </div>
                      <div className={`px-3 py-1 rounded-full ${category.bg} ${category.color} text-xs font-bold`}>
                        AQI {item.aqi?.toFixed(0) || "N/A"}
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-gray-500 dark:text-gray-400">Không có dữ liệu</div>
            )}
          </motion.div>

          {/* Weather Data */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg"
          >
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Cloud className="w-5 h-5 text-blue-600" />
              Thời tiết
            </h2>
            {weatherLoading ? (
              <div className="text-gray-600 dark:text-gray-400">Đang tải...</div>
            ) : weatherData?.data && weatherData.data.length > 0 ? (
              <div className="space-y-3">
                {weatherData.data.slice(0, 5).map((item: any, index: number) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-900/50"
                  >
                    <div>
                      <div className="font-semibold text-gray-900 dark:text-white text-sm">
                        {item.city_name || "Unknown"}
                      </div>
                      <div className="text-xs text-gray-500">
                        {item.weather_description || "N/A"}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-gray-900 dark:text-white">
                        {item.temperature?.toFixed(1) || "N/A"}°C
                      </div>
                      <div className="text-xs text-gray-500">
                        Độ ẩm: {item.humidity || "N/A"}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-gray-500 dark:text-gray-400">Không có dữ liệu</div>
            )}
          </motion.div>
        </div>

        {/* Top Green Schools */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg mb-8"
        >
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-success-600" />
            Top trường học xanh
          </h2>
          {topSchoolsLoading ? (
            <div className="text-gray-600 dark:text-gray-400">Đang tải...</div>
          ) : topSchools && topSchools.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {topSchools.slice(0, 6).map((school: any, index: number) => (
                <div
                  key={school.id}
                  className="p-4 rounded-lg bg-gradient-to-br from-success-50 to-green-50 dark:from-success-900/20 dark:to-green-900/20 border border-success-200 dark:border-success-800"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="font-semibold text-gray-900 dark:text-white text-sm mb-1">
                        {school.name}
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">
                        {school.district || school.city || ""}
                      </div>
                    </div>
                    <div className="px-2 py-1 rounded-full bg-success-600 text-white text-xs font-bold">
                      #{index + 1}
                    </div>
                  </div>
                  <div className="flex items-center gap-2 mt-3">
                    <div className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-success-500 to-green-500"
                        style={{ width: `${school.green_score || 0}%` }}
                      />
                    </div>
                    <div className="text-sm font-bold text-success-600">
                      {school.green_score?.toFixed(1) || "N/A"}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-gray-500 dark:text-gray-400">Không có dữ liệu</div>
          )}
        </motion.div>

        {/* AI Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="p-6 rounded-xl bg-gradient-to-br from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 border border-purple-200 dark:border-purple-800 shadow-lg"
        >
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-purple-600" />
            AI Analysis
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Chạy các phân tích AI để nhận insights về môi trường và giáo dục
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              {
                label: "Clustering",
                desc: "Phân vùng xanh/vàng/đỏ",
                action: () => handleRunAI("clustering"),
                loading: clusteringTask.isPending,
              },
              {
                label: "Prediction",
                desc: "Dự báo AQI 7 ngày",
                action: () => handleRunAI("prediction"),
                loading: predictionTask.isPending,
              },
              {
                label: "Correlation",
                desc: "Phân tích tương quan",
                action: () => handleRunAI("correlation"),
                loading: correlationTask.isPending,
              },
            ].map((ai, index) => (
              <button
                key={index}
                onClick={ai.action}
                disabled={ai.loading}
                className="p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-purple-400 dark:hover:border-purple-600 transition-all text-left disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div className="font-semibold text-gray-900 dark:text-white mb-1">
                  {ai.loading ? "Đang xử lý..." : ai.label}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-400">
                  {ai.desc}
                </div>
              </button>
            ))}
          </div>
        </motion.div>

        {/* Green Zones & Resources */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg"
          >
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <TreePine className="w-5 h-5 text-green-600" />
              Khu vực xanh
            </h2>
            {zonesLoading ? (
              <div className="text-gray-600 dark:text-gray-400">Đang tải...</div>
            ) : greenZones && greenZones.length > 0 ? (
              <div className="space-y-2">
                {greenZones.slice(0, 5).map((zone: any) => (
                  <div
                    key={zone.id}
                    className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-900/50"
                  >
                    <div>
                      <div className="font-semibold text-gray-900 dark:text-white text-sm">
                        {zone.name}
                      </div>
                      <div className="text-xs text-gray-500">
                        {zone.zone_type} • {zone.tree_count} cây
                      </div>
                    </div>
                    <div className="text-xs text-success-600 font-semibold">
                      {zone.area_sqm ? `${(zone.area_sqm / 1000).toFixed(1)}k m²` : "N/A"}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-gray-500 dark:text-gray-400">Không có dữ liệu</div>
            )}
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg"
          >
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-600" />
              Tài nguyên xanh
            </h2>
            {resourcesLoading ? (
              <div className="text-gray-600 dark:text-gray-400">Đang tải...</div>
            ) : greenResources && greenResources.length > 0 ? (
              <div className="space-y-2">
                {greenResources.slice(0, 5).map((resource: any) => (
                  <div
                    key={resource.id}
                    className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-900/50"
                  >
                    <div>
                      <div className="font-semibold text-gray-900 dark:text-white text-sm">
                        {resource.name}
                      </div>
                      <div className="text-xs text-gray-500">
                        {resource.type}
                      </div>
                    </div>
                    <div className="text-xs text-amber-600 font-semibold">
                      {resource.quantity} {resource.unit}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-gray-500 dark:text-gray-400">Không có dữ liệu</div>
            )}
          </motion.div>
        </div>

        {/* System Status */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg"
        >
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Trạng thái hệ thống
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "API Gateway", status: "online" },
              { label: "Education Service", status: schools ? "online" : "offline" },
              { label: "Environment Service", status: aqiData ? "online" : "offline" },
              { label: "Resource Service", status: greenZones ? "online" : "offline" },
            ].map((service, index) => (
              <div
                key={index}
                className="p-4 rounded-lg bg-gray-50 dark:bg-gray-900/50 text-center"
              >
                <div className={`inline-flex items-center justify-center w-3 h-3 rounded-full mb-2 ${
                  service.status === "online" ? "bg-green-500" : "bg-red-500"
                }`} />
                <div className="text-xs font-semibold text-gray-900 dark:text-white">
                  {service.label}
                </div>
                <div className={`text-xs mt-1 ${
                  service.status === "online" ? "text-green-600" : "text-red-600"
                }`}>
                  {service.status === "online" ? "Online" : "Offline"}
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}

