-- Education Service Database Tables
-- Schools, Green Courses, Activities, Enrollments

-- Enable PostGIS if not already enabled
CREATE EXTENSION IF NOT EXISTS postgis;

-- Schools table
CREATE TABLE IF NOT EXISTS schools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR NOT NULL,
    code VARCHAR UNIQUE NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    address VARCHAR,
    city VARCHAR,
    district VARCHAR,
    type VARCHAR NOT NULL,
    total_students INTEGER DEFAULT 0,
    total_teachers INTEGER DEFAULT 0,
    green_score FLOAT DEFAULT 0.0,
    total_trees INTEGER DEFAULT 0,
    green_area FLOAT DEFAULT 0.0,
    principal_name VARCHAR,
    phone VARCHAR,
    email VARCHAR,
    website VARCHAR,
    is_public BOOLEAN DEFAULT TRUE,
    data_uri VARCHAR,
    ngsi_ld_uri VARCHAR,
    facilities JSONB,
    meta_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_schools_location ON schools USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_schools_green_score ON schools(green_score DESC);
CREATE INDEX IF NOT EXISTS idx_schools_type ON schools(type);

COMMENT ON TABLE schools IS 'Trường học với green metrics';
COMMENT ON COLUMN schools.green_score IS 'Điểm đánh giá xanh (0-100)';

-- Green courses table
CREATE TABLE IF NOT EXISTS green_courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID REFERENCES schools(id) ON DELETE CASCADE,
    title VARCHAR NOT NULL,
    description TEXT,
    category VARCHAR NOT NULL,
    duration_hours INTEGER,
    max_students INTEGER DEFAULT 30,
    enrolled_students INTEGER DEFAULT 0,
    instructor_name VARCHAR,
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE,
    syllabus JSONB,
    learning_outcomes JSONB,
    status VARCHAR DEFAULT 'draft',
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_courses_school ON green_courses(school_id);
CREATE INDEX IF NOT EXISTS idx_courses_status ON green_courses(status);

-- Green activities table
CREATE TABLE IF NOT EXISTS green_activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID REFERENCES schools(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    description TEXT,
    activity_type VARCHAR NOT NULL,
    activity_date TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_hours FLOAT,
    participants_count INTEGER DEFAULT 0,
    trees_planted INTEGER DEFAULT 0,
    waste_collected_kg FLOAT DEFAULT 0,
    energy_saved_kwh FLOAT DEFAULT 0,
    impact_points INTEGER DEFAULT 0,
    location GEOGRAPHY(POINT, 4326),
    photos JSONB,
    status VARCHAR DEFAULT 'planned',
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_activities_school ON green_activities(school_id);
CREATE INDEX IF NOT EXISTS idx_activities_date ON green_activities(activity_date);
CREATE INDEX IF NOT EXISTS idx_activities_type ON green_activities(activity_type);

-- Enrollments table
CREATE TABLE IF NOT EXISTS enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES green_courses(id) ON DELETE CASCADE,
    user_id UUID,
    student_name VARCHAR NOT NULL,
    student_email VARCHAR,
    student_phone VARCHAR,
    enrollment_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR DEFAULT 'enrolled',
    completion_date TIMESTAMP WITH TIME ZONE,
    grade VARCHAR,
    certificate_url VARCHAR
);

CREATE INDEX IF NOT EXISTS idx_enrollments_course ON enrollments(course_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_user ON enrollments(user_id);
