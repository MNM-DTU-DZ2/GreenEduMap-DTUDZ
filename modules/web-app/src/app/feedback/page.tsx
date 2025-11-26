"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";

export default function FeedbackPage() {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    category: "general",
    images: [] as File[],
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const categories = [
    { value: "general", label: "Ý tưởng chung", icon: "💡" },
    { value: "improvement", label: "Cải thiện môi trường", icon: "🌱" },
    { value: "education", label: "Giáo dục", icon: "📚" },
    { value: "technology", label: "Công nghệ", icon: "⚙️" },
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      setFormData(prev => ({ ...prev, images: [...prev.images, ...files] }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setIsSubmitting(false);
    setSubmitSuccess(true);
    setFormData({ title: "", description: "", category: "general", images: [] });
    
    setTimeout(() => setSubmitSuccess(false), 5000);
  };

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
                💬 Gửi ý tưởng xanh
              </h1>
            </div>
            <nav className="hidden md:flex items-center gap-6">
              <Link href="/map" className="text-sm text-gray-600 hover:text-success-600 dark:text-gray-400 dark:hover:text-success-400">
                Bản đồ
              </Link>
              <Link href="/actions" className="text-sm text-gray-600 hover:text-success-600 dark:text-gray-400 dark:hover:text-success-400">
                Hành động xanh
              </Link>
              <Link href="/stats" className="text-sm text-gray-600 hover:text-success-600 dark:text-gray-400 dark:hover:text-success-400">
                Thống kê
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <div className="px-4 py-8 mx-auto max-w-4xl sm:px-6 lg:px-8">
        {/* Intro Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 text-center"
        >
          <h2 className="mb-4 text-3xl font-bold text-gray-900 dark:text-white">
            Chia sẻ ý tưởng xanh của bạn
          </h2>
          <p className="max-w-2xl mx-auto text-gray-600 dark:text-gray-400">
            Gửi ý tưởng, đề xuất hoặc phản hồi của bạn để cùng xây dựng một thành phố xanh và bền vững hơn.
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
                  Gửi thành công!
                </p>
                <p className="text-sm text-success-600 dark:text-success-500">
                  Cảm ơn bạn đã đóng góp ý tưởng xanh. Chúng tôi sẽ xem xét và phản hồi sớm nhất có thể.
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
          className="p-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg"
        >
          {/* Category Selection */}
          <div className="mb-6">
            <label className="block mb-3 text-sm font-semibold text-gray-900 dark:text-white">
              Danh mục
            </label>
            <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
              {categories.map((category) => (
                <motion.button
                  key={category.value}
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, category: category.value }))}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`p-4 rounded-xl border-2 transition-all text-center ${
                    formData.category === category.value
                      ? "border-success-500 bg-success-50 dark:bg-success-500/10"
                      : "border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600"
                  }`}
                >
                  <div className="text-2xl mb-2">{category.icon}</div>
                  <div className="text-sm font-medium text-gray-900 dark:text-white">
                    {category.label}
                  </div>
                </motion.button>
              ))}
            </div>
          </div>

          {/* Title */}
          <div className="mb-6">
            <label htmlFor="title" className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
              Tiêu đề
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent"
              placeholder="Nhập tiêu đề ý tưởng của bạn..."
            />
          </div>

          {/* Description */}
          <div className="mb-6">
            <label htmlFor="description" className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
              Mô tả chi tiết
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              required
              rows={6}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-success-500 focus:border-transparent resize-none"
              placeholder="Mô tả chi tiết ý tưởng, đề xuất hoặc phản hồi của bạn..."
            />
          </div>

          {/* Image Upload */}
          <div className="mb-6">
            <label className="block mb-2 text-sm font-semibold text-gray-900 dark:text-white">
              Hình ảnh đính kèm (tùy chọn)
            </label>
            <div className="mt-2 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl hover:border-success-500 dark:hover:border-success-500 transition-colors">
              <div className="space-y-1 text-center">
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  stroke="currentColor"
                  fill="none"
                  viewBox="0 0 48 48"
                  aria-hidden="true"
                >
                  <path
                    d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                    strokeWidth={2}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                <div className="flex text-sm text-gray-600 dark:text-gray-400">
                  <label
                    htmlFor="file-upload"
                    className="relative cursor-pointer rounded-md font-medium text-success-600 hover:text-success-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-success-500"
                  >
                    <span>Chọn ảnh</span>
                    <input
                      id="file-upload"
                      name="file-upload"
                      type="file"
                      className="sr-only"
                      accept="image/*"
                      multiple
                      onChange={handleImageUpload}
                    />
                  </label>
                  <p className="pl-1">hoặc kéo thả</p>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400">PNG, JPG, GIF lên đến 10MB</p>
              </div>
            </div>
            {formData.images.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {formData.images.map((image, index) => (
                  <div key={index} className="relative">
                    <img
                      src={URL.createObjectURL(image)}
                      alt={`Preview ${index + 1}`}
                      className="w-20 h-20 object-cover rounded-lg"
                    />
                    <button
                      type="button"
                      onClick={() => {
                        setFormData(prev => ({
                          ...prev,
                          images: prev.images.filter((_, i) => i !== index)
                        }));
                      }}
                      className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-xs hover:bg-red-600"
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Submit Button */}
          <motion.button
            type="submit"
            disabled={isSubmitting}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full px-6 py-4 text-base font-semibold text-white transition-all rounded-xl bg-gradient-to-r from-success-500 to-success-600 hover:shadow-lg hover:shadow-success-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Đang gửi...
              </span>
            ) : (
              "Gửi ý tưởng xanh"
            )}
          </motion.button>
        </motion.form>
      </div>
    </div>
  );
}

