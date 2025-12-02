"use client";

import { useState } from "react";
import { CheckCircle, XCircle, Copy, Play } from "lucide-react";

interface TestResult {
    endpoint: string;
    method: string;
    status: number | null;
    response: any;
    error?: string;
}

export default function APITestPage() {
    const [activeTab, setActiveTab] = useState("schools");
    const [results, setResults] = useState<TestResult[]>([]);
    const [loading, setLoading] = useState(false);

    const API_BASE = "http://localhost:8000";

    const testEndpoints = {
        schools: [
            { name: "List Schools", method: "GET", endpoint: "/api/v1/schools", body: null },
            { name: "Get School by ID", method: "GET", endpoint: "/api/v1/schools/:id", body: null, requiresId: true },
            { name: "Nearby Schools", method: "GET", endpoint: "/api/v1/schools/nearby?latitude=16.0544&longitude=108.2022&radius_km=10", body: null },
            { name: "School Rankings", method: "GET", endpoint: "/api/v1/schools/rankings?limit=10", body: null },
        ],
        courses: [
            { name: "List Green Courses", method: "GET", endpoint: "/api/v1/green-courses", body: null },
            { name: "Courses by School", method: "GET", endpoint: "/api/v1/green-courses/by-school/:id", body: null, requiresId: true },
        ],
        reviews: [
            { name: "List Reviews", method: "GET", endpoint: "/api/v1/schools/:id/reviews", body: null, requiresId: true },
            {
                name: "Create Review",
                method: "POST",
                endpoint: "/api/v1/schools/:id/reviews",
                requiresId: true,
                body: {
                    user_name: "Test User",
                    rating: 5,
                    comment: "Great school! Test review."
                }
            },
        ],
        opendata: [
            { name: "Schools GeoJSON", method: "GET", endpoint: "/api/open-data/schools", body: null },
        ]
    };

    const runTest = async (test: any) => {
        setLoading(true);
        const result: TestResult = {
            endpoint: test.endpoint,
            method: test.method,
            status: null,
            response: null
        };

        try {
            let url = API_BASE + test.endpoint;

            // Replace :id with first school ID if needed
            if (test.requiresId) {
                // First fetch a school ID
                const schoolsRes = await fetch(`${API_BASE}/api/v1/schools?limit=1`);
                const schools = await schoolsRes.json();
                if (schools && schools.length > 0) {
                    url = url.replace(":id", schools[0].id);
                } else {
                    throw new Error("No schools found to use for ID");
                }
            }

            const options: RequestInit = {
                method: test.method,
                headers: {
                    "Content-Type": "application/json",
                },
            };

            if (test.body) {
                options.body = JSON.stringify(test.body);
            }

            const response = await fetch(url, options);
            result.status = response.status;

            if (response.ok) {
                result.response = await response.json();
            } else {
                result.error = `${response.status} ${response.statusText}`;
                result.response = await response.text();
            }
        } catch (error: any) {
            result.error = error.message;
        } finally {
            setLoading(false);
            setResults([result, ...results]);
        }
    };

    const runAllTests = async () => {
        setResults([]);
        const currentTests = testEndpoints[activeTab as keyof typeof testEndpoints];
        for (const test of currentTests) {
            await runTest(test);
            // Small delay between tests
            await new Promise(resolve => setTimeout(resolve, 300));
        }
    };

    const copyResponse = (response: any) => {
        navigator.clipboard.writeText(JSON.stringify(response, null, 2));
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8 px-4">
            <div className="max-w-6xl mx-auto">
                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">API Test Dashboard</h1>
                    <p className="text-gray-600">Test GreenEduMap API endpoints (Day 1-7)</p>
                </div>

                {/* Tabs */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 mb-6">
                    <div className="flex border-b border-gray-100">
                        {Object.keys(testEndpoints).map((tab) => (
                            <button
                                key={tab}
                                onClick={() => setActiveTab(tab)}
                                className={`px-6 py-3 font-medium capitalize transition-colors ${activeTab === tab
                                    ? "border-b-2 border-green-600 text-green-600"
                                    : "text-gray-500 hover:text-gray-700"
                                    }`}
                            >
                                {tab}
                            </button>
                        ))}
                    </div>

                    <div className="p-6">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-bold text-gray-900">
                                {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Tests
                            </h2>
                            <button
                                onClick={runAllTests}
                                disabled={loading}
                                className="bg-green-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center gap-2 disabled:opacity-50"
                            >
                                <Play className="w-4 h-4" />
                                Run All Tests
                            </button>
                        </div>

                        <div className="space-y-3">
                            {testEndpoints[activeTab as keyof typeof testEndpoints].map((test, idx) => (
                                <div
                                    key={idx}
                                    className="border border-gray-200 rounded-lg p-4 hover:border-green-300 transition-colors"
                                >
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <h3 className="font-medium text-gray-900">{test.name}</h3>
                                            <p className="text-sm text-gray-500 font-mono mt-1">
                                                <span className={`px-2 py-0.5 rounded text-xs font-semibold mr-2 ${test.method === "GET" ? "bg-blue-100 text-blue-700" : "bg-green-100 text-green-700"
                                                    }`}>
                                                    {test.method}
                                                </span>
                                                {test.endpoint}
                                            </p>
                                        </div>
                                        <button
                                            onClick={() => runTest(test)}
                                            disabled={loading}
                                            className="bg-gray-100 text-gray-700 px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors disabled:opacity-50"
                                        >
                                            Test
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Results */}
                {results.length > 0 && (
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                        <h2 className="text-xl font-bold text-gray-900 mb-4">Test Results</h2>
                        <div className="space-y-4">
                            {results.map((result, idx) => (
                                <div
                                    key={idx}
                                    className={`border rounded-lg p-4 ${result.status && result.status >= 200 && result.status < 300
                                        ? "border-green-200 bg-green-50"
                                        : result.status && result.status >= 400
                                            ? "border-red-200 bg-red-50"
                                            : "border-gray-200"
                                        }`}
                                >
                                    <div className="flex items-center justify-between mb-2">
                                        <div className="flex items-center gap-2">
                                            {result.status && result.status >= 200 && result.status < 300 ? (
                                                <CheckCircle className="w-5 h-5 text-green-600" />
                                            ) : (
                                                <XCircle className="w-5 h-5 text-red-600" />
                                            )}
                                            <span className="font-medium text-gray-900">
                                                {result.method} {result.endpoint}
                                            </span>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <span
                                                className={`px-2 py-1 rounded text-sm font-semibold ${result.status && result.status >= 200 && result.status < 300
                                                    ? "bg-green-100 text-green-700"
                                                    : "bg-red-100 text-red-700"
                                                    }`}
                                            >
                                                {result.status || "Error"}
                                            </span>
                                            <button
                                                onClick={() => copyResponse(result.response)}
                                                className="text-gray-500 hover:text-gray-700"
                                            >
                                                <Copy className="w-4 h-4" />
                                            </button>
                                        </div>
                                    </div>
                                    {result.error && (
                                        <div className="text-sm text-red-600 mb-2">Error: {result.error}</div>
                                    )}
                                    <div className="bg-gray-900 text-green-400 p-3 rounded font-mono text-xs overflow-auto max-h-60">
                                        <pre>{JSON.stringify(result.response, null, 2)}</pre>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
