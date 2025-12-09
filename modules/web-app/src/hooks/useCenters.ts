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

export type AdminCenter = {
  id: number;
  ten_trung_tam: string;
  dia_chi: string;
  vi_do?: number | null;
  kinh_do?: number | null;
  nguoi_quan_ly?: string | null;
  so_lien_he?: string | null;
  nguon_lucs: Array<{
    id: number;
    ten_nguon_luc: string;
    loai: string;
  }>;
  created_at?: string;
};

type CentersResponse = {
  centers: AdminCenter[];
};

type CreateCenterPayload = {
  ten_trung_tam: string;
  dia_chi: string;
  vi_do?: number | null;
  kinh_do?: number | null;
  nguoi_quan_ly?: string;
  so_lien_he?: string;
};

export function useCenters() {
  const { error: showError } = useToast();

  return useQuery<CentersResponse>({
    queryKey: ["centers"],
    queryFn: async () => {
      const res = await fetch(`/api/centers`);
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || "Lỗi khi tải danh sách trung tâm");
      }
      return res.json();
    },
  });
}

export function useCreateCenter() {
  const queryClient = useQueryClient();
  const { success, error: showError } = useToast();

  return useMutation({
    mutationFn: async (data: CreateCenterPayload) => {
      const res = await fetch("/api/centers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || "Lỗi khi tạo trung tâm cứu trợ");
      }
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["centers"] });
      success("✅ Tạo trung tâm cứu trợ thành công!");
    },
    onError: (err: Error) => {
      showError(err.message);
    },
  });
}
