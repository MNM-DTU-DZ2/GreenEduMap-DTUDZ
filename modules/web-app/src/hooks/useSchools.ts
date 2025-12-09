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

export interface School {
  id: string;
  name: string;
  code: string;
  address: string;
  city?: string;
  district?: string;
  latitude?: number;
  longitude?: number;
  green_score?: number;
  total_students?: number;
  total_teachers?: number;
  type?: string; // 'university', 'high_school', 'middle_school', 'primary'
  created_at: string;
  updated_at: string;
}

export interface GreenCourse {
  id: string;
  school_id: string;
  title: string;
  description?: string;
  category?: string; // 'Energy', 'Waste', 'Water', 'Biodiversity'
  duration_weeks?: number;
  start_date?: string;
  end_date?: string;
  instructor_name?: string;
  max_participants?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Hook to fetch list of schools
 */
export function useSchools(skip: number = 0, limit: number = 100) {
  return useQuery({
    queryKey: ["schools", skip, limit],
    queryFn: async () => {
      const response = await api.get<School[]>(
        `/api/v1/schools?skip=${skip}&limit=${limit}`
      );
      return response;
    },
    staleTime: 1000 * 60 * 10, // 10 minutes
    retry: 1,
  });
}

/**
 * Hook to get a single school by ID
 */
export function useSchool(id: string) {
  return useQuery({
    queryKey: ["school", id],
    queryFn: async () => {
      const response = await api.get<School>(`/api/v1/schools/${id}`);
      return response;
    },
    enabled: !!id,
    staleTime: 1000 * 60 * 15, // 15 minutes
  });
}

/**
 * Hook to find schools nearby a location
 */
export function useNearbySchools(
  latitude: number,
  longitude: number,
  radius: number = 5000,
  limit: number = 10
) {
  return useQuery({
    queryKey: ["nearby-schools", latitude, longitude, radius, limit],
    queryFn: async () => {
      const response = await api.get<School[]>(
        `/api/v1/schools/nearby?latitude=${latitude}&longitude=${longitude}&radius=${radius}&limit=${limit}`
      );
      return response;
    },
    enabled: !!latitude && !!longitude,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

/**
 * Hook to get top green schools
 */
export function useTopGreenSchools(limit: number = 10) {
  return useQuery({
    queryKey: ["top-green-schools", limit],
    queryFn: async () => {
      const response = await api.get<School[]>(
        `/api/v1/schools/top-green?limit=${limit}`
      );
      return response;
    },
    staleTime: 1000 * 60 * 30, // 30 minutes
  });
}

/**
 * Hook to fetch list of green courses
 */
export function useGreenCourses(skip: number = 0, limit: number = 100) {
  return useQuery({
    queryKey: ["green-courses", skip, limit],
    queryFn: async () => {
      const response = await api.get<GreenCourse[]>(
        `/api/v1/green-courses?skip=${skip}&limit=${limit}`
      );
      return response;
    },
    staleTime: 1000 * 60 * 10, // 10 minutes
    retry: 1,
  });
}

/**
 * Hook to get a single course by ID
 */
export function useGreenCourse(id: string) {
  return useQuery({
    queryKey: ["green-course", id],
    queryFn: async () => {
      const response = await api.get<GreenCourse>(`/api/v1/green-courses/${id}`);
      return response;
    },
    enabled: !!id,
    staleTime: 1000 * 60 * 15,
  });
}

/**
 * Hook to get courses by category
 */
export function useCoursesByCategory(category: string, limit: number = 50) {
  return useQuery({
    queryKey: ["courses-by-category", category, limit],
    queryFn: async () => {
      const response = await api.get<GreenCourse[]>(
        `/api/v1/green-courses/category/${category}?limit=${limit}`
      );
      return response;
    },
    enabled: !!category,
    staleTime: 1000 * 60 * 10,
  });
}

/**
 * Hook to create a new school (admin only)
 */
export function useCreateSchool() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: Partial<School>) => {
      const response = await api.post("/api/v1/schools", data);
      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["schools"] });
    },
  });
}

/**
 * Hook to update a school
 */
export function useUpdateSchool(id: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: Partial<School>) => {
      const response = await api.put(`/api/v1/schools/${id}`, data);
      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["schools"] });
      queryClient.invalidateQueries({ queryKey: ["school", id] });
    },
  });
}

