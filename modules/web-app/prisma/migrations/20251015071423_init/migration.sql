--
-- GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
-- Copyright (C) 2025 DTU-DZ2 Team
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program. If not, see <https://www.gnu.org/licenses/>.
--

/*
  Warnings:

  - You are about to drop the `du_bao_ais` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `nguoi_dungs` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `nguon_lucs` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `nhat_ky_blockchains` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `phan_phois` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `trung_tam_cuu_tros` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `yeu_cau_cuu_tros` table. If the table is not empty, all the data it contains will be lost.

*/
-- CreateEnum
CREATE TYPE "UserRole" AS ENUM ('ADMIN', 'USER', 'VOLUNTEER', 'CITIZEN');

-- DropForeignKey
ALTER TABLE "nguon_lucs" DROP CONSTRAINT "nguon_lucs_id_trung_tam_fkey";

-- DropForeignKey
ALTER TABLE "nhat_ky_blockchains" DROP CONSTRAINT "nhat_ky_blockchains_id_phan_phoi_fkey";

-- DropForeignKey
ALTER TABLE "phan_phois" DROP CONSTRAINT "phan_phois_id_nguon_luc_fkey";

-- DropForeignKey
ALTER TABLE "phan_phois" DROP CONSTRAINT "phan_phois_id_tinh_nguyen_vien_fkey";

-- DropForeignKey
ALTER TABLE "phan_phois" DROP CONSTRAINT "phan_phois_id_yeu_cau_fkey";

-- DropForeignKey
ALTER TABLE "yeu_cau_cuu_tros" DROP CONSTRAINT "yeu_cau_cuu_tros_id_nguoi_dung_fkey";

-- DropTable
DROP TABLE "du_bao_ais";

-- DropTable
DROP TABLE "nguoi_dungs";

-- DropTable
DROP TABLE "nguon_lucs";

-- DropTable
DROP TABLE "nhat_ky_blockchains";

-- DropTable
DROP TABLE "phan_phois";

-- DropTable
DROP TABLE "trung_tam_cuu_tros";

-- DropTable
DROP TABLE "yeu_cau_cuu_tros";

-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "firstName" TEXT NOT NULL,
    "lastName" TEXT NOT NULL,
    "role" "UserRole" NOT NULL DEFAULT 'USER',
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");
