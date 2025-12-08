/**
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

'use client';

import { useEffect, useState, useCallback, useRef } from 'react';

interface AirQualityData {
    id: string;
    station_name: string;
    aqi: number;
    pm25: number;
    pm10: number;
    latitude: number;
    longitude: number;
    measurement_date: string;
}

interface WeatherData {
    id: string;
    city_name: string;
    temperature: number;
    feels_like: number;
    humidity: number;
    pressure: number;
    wind_speed: number;
    latitude: number;
    longitude: number;
    weather_description: string;
    observation_time: string;
}

interface UseRealtimeDataReturn {
    aqiData: AirQualityData[];
    weatherData: WeatherData[];
    isConnected: boolean;
    error: string | null;
    reconnect: () => void;
}

/**
 * Hook to connect to real-time WebSocket data streams
 * Automatically handles reconnection and works in both local and production
 */
export function useRealtimeData(): UseRealtimeDataReturn {
    const [aqiData, setAqiData] = useState<AirQualityData[]>([]);
    const [weatherData, setWeatherData] = useState<WeatherData[]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const wsAqiRef = useRef<WebSocket | null>(null);
    const wsWeatherRef = useRef<WebSocket | null>(null);
    const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
    const reconnectAttemptsRef = useRef(0);

    // Get WebSocket URL based on environment
    const getWebSocketUrl = useCallback((endpoint: string) => {
        // Check if we're in browser
        if (typeof window === 'undefined') return '';

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.hostname;

        // Local development
        if (host === 'localhost' || host === '127.0.0.1') {
            return `ws://localhost:8007${endpoint}`;
        }

        // Production VPS
        // Assuming environment-service is exposed on same domain with /ws prefix
        return `${protocol}//${host}/ws${endpoint}`;
    }, []);

    const connectWebSockets = useCallback(() => {
        try {
            // Close existing connections
            if (wsAqiRef.current) wsAqiRef.current.close();
            if (wsWeatherRef.current) wsWeatherRef.current.close();

            const aqiUrl = getWebSocketUrl('/air-quality');
            const weatherUrl = getWebSocketUrl('/weather');

            console.log('🔌 Connecting to WebSocket:', { aqiUrl, weatherUrl });

            // Air Quality WebSocket
            const wsAqi = new WebSocket(aqiUrl);

            wsAqi.onopen = () => {
                console.log('✅ AQI WebSocket connected');
                setIsConnected(true);
                setError(null);
                reconnectAttemptsRef.current = 0;
            };

            wsAqi.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log('📊 Received AQI data:', data.length, 'points');
                    setAqiData(data);
                } catch (err) {
                    console.error('Error parsing AQI data:', err);
                }
            };

            wsAqi.onerror = (event) => {
                console.error('❌ AQI WebSocket error:', event);
                setError('Failed to connect to AQI stream');
            };

            wsAqi.onclose = () => {
                console.log('🔌 AQI WebSocket closed');
                setIsConnected(false);

                // Attempt reconnection with exponential backoff
                if (reconnectAttemptsRef.current < 5) {
                    const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000);
                    console.log(`🔄 Reconnecting in ${delay}ms...`);

                    reconnectTimeoutRef.current = setTimeout(() => {
                        reconnectAttemptsRef.current++;
                        connectWebSockets();
                    }, delay);
                }
            };

            // Weather WebSocket
            const wsWeather = new WebSocket(weatherUrl);

            wsWeather.onopen = () => {
                console.log('✅ Weather WebSocket connected');
            };

            wsWeather.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log('🌤️ Received weather data:', data.length, 'points');
                    setWeatherData(data);
                } catch (err) {
                    console.error('Error parsing weather data:', err);
                }
            };

            wsWeather.onerror = (event) => {
                console.error('❌ Weather WebSocket error:', event);
            };

            wsWeather.onclose = () => {
                console.log('🔌 Weather WebSocket closed');
            };

            wsAqiRef.current = wsAqi;
            wsWeatherRef.current = wsWeather;

        } catch (err) {
            console.error('Error creating WebSocket:', err);
            setError('Failed to create WebSocket connection');
        }
    }, [getWebSocketUrl]);

    const reconnect = useCallback(() => {
        reconnectAttemptsRef.current = 0;
        connectWebSockets();
    }, [connectWebSockets]);

    useEffect(() => {
        connectWebSockets();

        return () => {
            // Cleanup
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
            }
            if (wsAqiRef.current) {
                wsAqiRef.current.close();
            }
            if (wsWeatherRef.current) {
                wsWeatherRef.current.close();
            }
        };
    }, [connectWebSockets]);

    return {
        aqiData,
        weatherData,
        isConnected,
        error,
        reconnect
    };
}
