"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";

export default function SchoolNewCoursePage() {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    duration: "",
    objectives: "",
    requirements: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setIsSubmitting(false);
    setSubmitSuccess(true);
    setFormData({ title: "", description: "", duration: "", objectives: "", requirements: "" });
    
    setTimeout(() => setSubmitSuccess(false), 5000);
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
                ➕ Tạo khóa học mới
              </h1>
            </div>
          </div>
        </div>
      </header>

      <div className="px-4 py-8 mx-auto max-w-4xl sm:px-6 lg:px-8">
        {/* Intro Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h2 className="mb-4 text-3xl font-bold text-gray-900 dark:text-white">
            Tạo khóa học môi trường mới
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Tạo khóa học mới để chia sẻ kiến thức về môi trường và phát triển bền vững
          </p>
        </motion.div>

        {/* Success Message */}
        {submitSuccess && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-4 mb-6 bg-success-50 dark:bg-success-500/10 border border-success-200 dark:border-success-800 rounded-xl"
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl">✅</span>
              <div>
                <p className="font-semibold text-success-700 dark:text-success-400">
                  Tạo khóa học thành công!
                </p>
                <p className="text-sm text-success-600 dark:text-success-500">
                  Khóa học của bạn đã được tạo và sẽ được duyệt trong thời gian sớm nhất.
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Form */}
        <motion.form
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          onSubmit={handleSubmit}
          className="p-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg space-y-6"
        >
          {/* Title */}
          <div>
            <label htmlFor="title" className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
              Tên khóa học *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent"
              placeholder="Ví dụ: Bảo vệ môi trường sống"
            />
          </div>

          {/* Description */}
          <div>
            <label htmlFor="description" className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
              Mô tả khóa học *
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              required
              rows={4}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent resize-none"
              placeholder="Mô tả chi tiết về khóa học..."
            />
          </div>

          {/* Duration */}
          <div>
            <label htmlFor="duration" className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
              Thời lượng *
            </label>
            <input
              type="text"
              id="duration"
              name="duration"
              value={formData.duration}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent"
              placeholder="Ví dụ: 8 tuần, 12 tuần"
            />
          </div>

          {/* Objectives */}
          <div>
            <label htmlFor="objectives" className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
              Mục tiêu khóa học *
            </label>
            <textarea
              id="objectives"
              name="objectives"
              value={formData.objectives}
              onChange={handleInputChange}
              required
              rows={4}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent resize-none"
              placeholder="Liệt kê các mục tiêu học viên sẽ đạt được..."
            />
          </div>

          {/* Requirements */}
          <div>
            <label htmlFor="requirements" className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
              Yêu cầu đầu vào
            </label>
            <textarea
              id="requirements"
              name="requirements"
              value={formData.requirements}
              onChange={handleInputChange}
              rows={3}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent resize-none"
              placeholder="Yêu cầu kiến thức, trình độ của học viên..."
            />
          </div>

          {/* Submit Button */}
          <div className="flex gap-4 pt-4">
            <motion.button
              type="submit"
              disabled={isSubmitting}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex-1 px-6 py-4 text-base font-semibold text-white transition-all rounded-xl bg-gradient-to-r from-success-500 to-success-600 hover:shadow-lg hover:shadow-success-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Đang tạo...
                </span>
              ) : (
                "Tạo khóa học"
              )}
            </motion.button>
            <Link
              href="/school/courses"
              className="px-6 py-4 text-base font-semibold text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
            >
              Hủy
            </Link>
          </div>
        </motion.form>
      </div>
    </div>
  );
}

