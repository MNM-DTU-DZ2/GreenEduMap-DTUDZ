"use client";

import { useState, useEffect } from "react";
import { Star, Send } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import Link from "next/link";

interface ReviewFormProps {
    schoolId: string;
    onReviewSubmitted: () => void;
}

export default function ReviewForm({ schoolId, onReviewSubmitted }: ReviewFormProps) {
    const { user, isAuthenticated } = useAuth();
    const [rating, setRating] = useState(5);
    const [comment, setComment] = useState("");
    const [userName, setUserName] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState("");

    // Auto-fill username if user is authenticated
    useEffect(() => {
        if (isAuthenticated && user) {
            setUserName(user.full_name || user.username);
        }
    }, [isAuthenticated, user]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError("");

        if (!userName.trim()) {
            setError("Vui lòng nhập tên của bạn");
            setIsSubmitting(false);
            return;
        }

        try {
            // Get access token if user is authenticated
            const token = localStorage.getItem('accessToken');
            const headers: HeadersInit = {
                "Content-Type": "application/json",
            };

            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            // Use client-side fetch to API Gateway (localhost:8000)
            const response = await fetch(`http://localhost:8000/api/v1/schools/${schoolId}/reviews`, {
                method: "POST",
                headers,
                body: JSON.stringify({
                    rating,
                    comment,
                    user_name: userName,
                }),
            });

            if (!response.ok) {
                throw new Error("Failed to submit review");
            }

            // Reset form
            setComment("");
            setUserName("");
            setRating(5);
            onReviewSubmitted();
        } catch (err) {
            console.error(err);
            setError("Có lỗi xảy ra khi gửi đánh giá. Vui lòng thử lại.");
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Viết đánh giá của bạn</h3>

            {error && (
                <div className="mb-4 p-3 bg-red-50 text-red-600 text-sm rounded-lg">
                    {error}
                </div>
            )}

            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Đánh giá</label>
                <div className="flex gap-1">
                    {[1, 2, 3, 4, 5].map((star) => (
                        <button
                            key={star}
                            type="button"
                            onClick={() => setRating(star)}
                            className="focus:outline-none transition-transform hover:scale-110"
                        >
                            <Star
                                className={`w-8 h-8 ${star <= rating ? "text-yellow-400 fill-yellow-400" : "text-gray-200"}`}
                            />
                        </button>
                    ))}
                </div>
            </div>

            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Tên của bạn</label>
                {!isAuthenticated && (
                    <p className="text-sm text-gray-500 mb-2">
                        <Link href="/auth/login" className="text-green-600 hover:text-green-700 underline">
                            Đăng nhập
                        </Link>
                        {' '}để tự động điền thông tin
                    </p>
                )}
                <input
                    type="text"
                    value={userName}
                    onChange={(e) => setUserName(e.target.value)}
                    readOnly={isAuthenticated}
                    className={`w-full px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none ${isAuthenticated ? 'bg-gray-50 cursor-not-allowed' : ''
                        }`}
                    placeholder="Nhập tên hiển thị..."
                    required
                />
            </div>

            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Nhận xét</label>
                <textarea
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    className="w-full px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none min-h-[100px]"
                    placeholder="Chia sẻ trải nghiệm của bạn về trường này..."
                />
            </div>

            <button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-green-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
            >
                {isSubmitting ? (
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                    <>
                        <Send className="w-4 h-4" />
                        Gửi đánh giá
                    </>
                )}
            </button>
        </form>
    );
}
