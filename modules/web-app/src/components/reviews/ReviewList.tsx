"use client";

import { Star, User } from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import { vi } from "date-fns/locale";

interface Review {
    id: string;
    user_name: string;
    rating: number;
    comment: string;
    created_at: string;
}

interface ReviewListProps {
    reviews: Review[];
}

export default function ReviewList({ reviews }: ReviewListProps) {
    if (!reviews || reviews.length === 0) {
        return (
            <div className="text-center py-8 text-gray-500 bg-gray-50 rounded-xl border border-dashed border-gray-200">
                <p>Chưa có đánh giá nào. Hãy là người đầu tiên!</p>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {reviews.map((review) => (
                <div key={review.id} className="bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
                    <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-600">
                                <User className="w-4 h-4" />
                            </div>
                            <div>
                                <h4 className="font-bold text-sm text-gray-900">{review.user_name}</h4>
                                <span className="text-xs text-gray-500">
                                    {formatDistanceToNow(new Date(review.created_at), { addSuffix: true, locale: vi })}
                                </span>
                            </div>
                        </div>
                        <div className="flex">
                            {[...Array(5)].map((_, i) => (
                                <Star
                                    key={i}
                                    className={`w-4 h-4 ${i < review.rating ? "text-yellow-400 fill-yellow-400" : "text-gray-200"}`}
                                />
                            ))}
                        </div>
                    </div>
                    <p className="text-gray-700 text-sm">{review.comment}</p>
                </div>
            ))}
        </div>
    );
}
