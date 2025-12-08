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
import { Modal } from "@/components/ui/modal";

type AdminModalSize = "sm" | "md" | "lg" | "xl";

interface AdminModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  size?: AdminModalSize;
  hideCloseButton?: boolean;
  className?: string;
}

const sizeMap: Record<AdminModalSize, string> = {
  sm: "max-w-md",
  md: "max-w-lg",
  lg: "max-w-2xl",
  xl: "max-w-4xl",
};

export default function AdminModal({
  isOpen,
  onClose,
  title,
  description,
  children,
  footer,
  size = "lg",
  hideCloseButton = false,
  className = "",
}: AdminModalProps) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      className={`${sizeMap[size]} ${className}`.trim()}
      showCloseButton={!hideCloseButton}
    >
      <div className="w-full space-y-6 rounded-3xl p-6 sm:p-8">
        <header className="space-y-2">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
            {title}
          </h2>
          {description && (
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {description}
            </p>
          )}
        </header>

        <div className="space-y-6">{children}</div>

        {footer && <footer className="flex flex-col gap-3 sm:flex-row sm:justify-end">{footer}</footer>}
      </div>
    </Modal>
  );
}
