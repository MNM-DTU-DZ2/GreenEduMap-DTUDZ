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
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  Modal,
  Platform,
} from 'react-native';
import LottieView from 'lottie-react-native';
import { theme } from '../theme/colors';

interface LoadingOverlayProps {
  visible: boolean;
  message?: string;
  useLottie?: boolean;
  lottieSize?: number;
  loop?: boolean;
  autoPlay?: boolean;
}

const LoadingOverlay: React.FC<LoadingOverlayProps> = ({
  visible,
  message = 'Loading...',
  useLottie = true,
  lottieSize = 120,
  loop = true,
  autoPlay = true,
}) => {
  const [lottieError, setLottieError] = React.useState(false);

  if (!visible) return null;

  // Fallback for platforms where Lottie might not work properly
  const shouldUseLottie = useLottie && Platform.OS !== 'web' && !lottieError;

  const handleLottieError = () => {
    console.warn('Lottie animation failed to load, falling back to ActivityIndicator');
    setLottieError(true);
  };

  return (
    <Modal transparent visible={visible}>
      <View style={styles.container}>
        <View style={styles.content}>
          {shouldUseLottie ? (
            <LottieView
              source={require('../assets/animations/coin_wallet.json')}
              autoPlay={autoPlay}
              loop={loop}
              style={{ 
                width: lottieSize, 
                height: lottieSize,
                backgroundColor: 'transparent'
              }}
              resizeMode="contain"
              hardwareAccelerationAndroid={true}
              onAnimationFailure={handleLottieError}
            />
          ) : (
            <ActivityIndicator size="large" color={theme.colors.primary} />
          )}
          {message && <Text style={styles.message}>{message}</Text>}
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.overlay,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    backgroundColor: theme.colors.white,
    padding: theme.spacing.lg,
    borderRadius: theme.borderRadius.md, 
    alignItems: 'center',
    ...theme.shadows.lg,
  },
  message: {
    marginTop: theme.spacing.md,
    fontFamily: theme.typography.fontFamily,
    fontSize: theme.typography.fontSize.md,
    color: theme.colors.text,
  },
});

export default LoadingOverlay; 