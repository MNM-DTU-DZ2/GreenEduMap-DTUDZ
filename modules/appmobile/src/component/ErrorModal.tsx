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
  Modal,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import LottieView from 'lottie-react-native';
import { theme } from '../theme/colors';

interface ErrorModalProps {
  visible: boolean;
  onClose: () => void;
  onConfirm?: () => void;
  title?: string;
  message?: string;
  buttonText?: string;
  animationSize?: number;
  showConfirmButton?: boolean;
}

const { width } = Dimensions.get('window');

const ErrorModal: React.FC<ErrorModalProps> = ({
  visible,
  onClose,
  onConfirm,
  title = 'Lỗi',
  message = 'Đã xảy ra lỗi',
  buttonText = 'Xác nhận',
  animationSize = 200,
  showConfirmButton = true,
}) => {
  const handleConfirm = () => {
    if (onConfirm) {
      onConfirm();
    }
    onClose();
  };

  return (
    <Modal
      transparent
      visible={visible}
      animationType="fade"
      onRequestClose={onClose}
    >
      <View style={styles.overlay}>
        <View style={styles.container}>
          <View style={styles.content}>
            {/* Lottie Animation */}
            <LottieView
              source={require('../assets/animations/no_data.json')}
              autoPlay
              loop={false}
              style={{
                width: animationSize,
                height: animationSize,
              }}
              resizeMode="contain"
            />
            
            {/* Title */}
            <Text style={styles.title}>{title}</Text>
            
            {/* Message */}
            <Text style={styles.message}>{message}</Text>
            
            {/* Confirm Button */}
            {showConfirmButton && (
              <TouchableOpacity style={styles.button} onPress={handleConfirm}>
                <Text style={styles.buttonText}>{buttonText}</Text>
              </TouchableOpacity>
            )}
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  container: {
    width: width * 0.85,
    maxWidth: 400,
  },
  content: {
    backgroundColor: theme.colors.white,
    borderRadius: theme.borderRadius.lg,
    padding: theme.spacing.xl,
    alignItems: 'center',
    ...theme.shadows.lg,
  },
  title: {
    fontSize: theme.typography.fontSize.xl,
    fontWeight: 'bold',
    color: '#FF3B30',
    marginTop: theme.spacing.lg,
    marginBottom: theme.spacing.md,
    textAlign: 'center',
    fontFamily: theme.typography.fontFamily,
  },
  message: {
    fontSize: theme.typography.fontSize.md,
    color: theme.colors.textLight,
    textAlign: 'center',
    marginBottom: theme.spacing.xl,
    lineHeight: 22,
    fontFamily: theme.typography.fontFamily,
  },
  button: {
    backgroundColor: '#FF3B30',
    paddingHorizontal: theme.spacing.xl,
    paddingVertical: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    minWidth: 120,
    alignItems: 'center',
  },
  buttonText: {
    color: theme.colors.white,
    fontSize: theme.typography.fontSize.md,
    fontWeight: '600',
    fontFamily: theme.typography.fontFamily,
  },
});

export default ErrorModal;

