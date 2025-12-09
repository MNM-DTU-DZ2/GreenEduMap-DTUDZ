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

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useToast } from "@/context/ToastContext";

type ResourceFilters = {
  loai?: string;
  id_trung_tam?: number;
};

export type AdminResource = {
  id: number;
  ten_nguon_luc: string;
  loai: string;
  so_luong: number;
  don_vi: string;
  id_trung_tam: number;
  trung_tam?: {
    id: number;
    ten_trung_tam: string;
    dia_chi: string;
    vi_do?: number | null;
    kinh_do?: number | null;
  } | null;
  created_at?: string;
};

type ResourcesResponse = {
  resources: AdminResource[];
};

type CreateResourcePayload = {
  ten_nguon_luc: string;
  loai: string;
  so_luong: number;
  don_vi: string;
  id_trung_tam: number;
};

export function useResources(filters?: ResourceFilters) {
  const { error: showError } = useToast();
  const params = new URLSearchParams();
  if (filters?.loai) params.append("loai", filters.loai);
  if (filters?.id_trung_tam) params.append("id_trung_tam", filters.id_trung_tam.toString());

  return useQuery<ResourcesResponse>({
    queryKey: ["resources", filters],
    queryFn: async () => {
      const res = await fetch(`/api/resources?${params.toString()}`);
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || "Lỗi khi lấy danh sách nguồn lực");
      }
      return res.json();
    },
  });
}

export function useCreateResource() {
  const queryClient = useQueryClient();
  const { success, error: showError } = useToast();

  return useMutation({
    mutationFn: async (data: CreateResourcePayload) => {
      const res = await fetch("/api/resources", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || "Lỗi khi tạo nguồn lực");
      }
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resources"] });
      success("✅ Tạo nguồn lực thành công!");
    },
    onError: (err: Error) => {
      showError(err.message);
    },
  });
}
