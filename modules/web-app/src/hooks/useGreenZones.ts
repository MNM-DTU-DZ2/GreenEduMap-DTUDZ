"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export interface GreenZone {
  id: string;
  name: string;
  code: string;
  latitude: number;
  longitude: number;
  address?: string;
  zone_type?: string; // park, forest, garden, green_space
  area_sqm?: number;
  tree_count: number;
  vegetation_coverage?: number;
  maintained_by?: string;
  phone?: string;
  is_public: boolean;
  facilities?: any; // Can be Dict or List
  created_at: string;
}

export interface GreenResource {
  id: string;
  name: string;
  type: string; // trees, solar_panels, recycling_bins, etc.
  quantity: number;
  available_quantity: number;
  unit: string;
  status: string;
  zone_id?: string;
  is_public: boolean;
  meta_data?: any;
  created_at: string;
}

/**
 * Hook to fetch list of green zones
 */
export function useGreenZones(skip: number = 0, limit: number = 100) {
  return useQuery({
    queryKey: ["green-zones", skip, limit],
    queryFn: async () => {
      const response = await api.get<GreenZone[]>(
        `/api/v1/green-zones?skip=${skip}&limit=${limit}`
      );
      return response;
    },
    staleTime: 1000 * 60 * 10, // 10 minutes
    retry: 1,
  });
}

/**
 * Hook to get a single green zone by ID
 */
export function useGreenZone(id: string) {
  return useQuery({
    queryKey: ["green-zone", id],
    queryFn: async () => {
      const response = await api.get<GreenZone>(`/api/v1/green-zones/${id}`);
      return response;
    },
    enabled: !!id,
    staleTime: 1000 * 60 * 15,
  });
}

/**
 * Hook to fetch list of green resources
 */
export function useGreenResources(skip: number = 0, limit: number = 100) {
  return useQuery({
    queryKey: ["green-resources", skip, limit],
    queryFn: async () => {
      const response = await api.get<GreenResource[]>(
        `/api/v1/green-resources?skip=${skip}&limit=${limit}`
      );
      return response;
    },
    staleTime: 1000 * 60 * 10,
    retry: 1,
  });
}

/**
 * Hook to get resources by zone
 */
export function useResourcesByZone(zoneId: string) {
  return useQuery({
    queryKey: ["resources-by-zone", zoneId],
    queryFn: async () => {
      const response = await api.get<GreenResource[]>(
        `/api/v1/green-resources?zone_id=${zoneId}`
      );
      return response;
    },
    enabled: !!zoneId,
    staleTime: 1000 * 60 * 5,
  });
}

