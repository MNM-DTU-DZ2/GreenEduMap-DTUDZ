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

export function useBlockchainLogs(id_phan_phoi?: number) {
  const params = new URLSearchParams();
  if (id_phan_phoi) params.append("id_phan_phoi", id_phan_phoi.toString());

  return useQuery({
    queryKey: ["blockchain-logs", id_phan_phoi],
    queryFn: async () => {
      const res = await fetch(`/api/blockchain?${params.toString()}`);
      if (!res.ok) throw new Error("Failed to fetch blockchain logs");
      return res.json();
    },
  });
}

