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

interface RadioProps {
  id: string; // Unique ID for the radio button
  name: string; // Group name for the radio button
  value: string; // Value of the radio button
  checked: boolean; // Whether the radio button is checked
  label: string; // Label text for the radio button
  onChange: (value: string) => void; // Handler for when the radio button is toggled
  className?: string; // Optional custom classes for styling
}

const RadioSm: React.FC<RadioProps> = ({
  id,
  name,
  value,
  checked,
  label,
  onChange,
  className = "",
}) => {
  return (
    <label
      htmlFor={id}
      className={`flex cursor-pointer select-none items-center text-sm text-gray-500 dark:text-gray-400 ${className}`}
    >
      <span className="relative">
        {/* Hidden Input */}
        <input
          type="radio"
          id={id}
          name={name}
          value={value}
          checked={checked}
          onChange={() => onChange(value)}
          className="sr-only"
        />
        {/* Styled Radio Circle */}
        <span
          className={`mr-2 flex h-4 w-4 items-center justify-center rounded-full border ${
            checked
              ? "border-brand-500 bg-brand-500"
              : "bg-transparent border-gray-300 dark:border-gray-700"
          }`}
        >
          {/* Inner Dot */}
          <span
            className={`h-1.5 w-1.5 rounded-full ${
              checked ? "bg-white" : "bg-white dark:bg-[#1e2636]"
            }`}
          ></span>
        </span>
      </span>
      {label}
    </label>
  );
};

export default RadioSm;
