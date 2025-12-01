"use client";

import { useState, useEffect, useRef } from "react";
import { Search } from "lucide-react";

interface SchoolSearchProps {
    onSelectSchool: (school: any) => void;
}

export default function SchoolSearch({ onSelectSchool }: SchoolSearchProps) {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<any[]>([]);
    const [isOpen, setIsOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const wrapperRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    useEffect(() => {
        const searchSchools = async () => {
            if (query.length < 2) {
                setResults([]);
                return;
            }

            setIsLoading(true);
            try {
                // Fetch all schools and filter client-side for better UX with small dataset
                // In a real large-scale app, we would use a search API endpoint
                const response = await fetch("http://localhost:8000/api/open-data/schools");
                const data = await response.json();

                const filtered = data.features.filter((feature: any) =>
                    feature.properties.name.toLowerCase().includes(query.toLowerCase()) ||
                    feature.properties.address?.toLowerCase().includes(query.toLowerCase())
                );

                setResults(filtered.slice(0, 5)); // Limit to 5 results
                setIsOpen(true);
            } catch (error) {
                console.error("Search error:", error);
            } finally {
                setIsLoading(false);
            }
        };

        const timeoutId = setTimeout(searchSchools, 300);
        return () => clearTimeout(timeoutId);
    }, [query]);

    return (
        <div ref={wrapperRef} className="relative w-full max-w-md">
            <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Tìm kiếm trường học..."
                    className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white shadow-sm"
                    onFocus={() => query.length >= 2 && setIsOpen(true)}
                />
                {isLoading && (
                    <div className="absolute right-3 top-1/2 -translate-y-1/2">
                        <div className="animate-spin h-4 w-4 border-2 border-green-500 border-t-transparent rounded-full"></div>
                    </div>
                )}
            </div>

            {isOpen && results.length > 0 && (
                <div className="absolute w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-100 max-h-60 overflow-auto z-50">
                    {results.map((school) => (
                        <button
                            key={school.properties.id}
                            onClick={() => {
                                onSelectSchool(school);
                                setQuery(school.properties.name);
                                setIsOpen(false);
                            }}
                            className="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors border-b last:border-0 border-gray-50"
                        >
                            <div className="font-medium text-sm text-gray-900">
                                {school.properties.name}
                            </div>
                            <div className="text-xs text-gray-500 truncate">
                                {school.properties.address}
                            </div>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
