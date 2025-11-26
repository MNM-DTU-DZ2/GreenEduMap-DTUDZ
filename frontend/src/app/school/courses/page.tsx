"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";

export default function SchoolCoursesPage() {
  const [searchQuery, setSearchQuery] = useState("");

  const courses = [
    {
      id: 1,
      title: "Bảo vệ môi trường sống",
      description: "Khóa học về cách bảo vệ và cải thiện môi trường sống xung quanh chúng ta",
      students: 156,
      status: "active",
      duration: "8 tuần",
      createdAt: "2024-01-15",
    },
    {
      id: 2,
      title: "Năng lượng tái tạo",
      description: "Tìm hiểu về các nguồn năng lượng tái tạo và cách sử dụng hiệu quả",
      students: 203,
      status: "active",
      duration: "10 tuần",
      createdAt: "2024-02-01",
    },
    {
      id: 3,
      title: "Xử lý rác thải thông minh",
      description: "Học cách phân loại và xử lý rác thải một cách hiệu quả",
      students: 98,
      status: "completed",
      duration: "6 tuần",
      createdAt: "2023-12-10",
    },
    {
      id: 4,
      title: "Biến đổi khí hậu và giải pháp",
      description: "Tìm hiểu về biến đổi khí hậu và các giải pháp thực tế",
      students: 142,
      status: "active",
      duration: "12 tuần",
      createdAt: "2024-02-20",
    },
  ];

  const filteredCourses = courses.filter(course =>
    course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    course.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-40">
        <div className="px-4 py-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/school/dashboard" className="flex items-center gap-2">
                <img src="/images/logo/logo.svg" alt="GreenEduMap" className="h-8 w-auto" />
                <span className="text-lg font-bold bg-gradient-to-r from-success-600 to-success-500 bg-clip-text text-transparent">
                  GreenEduMap
                </span>
              </Link>
              <span className="text-gray-400">|</span>
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
                📚 Quản lý khóa học
              </h1>
            </div>
          </div>
        </div>
      </header>

      <div className="px-4 py-8 mx-auto max-w-7xl sm:px-6 lg:px-8">
        {/* Header Actions */}
        <div className="flex flex-col gap-4 mb-8 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="mb-2 text-2xl font-bold text-gray-900 dark:text-white">
              Danh sách khóa học
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Quản lý và theo dõi các khóa học môi trường của bạn
            </p>
          </div>
          <Link
            href="/school/new"
            className="px-6 py-3 font-semibold text-white transition-all rounded-xl bg-gradient-to-r from-success-500 to-success-600 hover:shadow-lg hover:shadow-success-500/50"
          >
            ➕ Tạo khóa học mới
          </Link>
        </div>

        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Tìm kiếm khóa học..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent"
          />
        </div>

        {/* Courses Grid */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredCourses.map((course, index) => (
            <motion.div
              key={course.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition-shadow border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="mb-2 text-xl font-semibold text-gray-900 dark:text-white">
                    {course.title}
                  </h3>
                  <p className="mb-4 text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                    {course.description}
                  </p>
                </div>
              </div>

              <div className="space-y-2 mb-4">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Học viên:</span>
                  <span className="font-semibold text-gray-900 dark:text-white">{course.students}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Thời lượng:</span>
                  <span className="font-semibold text-gray-900 dark:text-white">{course.duration}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Ngày tạo:</span>
                  <span className="font-semibold text-gray-900 dark:text-white">{course.createdAt}</span>
                </div>
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
                <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                  course.status === "active"
                    ? "bg-success-100 text-success-700 dark:bg-success-500/20 dark:text-success-400"
                    : "bg-gray-100 text-gray-700 dark:bg-gray-600 dark:text-gray-300"
                }`}>
                  {course.status === "active" ? "Đang hoạt động" : "Đã hoàn thành"}
                </span>
                <button className="px-4 py-2 text-sm font-medium text-success-600 dark:text-success-400 hover:bg-success-50 dark:hover:bg-success-500/10 rounded-lg transition-colors">
                  Chi tiết
                </button>
              </div>
            </motion.div>
          ))}
        </div>

        {filteredCourses.length === 0 && (
          <div className="py-12 text-center">
            <p className="text-gray-500 dark:text-gray-400">
              Không tìm thấy khóa học nào.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

