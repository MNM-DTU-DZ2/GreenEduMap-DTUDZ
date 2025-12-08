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

/**
 * Utility functions for translating status values to Vietnamese
 */

type BadgeColor = "error" | "warning" | "info" | "success" | "light";

/**
 * Translate priority level to Vietnamese
 */
export function translatePriority(priority: string): string {
  const translations: Record<string, string> = {
    cao: "Cao",
    trung_binh: "Trung bình",
    thap: "Thấp",
    high: "Cao",
    medium: "Trung bình",
    low: "Thấp",
  };
  return translations[priority] || priority;
}

/**
 * Translate request status to Vietnamese
 */
export function translateRequestStatus(status: string): string {
  const translations: Record<string, string> = {
    cho_xu_ly: "Chờ xử lý",
    dang_xu_ly: "Đang xử lý",
    hoan_thanh: "Hoàn thành",
    huy_bo: "Đã hủy bỏ",
  };
  return translations[status] || status;
}

/**
 * Translate distribution status to Vietnamese
 */
export function translateDistributionStatus(status: string): string {
  const translations: Record<string, string> = {
    dang_chuan_bi: "Đang chuẩn bị",
    dang_van_chuyen: "Đang vận chuyển",
    dang_giao: "Đang giao",
    hoan_thanh: "Hoàn thành",
    huy_bo: "Đã hủy bỏ",
  };
  return translations[status] || status;
}

/**
 * Get color for priority badge
 */
export function getPriorityColor(priority: string): BadgeColor {
  if (priority === "cao" || priority === "high") return "error";
  if (priority === "trung_binh" || priority === "medium") return "warning";
  return "info";
}

/**
 * Get color for request status badge
 */
export function getRequestStatusColor(status: string): BadgeColor {
  if (status === "hoan_thanh") return "success";
  if (status === "dang_xu_ly") return "warning";
  if (status === "huy_bo") return "error";
  return "info";
}

/**
 * Get color for distribution status badge
 */
export function getDistributionStatusColor(status: string): BadgeColor {
  if (status === "hoan_thanh") return "success";
  if (status === "dang_giao") return "warning";
  if (status === "dang_van_chuyen") return "info";
  if (status === "huy_bo") return "error";
  return "light";
}


