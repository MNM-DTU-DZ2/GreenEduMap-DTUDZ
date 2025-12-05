"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { 
  BookOpen, 
  Clock, 
  Users, 
  Calendar,
  Search,
  Filter,
  GraduationCap,
  Leaf,
  Droplet,
  Recycle,
  TreePine,
  Zap
} from "lucide-react";
import PublicHeader from "@/components/common/PublicHeader";
import { useGreenCourses } from "@/hooks/useSchools";

// Category icons
const categoryIcons: Record<string, any> = {
  Energy: Zap,
  Waste: Recycle,
  Water: Droplet,
  Biodiversity: TreePine,
  General: Leaf,
};

// Category colors
const categoryColors: Record<string, string> = {
  Energy: "from-amber-500 to-orange-500",
  Waste: "from-green-500 to-emerald-500",
  Water: "from-blue-500 to-cyan-500",
  Biodiversity: "from-green-600 to-teal-600",
  General: "from-success-500 to-green-500",
};

export default function CoursesPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const { data: courses, isLoading } = useGreenCourses(0, 100);

  // Filter courses
  const filteredCourses = courses?.filter((course: any) => {
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      course.description?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = !selectedCategory || course.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const categories = ["Energy", "Waste", "Water", "Biodiversity", "General"];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950">
      <PublicHeader />

      <div className="pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-black text-gray-900 dark:text-white mb-4">
            Khóa học{" "}
            <span className="bg-gradient-to-r from-success-600 to-green-500 bg-clip-text text-transparent">
              Môi trường
            </span>
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Học tập và hành động vì một tương lai xanh, bền vững
          </p>
        </motion.div>

        {/* Search & Filter */}
        <div className="mb-8 space-y-4">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Tìm kiếm khóa học..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent transition-all"
            />
          </div>

          {/* Category Filter */}
          <div className="flex items-center gap-3 overflow-x-auto pb-2">
            <div className="flex items-center gap-2 text-sm font-semibold text-gray-700 dark:text-gray-300 whitespace-nowrap">
              <Filter className="w-4 h-4" />
              Danh mục:
            </div>
            <button
              onClick={() => setSelectedCategory(null)}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all whitespace-nowrap ${
                !selectedCategory
                  ? "bg-success-600 text-white"
                  : "bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700"
              }`}
            >
              Tất cả
            </button>
            {categories.map((category) => {
              const Icon = categoryIcons[category] || Leaf;
              return (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all whitespace-nowrap ${
                    selectedCategory === category
                      ? "bg-success-600 text-white"
                      : "bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {category}
                </button>
              );
            })}
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {[
            {
              label: "Tổng khóa học",
              value: courses?.length || 0,
              icon: BookOpen,
              color: "from-purple-500 to-purple-600",
            },
            {
              label: "Đang hoạt động",
              value: courses?.filter((c: any) => c.is_active).length || 0,
              icon: GraduationCap,
              color: "from-success-500 to-green-500",
            },
            {
              label: "Danh mục",
              value: categories.length,
              icon: Leaf,
              color: "from-blue-500 to-cyan-500",
            },
          ].map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg"
            >
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-lg bg-gradient-to-br ${stat.color}`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <div className="text-3xl font-black text-gray-900 dark:text-white">
                    {stat.value}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {stat.label}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Courses Grid */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-success-600"></div>
            <p className="mt-4 text-gray-600 dark:text-gray-400">Đang tải khóa học...</p>
          </div>
        ) : filteredCourses && filteredCourses.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCourses.map((course: any, index: number) => {
              const Icon = categoryIcons[course.category] || Leaf;
              const gradient = categoryColors[course.category] || categoryColors.General;

              return (
                <motion.div
                  key={course.id}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  whileHover={{ y: -8, scale: 1.02 }}
                  className="group relative p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg hover:shadow-2xl transition-all cursor-pointer overflow-hidden"
                >
                  {/* Gradient Overlay */}
                  <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-0 group-hover:opacity-5 transition-opacity`} />

                  {/* Active Badge */}
                  {course.is_active && (
                    <div className="absolute top-4 right-4 px-2 py-1 rounded-full bg-success-600 text-white text-xs font-bold">
                      Đang mở
                    </div>
                  )}

                  {/* Category Icon */}
                  <div className={`inline-flex p-3 rounded-lg bg-gradient-to-br ${gradient} mb-4`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>

                  {/* Title */}
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2 group-hover:text-success-600 dark:group-hover:text-success-400 transition-colors">
                    {course.title}
                  </h3>

                  {/* Description */}
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
                    {course.description || "Khóa học về môi trường và phát triển bền vững"}
                  </p>

                  {/* Meta Info */}
                  <div className="space-y-2 mb-4">
                    {course.duration_weeks && (
                      <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <Clock className="w-4 h-4" />
                        <span>{course.duration_weeks} tuần</span>
                      </div>
                    )}
                    {course.instructor_name && (
                      <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <GraduationCap className="w-4 h-4" />
                        <span>{course.instructor_name}</span>
                      </div>
                    )}
                    {course.max_participants && (
                      <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <Users className="w-4 h-4" />
                        <span>Tối đa {course.max_participants} người</span>
                      </div>
                    )}
                    {course.start_date && (
                      <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <Calendar className="w-4 h-4" />
                        <span>
                          Bắt đầu: {new Date(course.start_date).toLocaleDateString("vi-VN")}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Category Badge */}
                  <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-700 text-xs font-semibold text-gray-700 dark:text-gray-300">
                    {course.category || "General"}
                  </div>

                  {/* Hover Action */}
                  <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-success-500 to-green-500 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left" />
                </motion.div>
              );
            })}
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <BookOpen className="w-16 h-16 text-gray-300 dark:text-gray-700 mx-auto mb-4" />
            <p className="text-gray-600 dark:text-gray-400 text-lg">
              Không tìm thấy khóa học nào
            </p>
            {searchQuery || selectedCategory ? (
              <button
                onClick={() => {
                  setSearchQuery("");
                  setSelectedCategory(null);
                }}
                className="mt-4 px-6 py-2 bg-success-600 text-white rounded-lg hover:bg-success-700 transition-colors"
              >
                Xóa bộ lọc
              </button>
            ) : null}
          </motion.div>
        )}

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-16 p-8 rounded-2xl bg-gradient-to-br from-success-600 via-success-500 to-green-500 text-white text-center"
        >
          <h2 className="text-3xl font-black mb-4">
            Bạn là giáo viên hoặc chuyên gia?
          </h2>
          <p className="text-lg mb-6 opacity-90">
            Chia sẻ kiến thức của bạn và tạo khóa học môi trường cho cộng đồng
          </p>
          <button className="px-8 py-4 bg-white text-success-700 rounded-xl font-semibold hover:bg-success-50 transition-colors shadow-xl">
            Tạo khóa học mới
          </button>
        </motion.div>
      </div>
    </div>
  );
}

