/**
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
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

/**
 * GreenEduMap Mobile App
 * 
 * Nền tảng di động dành cho công dân, học sinh và nhà quản lý đô thị,
 * giúp quan sát – phân tích – hành động dựa trên dữ liệu môi trường,
 * năng lượng và giáo dục mở (Open Data).
 * 
 * Kết nối dữ liệu từ OpenAQ, OpenWeather, NASA POWER, OpenStreetMap
 * và cung cấp đề xuất "hành động xanh" do AI gợi ý.
 */

import React from 'react';
import { StatusBar, useColorScheme, Platform } from 'react-native';
import { NavigationContainer, Theme } from '@react-navigation/native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import MainNavigator from './src/navigation/MainTabNavigator';
import { AuthProvider } from './src/contexts/AuthContext';
import { theme } from './src/theme/colors';
import './src/i18n'; // Initialize i18n
import { navigationRef } from './src/navigation/NavigationService';
import { AlertProvider } from './src/services/AlertService';
import AlertServiceConnector from './src/component/AlertServiceConnector';

const App = () => {
  const isDarkMode = useColorScheme() === 'dark';

  const navigationTheme: Theme = {
    dark: isDarkMode,
    colors: {
      primary: theme.colors.primary,
      background: theme.colors.background,
      card: theme.colors.white,
      text: theme.colors.text,
      border: theme.colors.border,
      notification: theme.colors.error,
    },
    fonts: {
      regular: {
        fontFamily: Platform.select({
          ios: 'SF Pro Display',
          android: 'Roboto',
        }) as string,
        fontWeight: '400',
      },
      medium: {
        fontFamily: Platform.select({
          ios: 'SF Pro Display',
          android: 'Roboto',
        }) as string,
        fontWeight: '500',
      },
      bold: {
        fontFamily: Platform.select({
          ios: 'SF Pro Display',
          android: 'Roboto',
        }) as string,
        fontWeight: '700',
      },
      heavy: {
        fontFamily: Platform.select({
          ios: 'SF Pro Display',
          android: 'Roboto',
        }) as string,
        fontWeight: '900',
      },
    },
  };

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <AlertProvider>
          <AlertServiceConnector />
          <AuthProvider>
            <StatusBar
              barStyle={isDarkMode ? 'light-content' : 'dark-content'}
              backgroundColor={theme.colors.background}
            />
            <NavigationContainer theme={navigationTheme} ref={navigationRef}>
              <MainNavigator />
            </NavigationContainer>
          </AuthProvider>
        </AlertProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
};

export default App;
