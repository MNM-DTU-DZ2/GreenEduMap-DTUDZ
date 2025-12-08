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

import { useQuery } from "@tanstack/react-query";
import { useToast } from "@/context/ToastContext";

export type AIPrediction = {
  id: number;
  tinh_thanh: string;
  loai_thien_tai: string;
  du_doan_nhu_cau_thuc_pham: number;
  du_doan_nhu_cau_nuoc: number;
  du_doan_nhu_cau_thuoc: number;
  du_doan_nhu_cau_cho_o: number;
  ngay_du_bao: string;
  created_at?: string;
};

type PredictionsResponse = {
  predictions: AIPrediction[];
};

export function useAIPredictions(tinhThanh?: string, generate?: boolean) {
  const { error: showError } = useToast();
  const params = new URLSearchParams();
  if (tinhThanh) params.append("tinh_thanh", tinhThanh);
  if (generate) params.append("generate", "true");

  return useQuery<PredictionsResponse>({
    queryKey: ["ai-predictions", tinhThanh, generate],
    queryFn: async () => {
      const res = await fetch(`/api/ai?${params.toString()}`);
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || "Lỗi khi tải dự báo AI");
      }
      return res.json();
    },
  });
}
