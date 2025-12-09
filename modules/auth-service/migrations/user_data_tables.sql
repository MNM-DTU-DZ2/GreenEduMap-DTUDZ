--
-- GreenEduMap-DTUDZ - User-Specific Data Tables
-- Copyright (C) 2025 DTU-DZ2 Team
--
-- Creates tables for user favorites, contributions, and activities
--

-- ============================================
-- USER FAVORITES
-- Địa điểm yêu thích của user
-- ============================================
CREATE TABLE IF NOT EXISTS user_favorites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    target_type VARCHAR(50) NOT NULL, -- 'school', 'green_zone', 'recycling_center'
    target_id UUID NOT NULL,
    note TEXT,
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_favorites_user_id ON user_favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_user_favorites_target ON user_favorites(target_type, target_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_user_favorites_unique ON user_favorites(user_id, target_type, target_id);

COMMENT ON TABLE user_favorites IS 'User favorite locations (schools, green zones, recycling centers)';
COMMENT ON COLUMN user_favorites.target_type IS 'Type: school, green_zone, recycling_center';
COMMENT ON COLUMN user_favorites.is_public IS 'Whether this favorite is visible to others';

-- ============================================
-- USER CONTRIBUTIONS
-- Đóng góp dữ liệu từ user
-- ============================================
CREATE TABLE IF NOT EXISTS user_contributions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- 'aqi_report', 'green_spot', 'issue', 'feedback'
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location GEOGRAPHY(POINT, 4326),
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    address TEXT,
    status VARCHAR(20) DEFAULT 'pending', -- pending, approved, rejected
    is_public BOOLEAN DEFAULT true,
    data JSONB, -- Additional data (photos, measurements, etc.)
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_contributions_user_id ON user_contributions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_contributions_type ON user_contributions(type);
CREATE INDEX IF NOT EXISTS idx_user_contributions_status ON user_contributions(status);
CREATE INDEX IF NOT EXISTS idx_user_contributions_location ON user_contributions USING GIST(location);

COMMENT ON TABLE user_contributions IS 'User-contributed data: AQI reports, green spots, issues';
COMMENT ON COLUMN user_contributions.type IS 'Type: aqi_report, green_spot, issue, feedback';
COMMENT ON COLUMN user_contributions.status IS 'Status: pending, approved, rejected';

-- ============================================
-- USER ACTIVITIES
-- Lịch sử hoạt động của user
-- ============================================
CREATE TABLE IF NOT EXISTS user_activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL, -- 'login', 'view', 'create', 'update', 'delete', 'share'
    target_type VARCHAR(50), -- 'school', 'green_zone', 'contribution', etc.
    target_id UUID,
    description TEXT,
    metadata JSONB, -- Additional context
    ip_address INET,
    user_agent TEXT,
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX IF NOT EXISTS idx_user_activities_action ON user_activities(action);
CREATE INDEX IF NOT EXISTS idx_user_activities_created_at ON user_activities(created_at DESC);

COMMENT ON TABLE user_activities IS 'User activity log for tracking actions';
COMMENT ON COLUMN user_activities.action IS 'Action: login, view, create, update, delete, share';

-- ============================================
-- USER SETTINGS
-- Cài đặt cá nhân của user
-- ============================================
CREATE TABLE IF NOT EXISTS user_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    notification_enabled BOOLEAN DEFAULT true,
    email_notifications BOOLEAN DEFAULT true,
    push_notifications BOOLEAN DEFAULT true,
    language VARCHAR(10) DEFAULT 'vi',
    theme VARCHAR(20) DEFAULT 'light',
    default_city VARCHAR(100) DEFAULT 'TP. Hồ Chí Minh',
    default_latitude DECIMAL(10,7) DEFAULT 10.7769,
    default_longitude DECIMAL(10,7) DEFAULT 106.7009,
    privacy_level VARCHAR(20) DEFAULT 'public', -- public, friends, private
    data JSONB, -- Additional settings
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_settings_user_id ON user_settings(user_id);

COMMENT ON TABLE user_settings IS 'User personal settings and preferences';

-- Success message
SELECT 'User data tables created successfully' as message;
