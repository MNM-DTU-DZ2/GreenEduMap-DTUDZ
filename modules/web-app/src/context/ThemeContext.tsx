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

import type React from "react";
import { createContext, useState, useContext, useEffect } from "react";

type Theme = "light" | "dark";

type ThemeContextType = {
  theme: Theme;
  toggleTheme: () => void;
};

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [theme, setTheme] = useState<Theme>("light");
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    // This code will only run on the client side
    const savedTheme = localStorage.getItem("theme") as Theme | null;
    const initialTheme = savedTheme || "light"; // Default to light theme

    console.log("Theme initialization:", { savedTheme, initialTheme });

    // Force light theme for auth pages
    const isAuthPage = window.location.pathname.startsWith('/login') || 
                      window.location.pathname.startsWith('/register') ||
                      window.location.pathname.startsWith('/forgot-password');
    
    if (isAuthPage) {
      console.log("Auth page detected, forcing light theme");
      document.documentElement.classList.remove("dark");
      setTheme("light");
    } else {
      // Ensure we start with light theme and remove any existing dark class
      document.documentElement.classList.remove("dark");
      setTheme(initialTheme);
    }
    
    setIsInitialized(true);
  }, []);

  useEffect(() => {
    if (isInitialized) {
      console.log("Theme change:", { theme, isInitialized });
      localStorage.setItem("theme", theme);
      if (theme === "dark") {
        document.documentElement.classList.add("dark");
        console.log("Added dark class");
      } else {
        document.documentElement.classList.remove("dark");
        console.log("Removed dark class");
      }
    }
  }, [theme, isInitialized]);

  const toggleTheme = () => {
    console.log("Toggle theme called, current theme:", theme);
    setTheme((prevTheme) => {
      const newTheme = prevTheme === "light" ? "dark" : "light";
      console.log("Theme toggled from", prevTheme, "to", newTheme);
      return newTheme;
    });
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {isInitialized ? children : (
        <div className="flex items-center justify-center h-screen">
          <div className="text-gray-500">Loading theme...</div>
        </div>
      )}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};
