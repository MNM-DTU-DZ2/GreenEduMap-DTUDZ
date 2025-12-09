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

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export interface AirQualityData {
  id: number;
  ward_name: string;
  district?: string;
  city: string;
  latitude?: number;
  longitude?: number;
  aqi: number;
  pm25?: number;
  pm10?: number;
  no2?: number;
  o3?: number;
  so2?: number;
  co?: number;
  measurement_date: string;
  created_at: string;
  updated_at: string;
}

export interface AirQualityAlert {
  location: string;
  aqi_level: string;
  aqi_value: number;
  main_pollutant: string;
  recommendation: string;
}

export function useAirQuality(skip: number = 0, limit: number = 10) {
  return useQuery({
    queryKey: ["air-quality", skip, limit],
    queryFn: async () => {
      const response = await api.get<{
        total: number;
        skip: number;
        limit: number;
        data: AirQualityData[];
      }>(`/api/v1/air-quality?skip=${skip}&limit=${limit}`);
      return response;
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
    retry: 1,
  });
}

export function useAirQualityLatest(limit: number = 100) {
  return useQuery({
    queryKey: ["air-quality-latest", limit],
    queryFn: async () => {
      const response = await api.get<{
        total: number;
        data: AirQualityData[];
      }>(`/api/v1/air-quality/latest?limit=${limit}`);
      return response;
    },
    staleTime: 1000 * 60 * 2, // 2 minutes
    retry: 1,
  });
}

export function useWeather(skip: number = 0, limit: number = 10) {
  return useQuery({
    queryKey: ["weather", skip, limit],
    queryFn: async () => {
      const response = await api.get<{
        total: number;
        skip: number;
        limit: number;
        data: any[];
      }>(`/api/v1/weather?skip=${skip}&limit=${limit}`);
      return response;
    },
    staleTime: 1000 * 60 * 10, // 10 minutes
    retry: 1,
  });
}
