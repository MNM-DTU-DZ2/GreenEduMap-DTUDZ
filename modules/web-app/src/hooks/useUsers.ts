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

export type AdminUser = {
  id: number;
  ho_va_ten: string;
  email: string;
  so_dien_thoai?: string | null;
  vai_tro: string;
  created_at: string;
};

type UsersResponse = {
  users: AdminUser[];
};

export function useUsers(role?: string) {
  const { error: showError } = useToast();
  const params = new URLSearchParams();
  if (role) params.append("vai_tro", role);

  return useQuery<UsersResponse>({
    queryKey: ["users", role],
    queryFn: async () => {
      const res = await fetch(`/api/users?${params.toString()}`);
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || "Lỗi khi tải danh sách người dùng");
      }
      return res.json();
    },
  });
}
