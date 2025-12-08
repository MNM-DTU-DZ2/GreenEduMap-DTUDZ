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
 * Mock Blockchain utility
 * Generates random transaction hashes for transparency logs
 */

export function generateTxHash(): string {
  const chars = "0123456789abcdef";
  let hash = "0x";
  for (let i = 0; i < 64; i++) {
    hash += chars[Math.floor(Math.random() * chars.length)];
  }
  return hash;
}

export function validateTxHash(hash: string): boolean {
  return /^0x[a-f0-9]{64}$/.test(hash);
}

export interface BlockchainLog {
  txHash: string;
  action: string;
  timestamp: Date;
  data: Record<string, unknown>;
}

export function createBlockchainLog(
  action: string,
  data: Record<string, unknown>,
): BlockchainLog {
  return {
    txHash: generateTxHash(),
    action,
    timestamp: new Date(),
    data,
  };
}

