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
import React from "react";
import { ApexOptions } from "apexcharts";
import dynamic from "next/dynamic";

const ReactApexChart = dynamic(() => import("react-apexcharts"), {
  ssr: false,
});

interface ResourceTypeChartProps {
  data: {
    categories: string[];
    data: number[];
  };
}

export default function ResourceTypeChart({ data }: ResourceTypeChartProps) {
  const options: ApexOptions = {
    colors: [
      "#3B82F6", "#8B5CF6", "#F59E0B", "#10B981", "#EF4444",
      "#06B6D4", "#84CC16", "#F97316", "#EC4899", "#6366F1"
    ],
    chart: {
      fontFamily: "Outfit, sans-serif",
      type: "donut",
      height: 300,
    },
    plotOptions: {
      pie: {
        donut: {
          size: "70%",
          labels: {
            show: true,
            name: {
              show: true,
              fontSize: "14px",
              fontWeight: 600,
              color: "#6B7280",
            },
            value: {
              show: true,
              fontSize: "16px",
              fontWeight: 700,
              color: "#1F2937",
              formatter: (val: string) => `${val}`,
            },
            total: {
              show: true,
              showAlways: true,
              label: "Tổng nguồn lực",
              fontSize: "14px",
              fontWeight: 600,
              color: "#6B7280",
              formatter: () => {
                const total = data.data.reduce((sum, val) => sum + val, 0);
                return `${total}`;
              },
            },
          },
        },
      },
    },
    dataLabels: {
      enabled: true,
      formatter: (val: number) => `${val.toFixed(1)}%`,
      style: {
        fontSize: "12px",
        fontWeight: "bold",
        colors: ["#fff"],
      },
    },
    legend: {
      show: true,
      position: "bottom",
      horizontalAlign: "center",
      fontSize: "12px",
      labels: {
        colors: "#6B7280",
      },
      markers: {
        size: 8,
      },
    },
    tooltip: {
      y: {
        formatter: (val: number) => `${val} nguồn lực`,
      },
    },
    responsive: [
      {
        breakpoint: 768,
        options: {
          chart: {
            height: 250,
          },
          legend: {
            position: "bottom",
          },
        },
      },
    ],
  };

  const series = data.data;

  return (
    <div className="w-full">
      <ReactApexChart
        options={options}
        series={series}
        type="donut"
        height={300}
      />
    </div>
  );
}
