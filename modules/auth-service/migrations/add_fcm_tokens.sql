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

-- Migration: Add FCM tokens table
-- Date: 2025-12-09

-- Create fcm_tokens table
CREATE TABLE IF NOT EXISTS fcm_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    token VARCHAR(512) NOT NULL UNIQUE,
    device_type VARCHAR(20) NOT NULL DEFAULT 'ios',
    device_name VARCHAR(100),
    device_id VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT true,
    notification_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_fcm_tokens_user_id ON fcm_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_fcm_tokens_is_active ON fcm_tokens(is_active);

-- Add comment
COMMENT ON TABLE fcm_tokens IS 'FCM tokens for push notifications';
COMMENT ON COLUMN fcm_tokens.device_type IS 'Device platform: ios, android, web';
