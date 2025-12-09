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

import React from 'react';
import { 
  StyleSheet, 
  TouchableOpacity, 
  ActivityIndicator,
  TouchableOpacityProps,
} from 'react-native';
import { ThemedText } from './ThemedText';
import Animated, { 
  useAnimatedStyle, 
  withSpring 
} from 'react-native-reanimated';
import { theme } from '../theme/colors';

interface AuthButtonProps extends TouchableOpacityProps {
  title: string;
  loading?: boolean;
  variant?: 'primary' | 'secondary';
}

const AnimatedTouchable = Animated.createAnimatedComponent(TouchableOpacity);

export function AuthButton({ 
  title, 
  loading, 
  variant = 'primary',
  style,
  disabled,
  ...props 
}: AuthButtonProps) {
  const buttonStyle = useAnimatedStyle(() => {
    return {
      transform: [
        { scale: withSpring(disabled ? 0.98 : 1) }
      ],
      opacity: withSpring(disabled ? 0.7 : 1),
    };
  });

  return (
    <AnimatedTouchable
      style={[
        styles.button,
        variant === 'secondary' && styles.buttonSecondary,
        buttonStyle,
        style,
      ]}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <ActivityIndicator 
          color={variant === 'primary' ? '#FFF' : theme.colors.primary} 
          size="small" 
        />
      ) : (
        <ThemedText 
          style={[
            styles.text,
            variant === 'secondary' && styles.textSecondary,
          ]}
        >
          {title}
        </ThemedText>
      )}
    </AnimatedTouchable>
  );
}

const styles = StyleSheet.create({
  button: {
    height: 56,
    borderRadius: 28,
    backgroundColor: theme.colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: theme.colors.primary,
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  buttonSecondary: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: theme.colors.primary,
  },
  text: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: '600',
  },
  textSecondary: {
    color: theme.colors.primary,
  },
});
