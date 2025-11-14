"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";

export default function SchoolProfilePage() {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    schoolName: "Trường Tiểu học Xanh",
    address: "123 Đường ABC, Quận 1, TP.HCM",
    phone: "0123456789",
    email: "contact@school.edu.vn",
    description: "Trường học cam kết giáo dục môi trường và phát triển bền vững",
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSave = () => {
    // Simulate API call
    setIsEditing(false);
  };

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
                👤 Hồ sơ trường học
              </h1>
            </div>
          </div>
        </div>
      </header>

      <div className="px-4 py-8 mx-auto max-w-4xl sm:px-6 lg:px-8">
        {/* Profile Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg"
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Thông tin trường học
            </h2>
            {!isEditing ? (
              <button
                onClick={() => setIsEditing(true)}
                className="px-4 py-2 text-sm font-semibold text-white rounded-lg bg-gradient-to-r from-success-500 to-success-600 hover:shadow-lg"
              >
                ✏️ Chỉnh sửa
              </button>
            ) : (
              <div className="flex gap-2">
                <button
                  onClick={handleSave}
                  className="px-4 py-2 text-sm font-semibold text-white rounded-lg bg-gradient-to-r from-success-500 to-success-600 hover:shadow-lg"
                >
                  💾 Lưu
                </button>
                <button
                  onClick={() => setIsEditing(false)}
                  className="px-4 py-2 text-sm font-semibold text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600"
                >
                  Hủy
                </button>
              </div>
            )}
          </div>

          {/* Profile Form */}
          <div className="space-y-6">
            {/* School Name */}
            <div>
              <label className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
                Tên trường *
              </label>
              {isEditing ? (
                <input
                  type="text"
                  name="schoolName"
                  value={formData.schoolName}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent"
                />
              ) : (
                <p className="px-4 py-3 bg-gray-50 dark:bg-gray-700 rounded-xl text-gray-900 dark:text-white">
                  {formData.schoolName}
                </p>
              )}
            </div>

            {/* Address */}
            <div>
              <label className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
                Địa chỉ *
              </label>
              {isEditing ? (
                <input
                  type="text"
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent"
                />
              ) : (
                <p className="px-4 py-3 bg-gray-50 dark:bg-gray-700 rounded-xl text-gray-900 dark:text-white">
                  {formData.address}
                </p>
              )}
            </div>

            {/* Phone */}
            <div>
              <label className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
                Số điện thoại *
              </label>
              {isEditing ? (
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent"
                />
              ) : (
                <p className="px-4 py-3 bg-gray-50 dark:bg-gray-700 rounded-xl text-gray-900 dark:text-white">
                  {formData.phone}
                </p>
              )}
            </div>

            {/* Email */}
            <div>
              <label className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
                Email *
              </label>
              {isEditing ? (
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent"
                />
              ) : (
                <p className="px-4 py-3 bg-gray-50 dark:bg-gray-700 rounded-xl text-gray-900 dark:text-white">
                  {formData.email}
                </p>
              )}
            </div>

            {/* Description */}
            <div>
              <label className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
                Mô tả
              </label>
              {isEditing ? (
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent resize-none"
                />
              ) : (
                <p className="px-4 py-3 bg-gray-50 dark:bg-gray-700 rounded-xl text-gray-900 dark:text-white">
                  {formData.description}
                </p>
              )}
            </div>
          </div>
        </motion.div>

        {/* Statistics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-3"
        >
          {[
            { label: "Tổng khóa học", value: "12", icon: "📚" },
            { label: "Tổng học viên", value: "1,248", icon: "👥" },
            { label: "Tỷ lệ hoàn thành", value: "87%", icon: "✅" },
          ].map((stat, index) => (
            <div
              key={stat.label}
              className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg"
            >
              <div className="text-3xl mb-2">{stat.icon}</div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                {stat.value}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                {stat.label}
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </div>
  );
}

