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

import { ApiResponse } from './common';

export type UserRole = 'student' | 'teacher' | 'parent' | 'researcher' | 'admin' | 'verifier';

export interface User {
    id: number;
    username?: string;
    email: string;
    full_name: string;
    phone?: string;
    avatar?: string | null;
    role?: UserRole;
    email_verified?: boolean;
    phone_verified?: boolean;
    ekyc_verified?: boolean;
    points?: number; // Environmental points
    carbon_saved?: number; // Total CO2 saved
    badge_level?: number;
    badge_level_text?: string;
    created_at: string;
    updated_at?: string;
}

export interface LoginResponse {
    user: User;
    access_token: string;
    refresh_token: string;
    token_type: string;
}

export interface LoginRequest {
    email: string;
    password: string;
    remember?: boolean;
}

export interface RegisterRequest {
    username: string;
    email: string;
    password: string;
    password_confirmation?: string;
    full_name: string;
    phone: string;
    role?: UserRole;
}

export interface UpdateProfileRequest {
    full_name?: string;
    phone?: string;
    avatar?: string; // base64 image or URL
}

export interface ChangePasswordRequest {
    old_password: string;
    new_password: string;
    new_password_confirmation: string;
}

export interface ResetPasswordRequest {
    token: string;
    email: string;
    password: string;
    password_confirmation: string;
}

export interface VerifyCodeRequest {
    code: string;
}

export interface UpdateFcmTokenRequest {
    push_token: string;
}

