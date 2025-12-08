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

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { verifyToken } from "@/lib/jwt";
import { getDashboardUrl, hasRouteAccess, getRedirectUrl } from "@/lib/redirect";

export async function middleware(request: NextRequest) {
  const token = request.cookies.get("token")?.value;
  const { pathname } = request.nextUrl;

  // Public routes that don't need authentication
  const isPublicRoute = pathname === "/" || 
    pathname === "/map" || 
    pathname === "/actions" || 
    pathname === "/feedback" || 
    pathname === "/stats" ||
    pathname.startsWith("/api/auth");

  if (isPublicRoute) {
    return NextResponse.next();
  }

  // Check if token exists and is valid
  if (!token) {
    if (pathname.startsWith("/api/")) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    return NextResponse.redirect(new URL("/", request.url));
  }

  const payload = await verifyToken(token);
  if (!payload) {
    if (pathname.startsWith("/api/")) {
      return NextResponse.json({ error: "Invalid token" }, { status: 401 });
    }
    return NextResponse.redirect(new URL("/", request.url));
  }

  // Role-based access control
  const userRole = payload.vai_tro as string;
  console.log("Middleware - User role:", userRole);
  console.log("Middleware - Current pathname:", pathname);

  // Check if user has access to the current route
  const hasAccess = hasRouteAccess(userRole, pathname);
  console.log("Middleware - Has access:", hasAccess);
  
  if (!hasAccess) {
    const redirectUrl = getRedirectUrl(userRole);
    console.log("Middleware - Redirecting to:", redirectUrl);
    return NextResponse.redirect(
      new URL(redirectUrl, request.url)
    );
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/api/:path*",
    "/admin/:path*",
    "/school/:path*",
    "/map/:path*",
    "/actions/:path*",
    "/feedback/:path*",
    "/stats/:path*",
    "/chat/:path*",
    "/recommendations/:path*",
  ],
};

