/*
 * GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
 * Copyright (C) 2025 DTU-DZ2 Team
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

"use client";

import { useState } from "react";
import ReviewList from "./ReviewList";
import ReviewForm from "./ReviewForm";

interface SchoolReviewsProps {
    schoolId: string;
    initialReviews: any[];
}

export default function SchoolReviews({ schoolId, initialReviews }: SchoolReviewsProps) {
    const [reviews, setReviews] = useState(initialReviews);

    const handleReviewSubmitted = async () => {
        // Refetch reviews
        try {
            const res = await fetch(`http://localhost:8000/api/v1/schools/${schoolId}/reviews`);
            if (res.ok) {
                const newReviews = await res.json();
                setReviews(newReviews);
            }
        } catch (error) {
            console.error("Failed to refresh reviews:", error);
        }
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Đánh giá từ cộng đồng ({reviews.length})</h2>
                <ReviewList reviews={reviews} />
            </div>
            <div>
                <ReviewForm schoolId={schoolId} onReviewSubmitted={handleReviewSubmitted} />
            </div>
        </div>
    );
}
