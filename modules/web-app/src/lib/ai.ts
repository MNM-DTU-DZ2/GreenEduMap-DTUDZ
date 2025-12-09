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
 * Mock AI Forecasting utility
 * Generates random disaster predictions for each province
 */

export interface AIPrediction {
  tinh_thanh: string;
  loai_thien_tai: string;
  du_doan_nhu_cau_thuc_pham: number;
  du_doan_nhu_cau_nuoc: number;
  du_doan_nhu_cau_thuoc: number;
  du_doan_nhu_cau_cho_o: number;
  ngay_du_bao: Date;
}

const PROVINCES = [
  "Hà Nội",
  "Hồ Chí Minh",
  "Đà Nẵng",
  "Hải Phòng",
  "Cần Thơ",
  "Quảng Ninh",
  "Thừa Thiên Huế",
  "Nghệ An",
  "Thanh Hóa",
  "Bình Định",
];

const DISASTER_TYPES = [
  "Lũ lụt",
  "Bão",
  "Hạn hán",
  "Sạt lở đất",
  "Động đất",
  "Cháy rừng",
];

export function generateMockPrediction(province?: string): AIPrediction {
  const selectedProvince =
    province || PROVINCES[Math.floor(Math.random() * PROVINCES.length)];

  return {
    tinh_thanh: selectedProvince,
    loai_thien_tai:
      DISASTER_TYPES[Math.floor(Math.random() * DISASTER_TYPES.length)],
    du_doan_nhu_cau_thuc_pham: Math.floor(Math.random() * 5000) + 1000,
    du_doan_nhu_cau_nuoc: Math.floor(Math.random() * 10000) + 2000,
    du_doan_nhu_cau_thuoc: Math.floor(Math.random() * 2000) + 500,
    du_doan_nhu_cau_cho_o: Math.floor(Math.random() * 1000) + 200,
    ngay_du_bao: new Date(Date.now() + Math.random() * 7 * 24 * 60 * 60 * 1000),
  };
}

export function generateMultiplePredictions(count: number): AIPrediction[] {
  return Array.from({ length: count }, () => generateMockPrediction());
}

