"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";

export default function SchoolDashboardPage() {
  const stats = {
    totalStudents: 1248,
    totalCourses: 12,
    activeClasses: 8,
    completionRate: 87,
  };

  const recentCourses = [
    { id: 1, title: "Bảo vệ môi trường sống", students: 156, status: "active" },
    { id: 2, title: "Năng lượng tái tạo", students: 203, status: "active" },
    { id: 3, title: "Xử lý rác thải thông minh", students: 98, status: "completed" },
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-40">
        <div className="px-4 py-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/" className="flex items-center gap-2">
                <img src="/images/logo/logo.svg" alt="GreenEduMap" className="h-8 w-auto" />
                <span className="text-lg font-bold bg-gradient-to-r from-success-600 to-success-500 bg-clip-text text-transparent">
                  GreenEduMap
                </span>
              </Link>
              <span className="text-gray-400">|</span>
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
                🏫 Dashboard Trường học
              </h1>
            </div>
          </div>
        </div>
      </header>

      <div className="px-4 py-8 mx-auto max-w-7xl sm:px-6 lg:px-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 gap-6 mb-8 md:grid-cols-2 lg:grid-cols-4">
          {[
            { label: "Tổng học viên", value: stats.totalStudents, icon: "👥", color: "blue" },
            { label: "Khóa học", value: stats.totalCourses, icon: "📚", color: "purple" },
            { label: "Lớp đang học", value: stats.activeClasses, icon: "🎓", color: "success" },
            { label: "Tỷ lệ hoàn thành", value: `${stats.completionRate}%`, icon: "✅", color: "warning" },
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-3xl">{stat.icon}</span>
              </div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                {stat.value}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Recent Courses */}
        <div className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Khóa học gần đây
            </h2>
            <Link
              href="/school/courses"
              className="px-4 py-2 text-sm font-medium text-white rounded-lg bg-gradient-to-r from-success-500 to-success-600 hover:shadow-lg"
            >
              Xem tất cả
            </Link>
          </div>
          <div className="space-y-4">
            {recentCourses.map((course) => (
              <div
                key={course.id}
                className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
              >
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    {course.title}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {course.students} học viên
                  </p>
                </div>
                <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                  course.status === "active"
                    ? "bg-success-100 text-success-700 dark:bg-success-500/20 dark:text-success-400"
                    : "bg-gray-100 text-gray-700 dark:bg-gray-600 dark:text-gray-300"
                }`}>
                  {course.status === "active" ? "Đang hoạt động" : "Đã hoàn thành"}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-6">
          <h2 className="mb-4 text-xl font-semibold text-gray-900 dark:text-white">
            Thao tác nhanh
          </h2>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <Link
              href="/school/new"
              className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition-shadow border-2 border-dashed border-gray-300 dark:border-gray-700 hover:border-success-500 text-center"
            >
              <div className="text-4xl mb-2">➕</div>
              <div className="font-semibold text-gray-900 dark:text-white">
                Tạo khóa học mới
              </div>
            </Link>
            <Link
              href="/school/courses"
              className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition-shadow"
            >
              <div className="text-4xl mb-2">📚</div>
              <div className="font-semibold text-gray-900 dark:text-white">
                Quản lý khóa học
              </div>
            </Link>
            <Link
              href="/school/profile"
              className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition-shadow"
            >
              <div className="text-4xl mb-2">👤</div>
              <div className="font-semibold text-gray-900 dark:text-white">
                Hồ sơ trường
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

