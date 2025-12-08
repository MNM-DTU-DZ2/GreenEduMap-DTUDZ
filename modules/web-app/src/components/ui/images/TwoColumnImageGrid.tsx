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

import Image from "next/image";
import React from "react";

export default function TwoColumnImageGrid() {
  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
      <div>
        <Image
          src="/images/grid-image/image-02.png"
          alt=" grid"
          className="w-full border border-gray-200 rounded-xl dark:border-gray-800"
          width={517}
          height={295}
        />
      </div>

      <div>
        <Image
          src="/images/grid-image/image-03.png"
          alt=" grid"
          className="w-full border border-gray-200 rounded-xl dark:border-gray-800"
          width={517}
          height={295}
        />
      </div>
    </div>
  );
}
