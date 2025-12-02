'use client';

import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { User, LogIn } from 'lucide-react';

export default function Navbar() {
    const { user, isAuthenticated, logout } = useAuth();

    return (
        <nav className="bg-white shadow-md">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    {/* Logo & Nav Links */}
                    <div className="flex items-center space-x-8">
                        <Link href="/" className="flex items-center space-x-2">
                            <span className="text-2xl font-bold text-green-600">🌱 GreenEduMap</span>
                        </Link>

                        <div className="hidden md:flex items-center space-x-4">
                            <Link
                                href="/schools/map"
                                className="text-gray-700 hover:text-green-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                            >
                                Bản đồ trường học
                            </Link>
                        </div>
                    </div>

                    {/* Auth Section */}
                    <div className="flex items-center space-x-4">
                        {isAuthenticated && user ? (
                            <div className="flex items-center space-x-3">
                                <Link
                                    href="/profile"
                                    className="flex items-center space-x-2 text-gray-700 hover:text-green-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    <User className="h-4 w-4" />
                                    <span className="hidden sm:inline">{user.username}</span>
                                </Link>
                                <button
                                    onClick={logout}
                                    className="text-gray-700 hover:text-red-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    Đăng xuất
                                </button>
                            </div>
                        ) : (
                            <div className="flex items-center space-x-2">
                                <Link
                                    href="/auth/login"
                                    className="flex items-center space-x-1 text-gray-700 hover:text-green-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    <LogIn className="h-4 w-4" />
                                    <span>Đăng nhập</span>
                                </Link>
                                <Link
                                    href="/auth/register"
                                    className="bg-green-600 text-white hover:bg-green-700 px-4 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    Đăng ký
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
}
