'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { User, Mail, Calendar, Shield, LogOut } from 'lucide-react';
import { useEffect, useState } from 'react';

interface Review {
    id: string;
    school_id: string;
    rating: number;
    comment: string;
    created_at: string;
}

export default function ProfilePage() {
    const { user, logout, isLoading } = useAuth();
    const router = useRouter();
    const [reviews, setReviews] = useState<Review[]>([]);
    const [loadingReviews, setLoadingReviews] = useState(true);

    useEffect(() => {
        if (!isLoading && !user) {
            router.push('/auth/login');
        }
    }, [user, isLoading, router]);

    useEffect(() => {
        // TODO: Fetch user's reviews from API
        // For now, we'll set empty array
        setLoadingReviews(false);
    }, [user]);

    if (isLoading || !user) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                {/* Header */}
                <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <div className="h-20 w-20 rounded-full bg-green-100 flex items-center justify-center">
                                <User className="h-10 w-10 text-green-600" />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-gray-900">{user.full_name || user.username}</h1>
                                <p className="text-gray-600">@{user.username}</p>
                            </div>
                        </div>
                        <button
                            onClick={logout}
                            className="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                        >
                            <LogOut className="h-4 w-4" />
                            <span>Đăng xuất</span>
                        </button>
                    </div>
                </div>

                {/* User Info */}
                <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">Thông tin tài khoản</h2>
                    <div className="space-y-3">
                        <div className="flex items-center space-x-3 text-gray-700">
                            <Mail className="h-5 w-5 text-gray-400" />
                            <span>{user.email}</span>
                        </div>
                        <div className="flex items-center space-x-3 text-gray-700">
                            <Shield className="h-5 w-5 text-gray-400" />
                            <span className="capitalize">{user.role}</span>
                        </div>
                        <div className="flex items-center space-x-3 text-gray-700">
                            <Calendar className="h-5 w-5 text-gray-400" />
                            <span>Tham gia: {new Date(user.created_at).toLocaleDateString('vi-VN')}</span>
                        </div>
                        <div className="flex items-center space-x-3">
                            <div className={`h-3 w-3 rounded-full ${user.is_active ? 'bg-green-500' : 'bg-red-500'}`}></div>
                            <span className="text-gray-700">{user.is_active ? 'Tài khoản hoạt động' : 'Tài khoản bị khóa'}</span>
                        </div>
                    </div>
                </div>

                {/* Reviews Section */}
                <div className="bg-white rounded-lg shadow-md p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">Đánh giá của tôi</h2>
                    {loadingReviews ? (
                        <div className="text-center py-8">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mx-auto"></div>
                        </div>
                    ) : reviews.length > 0 ? (
                        <div className="space-y-4">
                            {reviews.map((review) => (
                                <div key={review.id} className="border-b pb-4">
                                    <div className="flex items-center justify-between mb-2">
                                        <div className="flex items-center space-x-2">
                                            {'⭐'.repeat(review.rating)}
                                        </div>
                                        <span className="text-sm text-gray-500">
                                            {new Date(review.created_at).toLocaleDateString('vi-VN')}
                                        </span>
                                    </div>
                                    <p className="text-gray-700">{review.comment}</p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-8">
                            <p className="text-gray-500 mb-4">Bạn chưa có đánh giá nào</p>
                            <Link
                                href="/schools/map"
                                className="inline-block px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                            >
                                Khám phá trường học
                            </Link>
                        </div>
                    )}
                </div>

                {/* Back to Map */}
                <div className="mt-6 text-center">
                    <Link href="/schools/map" className="text-green-600 hover:text-green-700">
                        ← Quay lại bản đồ
                    </Link>
                </div>
            </div>
        </div>
    );
}
