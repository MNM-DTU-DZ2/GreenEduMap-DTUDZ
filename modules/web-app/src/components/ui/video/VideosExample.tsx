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

import React from "react";
import YouTubeEmbed from "./YouTubeEmbed";
import ComponentCard from "@/components/common/ComponentCard";

export default function VideosExample() {
  return (
    <div>
      <div className="grid grid-cols-1 gap-5 sm:gap-6 xl:grid-cols-2">
        <div className="space-y-5 sm:space-y-6">
          <ComponentCard title="Video Ratio 16:9">
            <YouTubeEmbed videoId="dQw4w9WgXcQ" />
          </ComponentCard>
          <ComponentCard title="Video Ratio 4:3">
            <YouTubeEmbed videoId="dQw4w9WgXcQ" aspectRatio="4:3" />
          </ComponentCard>
        </div>
        <div className="space-y-5 sm:space-y-6">
          <ComponentCard title="Video Ratio 21:9">
            <YouTubeEmbed videoId="dQw4w9WgXcQ" aspectRatio="21:9" />
          </ComponentCard>
          <ComponentCard title="Video Ratio 1:1">
            <YouTubeEmbed videoId="dQw4w9WgXcQ" aspectRatio="1:1" />
          </ComponentCard>
        </div>
      </div>
    </div>
  );
}
