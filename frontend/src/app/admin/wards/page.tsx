"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import AdminPageHeader from "@/components/admin/AdminPageHeader";
import AdminDataTable from "@/components/admin/AdminDataTable";
import AdminStatsCard from "@/components/admin/AdminStatsCard";
import { MapPin, Users, Home, TrendingUp } from "lucide-react";

interface Ward {
  id: number;
  name: string;
  district: string;
  population: number;
  aqi: number;
  greenSpaces: number;
  schools: number;
  boundingBox: {
    north: number;
    south: number;
    east: number;
    west: number;
  };
}

export default function AdminWardsPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDistrict, setSelectedDistrict] = useState("all");

  const wards: Ward[] = [
    {
      id: 1,
      name: "Phường 1",
      district: "Quận 1",
      population: 15420,
      aqi: 65,
      greenSpaces: 12,
      schools: 5,
      boundingBox: {
        north: 10.78,
        south: 10.76,
        east: 106.70,
        west: 106.68,
      },
    },
    {
      id: 2,
      name: "Phường 2",
      district: "Quận 1",
      population: 18230,
      aqi: 58,
      greenSpaces: 15,
      schools: 7,
      boundingBox: {
        north: 10.80,
        south: 10.78,
        east: 106.72,
        west: 106.70,
      },
    },
    {
      id: 3,
      name: "Phường 1",
      district: "Quận 2",
      population: 12150,
      aqi: 72,
      greenSpaces: 8,
      schools: 4,
      boundingBox: {
        north: 10.82,
        south: 10.80,
        east: 106.74,
        west: 106.72,
      },
    },
  ];

  const filteredWards = wards.filter(ward => {
    const matchesSearch = ward.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ward.district.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDistrict = selectedDistrict === "all" || ward.district === selectedDistrict;
    return matchesSearch && matchesDistrict;
  });

  const districts = Array.from(new Set(wards.map(w => w.district)));

  const totalStats = {
    totalWards: wards.length,
    totalPopulation: wards.reduce((sum, w) => sum + w.population, 0),
    avgAQI: Math.round(wards.reduce((sum, w) => sum + w.aqi, 0) / wards.length),
    totalGreenSpaces: wards.reduce((sum, w) => sum + w.greenSpaces, 0),
  };

  const columns = [
    {
      key: "name",
      label: "Tên phường",
    },
    {
      key: "district",
      label: "Quận",
    },
    {
      key: "population",
      label: "Dân số",
      render: (value: number) => value.toLocaleString(),
    },
    {
      key: "aqi",
      label: "AQI",
      render: (value: number) => (
        <span className={`font-semibold ${
          value < 50 ? "text-success-600" : value < 100 ? "text-warning-600" : "text-danger-600"
        }`}>
          {value}
        </span>
      ),
    },
    {
      key: "greenSpaces",
      label: "Khu vực xanh",
      render: (value: number) => `${value} khu vực`,
    },
    {
      key: "schools",
      label: "Trường học",
      render: (value: number) => `${value} trường`,
    },
    {
      key: "actions",
      label: "Thao tác",
      render: (_: unknown, row: Ward) => (
        <button className="px-3 py-1 text-sm font-medium text-success-600 dark:text-success-400 hover:bg-success-50 dark:hover:bg-success-500/10 rounded-lg">
          Xem chi tiết
        </button>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <AdminPageHeader
        title="Quản lý phường"
        description="Quản lý dữ liệu môi trường và giáo dục theo từng phường"
      />

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
        <AdminStatsCard
          title="Tổng số phường"
          value={totalStats.totalWards}
          icon={MapPin}
          color="blue"
          description="Đang theo dõi"
        />
        <AdminStatsCard
          title="Tổng dân số"
          value={totalStats.totalPopulation.toLocaleString()}
          icon={Users}
          color="green"
          description="Người"
        />
        <AdminStatsCard
          title="AQI trung bình"
          value={totalStats.avgAQI}
          icon={TrendingUp}
          color="orange"
          description="Chỉ số chất lượng không khí"
        />
        <AdminStatsCard
          title="Khu vực xanh"
          value={totalStats.totalGreenSpaces}
          icon={Home}
          color="purple"
          description="Tổng số khu vực"
        />
      </div>

      {/* Filters */}
      <div className="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm dark:border-white/[0.08] dark:bg-gray-900/60">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Lọc theo quận:
            </label>
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500"
            >
              <option value="all">Tất cả quận</option>
              {districts.map(district => (
                <option key={district} value={district}>{district}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-white/[0.08] dark:bg-gray-900/60">
        <AdminDataTable
          columns={columns}
          data={filteredWards}
          searchable
          searchPlaceholder="Tìm theo tên phường hoặc quận..."
          onSearch={setSearchQuery}
          emptyMessage="Không có dữ liệu phường"
        />
      </div>
    </div>
  );
}

