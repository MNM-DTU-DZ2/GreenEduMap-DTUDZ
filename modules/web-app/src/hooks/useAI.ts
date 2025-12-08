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

export function useAIPredictions(generate: boolean = false) {
  return useQuery({
    queryKey: ["ai-predictions", generate],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (generate) params.append("generate", "true");
      
      const res = await fetch(`/api/ai?${params.toString()}`);
      if (!res.ok) throw new Error("Failed to fetch predictions");
      return res.json();
    },
  });
}

export function useGeneratePredictions() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      const res = await fetch("/api/ai", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ generate_multiple: true }),
      });
      if (!res.ok) throw new Error("Failed to generate predictions");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ai-predictions"] });
    },
  });
}

