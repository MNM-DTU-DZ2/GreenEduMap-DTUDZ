import { notFound } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, MapPin, Award, BookOpen, Leaf } from "lucide-react";

async function getSchool(id: string) {
    try {
        // Use internal docker network URL for server-side fetch
        const res = await fetch(`http://api-gateway:8000/api/v1/schools/${id}`, {
            cache: "no-store",
        });

        if (!res.ok) {
            if (res.status === 404) return null;
            throw new Error(`Failed to fetch school: ${res.status}`);
        }

        return res.json();
    } catch (error) {
        console.error("Error fetching school:", error);
        return null;
    }
}

export default async function SchoolDetailsPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    const school = await getSchool(id);

    if (!school) {
        notFound();
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                {/* Back Button */}
                <Link
                    href="/schools/map"
                    className="inline-flex items-center text-sm text-gray-500 hover:text-green-600 mb-6 transition-colors"
                >
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Quay lại bản đồ
                </Link>

                {/* Header Section */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
                    <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900 mb-2">{school.name}</h1>
                            <div className="flex items-center text-gray-500">
                                <MapPin className="w-4 h-4 mr-2" />
                                <span>{school.address}</span>
                            </div>
                            <div className="mt-2 inline-flex items-center px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-sm font-medium">
                                {school.type}
                            </div>
                        </div>

                        <div className="flex flex-col items-center p-4 bg-green-50 rounded-xl border border-green-100 min-w-[120px]">
                            <span className="text-sm text-green-600 font-medium mb-1">Green Score</span>
                            <span className="text-4xl font-bold text-green-700">{school.green_score}</span>
                            <div className="flex mt-1">
                                {[...Array(5)].map((_, i) => (
                                    <Leaf
                                        key={i}
                                        className={`w-4 h-4 ${i < school.green_stars ? "text-green-500 fill-green-500" : "text-gray-300"}`}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Content Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Facilities Section */}
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                        <div className="flex items-center mb-4">
                            <Award className="w-5 h-5 text-green-600 mr-2" />
                            <h2 className="text-xl font-bold text-gray-900">Cơ sở vật chất xanh</h2>
                        </div>

                        {school.facilities && school.facilities.items && school.facilities.items.length > 0 ? (
                            <ul className="space-y-3">
                                {school.facilities.items.map((item: string, index: number) => (
                                    <li key={index} className="flex items-start">
                                        <span className="w-2 h-2 mt-2 rounded-full bg-green-500 mr-3 shrink-0" />
                                        <span className="text-gray-700 capitalize">{item}</span>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className="text-gray-500 italic">Chưa có thông tin về cơ sở vật chất.</p>
                        )}
                    </div>

                    {/* Green Courses Section */}
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                        <div className="flex items-center mb-4">
                            <BookOpen className="w-5 h-5 text-blue-600 mr-2" />
                            <h2 className="text-xl font-bold text-gray-900">Khóa học xanh</h2>
                        </div>

                        {school.green_courses && school.green_courses.length > 0 ? (
                            <div className="space-y-4">
                                {school.green_courses.map((course: any) => (
                                    <div key={course.id} className="p-4 rounded-xl bg-gray-50 border border-gray-100 hover:border-blue-200 transition-colors">
                                        <h3 className="font-bold text-gray-900 mb-1">{course.name}</h3>
                                        <p className="text-sm text-gray-600 line-clamp-2">{course.description}</p>
                                        <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
                                            <span>{course.duration}</span>
                                            <span className="px-2 py-1 rounded bg-white border border-gray-200">
                                                {course.level}
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-gray-500 italic">Chưa có khóa học xanh nào.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
