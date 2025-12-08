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

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export interface AITask {
  task_id: string;
  task_type: string;
  status: "queued" | "processing" | "completed" | "failed";
  created_at: string;
}

export interface ClusteringResult {
  zone: "green" | "yellow" | "red";
  cluster_id: number;
  zone_avg_aqi: number;
  green_score: number;
}

export interface PredictionResult {
  date: string;
  predicted_aqi: number;
  confidence: "high" | "medium" | "low";
  category: string;
}

export interface CorrelationResult {
  correlations: {
    [key: string]: {
      correlation: number;
      p_value: number;
      significant: boolean;
      interpretation: string;
    };
  };
  insights: string[];
  summary: {
    avg_aqi: number;
    avg_green_score: number;
    aqi_range: [number, number];
    green_score_range: [number, number];
  };
}

/**
 * Hook to trigger AI clustering analysis
 */
export function useClusteringTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (nClusters: number = 3) => {
      const response = await api.post<AITask>(
        `/api/v1/tasks/ai/clustering?n_clusters=${nClusters}`
      );
      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ai-tasks"] });
    },
  });
}

/**
 * Hook to trigger AI prediction (7-day forecast)
 */
export function usePredictionTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (params?: { location_id?: string; prediction_type?: string }) => {
      const queryString = new URLSearchParams(params as any).toString();
      const response = await api.post<AITask>(
        `/api/v1/tasks/ai/prediction${queryString ? `?${queryString}` : ""}`
      );
      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ai-tasks"] });
    },
  });
}

/**
 * Hook to trigger AI correlation analysis
 */
export function useCorrelationTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (analysisType: "pearson" | "spearman" = "pearson") => {
      const response = await api.post<AITask>(
        `/api/v1/tasks/ai/correlation?analysis_type=${analysisType}`
      );
      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ai-tasks"] });
    },
  });
}

