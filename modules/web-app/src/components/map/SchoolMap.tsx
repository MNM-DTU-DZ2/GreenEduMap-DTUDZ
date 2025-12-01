"use client";

import { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import SchoolSearch from "@/components/search/SchoolSearch";

interface SchoolProperties {
    id: string;
    name: string;
    address: string;
    type: string;
    green_score: number;
    green_stars: number;
}

export default function SchoolMap() {
    const mapContainer = useRef<HTMLDivElement>(null);
    const map = useRef<mapboxgl.Map | null>(null);
    const [mapLoaded, setMapLoaded] = useState(false);

    useEffect(() => {
        const mapboxToken =
            process.env.NEXT_PUBLIC_MAPBOX_TOKEN ||
            "pk.eyJ1IjoidmlldHZvMzcxIiwiYSI6ImNtZ3ZxazFmbDBndnMyanIxMzN0dHV1eGcifQ.lhk4cDYUEIozqnFfkSebaw";

        if (!mapboxToken) {
            console.error("Mapbox token not found");
            return;
        }

        mapboxgl.accessToken = mapboxToken;

        if (map.current || !mapContainer.current) return;

        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: "mapbox://styles/mapbox/streets-v12",
            center: [108.2022, 16.0544], // Da Nang coordinates
            zoom: 12,
        });

        map.current.on("load", () => {
            setMapLoaded(true);
            fetchSchools();
        });

        map.current.addControl(new mapboxgl.NavigationControl(), "top-right");
        map.current.addControl(
            new mapboxgl.GeolocateControl({
                positionOptions: {
                    enableHighAccuracy: true,
                },
                trackUserLocation: true,
            }),
            "top-right"
        );

        return () => {
            map.current?.remove();
        };
    }, []);

    const fetchSchools = async () => {
        if (!map.current) return;

        try {
            // Use absolute URL for server-side or relative for client-side proxy
            // Assuming API Gateway is accessible at localhost:8000 or via proxy
            // For direct browser access, we might need the full URL if not proxied
            // Using relative path assuming Next.js rewrites or same-domain hosting in prod
            // But for dev with separate ports, we might need full URL.
            // Let's try the direct Gateway URL for now, or relative if configured.
            // Given the context, we'll try the relative path first, assuming proxy setup in next.config.ts
            // If not, we fallback to localhost:8000

            const response = await fetch("http://localhost:8000/api/open-data/schools");
            const data = await response.json();

            if (!map.current.getSource("schools")) {
                map.current.addSource("schools", {
                    type: "geojson",
                    data: data,
                });

                // Add layers
                // 1. Circle layer for points
                map.current.addLayer({
                    id: "schools-circles",
                    type: "circle",
                    source: "schools",
                    paint: {
                        "circle-radius": 8,
                        "circle-color": [
                            "case",
                            [">=", ["get", "green_score"], 70],
                            "#10B981", // Green for high score
                            [">=", ["get", "green_score"], 40],
                            "#F59E0B", // Yellow/Orange for medium
                            "#EF4444", // Red for low
                        ],
                        "circle-stroke-width": 2,
                        "circle-stroke-color": "#ffffff",
                        "circle-opacity": 0.8,
                    },
                });

                // 2. Symbol layer for labels (optional, maybe just on hover)
                map.current.addLayer({
                    id: "schools-labels",
                    type: "symbol",
                    source: "schools",
                    layout: {
                        "text-field": ["get", "name"],
                        "text-variable-anchor": ["top", "bottom", "left", "right"],
                        "text-radial-offset": 0.5,
                        "text-justify": "auto",
                        "text-size": 12,
                    },
                    paint: {
                        "text-color": "#1f2937",
                        "text-halo-color": "#ffffff",
                        "text-halo-width": 1,
                    },
                    minzoom: 14,
                });

                // Interactions
                const popup = new mapboxgl.Popup({
                    closeButton: false,
                    closeOnClick: false,
                });

                map.current.on("mouseenter", "schools-circles", (e) => {
                    if (!map.current) return;
                    map.current.getCanvas().style.cursor = "pointer";

                    if (e.features && e.features[0]) {
                        const coordinates = (e.features[0].geometry as any).coordinates.slice();
                        const props = e.features[0].properties as SchoolProperties;

                        // Ensure popup appears over the copy being pointed to
                        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
                        }

                        const html = `
              <div class="p-2 min-w-[200px]">
                <h3 class="font-bold text-gray-900">${props.name}</h3>
                <p class="text-xs text-gray-500 mb-2">${props.address}</p>
                <div class="flex items-center justify-between mt-2">
                  <span class="text-xs font-semibold px-2 py-1 rounded bg-gray-100">
                    ${props.type}
                  </span>
                  <div class="flex items-center gap-1">
                    <span class="text-sm font-bold ${props.green_score >= 70
                                ? "text-green-600"
                                : props.green_score >= 40
                                    ? "text-yellow-600"
                                    : "text-red-600"
                            }">
                      ${props.green_score}
                    </span>
                    <span class="text-xs text-gray-400">/ 100</span>
                  </div>
                </div>
              </div>
            `;

                        popup.setLngLat(coordinates).setHTML(html).addTo(map.current);
                    }
                });

                map.current.on("mouseleave", "schools-circles", () => {
                    if (!map.current) return;
                    map.current.getCanvas().style.cursor = "";
                    popup.remove();
                });

                // Click to zoom
                map.current.on("click", "schools-circles", (e) => {
                    if (!map.current || !e.features || !e.features[0]) return;
                    const coordinates = (e.features[0].geometry as any).coordinates.slice();
                    map.current.flyTo({
                        center: coordinates,
                        zoom: 15
                    });
                });
            }
        } catch (error) {
            console.error("Error fetching schools:", error);
        }
    };

    const handleSelectSchool = (school: any) => {
        if (!map.current) return;

        const coordinates = school.geometry.coordinates;

        map.current.flyTo({
            center: coordinates,
            zoom: 16,
            essential: true
        });

        // Create popup
        new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false,
        })
            .setLngLat(coordinates)
            .setHTML(`
        <div class="p-2 min-w-[200px]">
          <h3 class="font-bold text-gray-900">${school.properties.name}</h3>
          <p class="text-xs text-gray-500 mb-2">${school.properties.address}</p>
          <div class="flex items-center justify-between mt-2">
            <span class="text-xs font-semibold px-2 py-1 rounded bg-gray-100">
              ${school.properties.type}
            </span>
            <div class="flex items-center gap-1">
              <span class="text-sm font-bold ${school.properties.green_score >= 70
                    ? "text-green-600"
                    : school.properties.green_score >= 40
                        ? "text-yellow-600"
                        : "text-red-600"
                }">
                ${school.properties.green_score}
              </span>
              <span class="text-xs text-gray-400">/ 100</span>
            </div>
          </div>
          <a href="/schools/${school.properties.id}" class="block mt-2 text-xs text-center text-white bg-green-600 py-1 rounded hover:bg-green-700 transition-colors">
            Xem chi tiết
          </a>
        </div>
      `)
            .addTo(map.current);
    };

    return (
        <div className="relative w-full h-full">
            <div ref={mapContainer} className="w-full h-full rounded-lg shadow-lg" />

            {/* Search Bar */}
            <div className="absolute top-5 left-5 z-10 w-full max-w-xs sm:max-w-md">
                <SchoolSearch onSelectSchool={handleSelectSchool} />
            </div>

            {/* Legend */}
            <div className="absolute bottom-5 right-5 bg-white p-4 rounded-lg shadow-md z-10">
                <h4 className="font-bold text-sm mb-2">Green Score</h4>
                <div className="space-y-2">
                    <div className="flex items-center gap-2">
                        <span className="w-3 h-3 rounded-full bg-green-500"></span>
                        <span className="text-xs">High ({">"}70)</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
                        <span className="text-xs">Medium (40-70)</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <span className="w-3 h-3 rounded-full bg-red-500"></span>
                        <span className="text-xs">Low ({"<"}40)</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
