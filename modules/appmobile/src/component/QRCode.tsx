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
  TouchableOpacity,
  Share,
  Platform,
  PermissionsAndroid,
} from 'react-native';
import QRCodeSVG from 'react-native-qrcode-svg';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { theme } from '../theme/colors';

interface QRCodeProps {
  value: string;
  size?: number;
  quietZone?: number;
  label?: string;
  error?: string;
  showShare?: boolean;
  showDownload?: boolean;
  onDownload?: () => void;
}

const QRCode: React.FC<QRCodeProps> = ({
  value,
  size = 200,
  quietZone = 0,
  label,
  error,
  showShare = true,
  showDownload = true,
  onDownload,
}) => {
  let qrRef: any = null;

  const handleShare = async () => {
    try {
      await Share.share({
        message: value,
      });
    } catch (error) {
      console.error('Error sharing QR code:', error);
    }
  };

  const handleDownload = async () => {
    if (Platform.OS === 'android') {
      try {
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE,
          {
            title: 'Storage Permission',
            message: 'AgriCred needs access to your storage to save QR codes.',
            buttonNeutral: 'Ask Me Later',
            buttonNegative: 'Cancel',
            buttonPositive: 'OK',
          },
        );
        if (granted !== PermissionsAndroid.RESULTS.GRANTED) {
          console.error('Storage permission denied');
          return;
        }
      } catch (err) {
        console.error('Error requesting storage permission:', err);
        return;
      }
    }

    onDownload?.();
  };

  return (
    <View style={styles.container}>
      {label && <Text style={styles.label}>{label}</Text>}
      <View style={styles.qrContainer}>
        <QRCodeSVG
          value={value}
          size={size}
          color={theme.colors.text}
          backgroundColor={theme.colors.white}
          quietZone={quietZone}
          getRef={c => (qrRef = c)}
        />
      </View>
      {/* <View style={styles.actions}>
        {showShare && (
          <TouchableOpacity style={styles.actionButton} onPress={handleShare}>
            <Icon name="share-variant" size={24} color={theme.colors.primary} />
            <Text style={styles.actionText}>Share</Text>
          </TouchableOpacity>
        )}
        {showDownload && (
          <TouchableOpacity style={styles.actionButton} onPress={handleDownload}>
            <Icon name="download" size={24} color={theme.colors.primary} />
            <Text style={styles.actionText}>Download</Text>
          </TouchableOpacity>
        )}
      </View> */}
      {error && <Text style={styles.errorText}>{error}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginBottom: theme.spacing.md,
  },
  label: {
    fontFamily: theme.typography.fontFamily as string,
    fontWeight: '500',
    fontSize: theme.typography.fontSize.sm,
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  qrContainer: {
    padding: theme.spacing.md,
    backgroundColor: theme.colors.white,
    borderRadius: theme.borderRadius.md,
    ...theme.shadows.md,
  },
  actions: {
    flexDirection: 'row',
    marginTop: theme.spacing.md,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: theme.spacing.sm,
    marginHorizontal: theme.spacing.sm,
  },
  actionText: {
    marginLeft: theme.spacing.xs,
    fontFamily: theme.typography.fontFamily as string,
    fontWeight: '500',
    fontSize: theme.typography.fontSize.sm,
    color: theme.colors.primary,
  },
  errorText: {
    fontFamily: theme.typography.fontFamily as string,
    fontWeight: '400',
    fontSize: theme.typography.fontSize.sm,
    color: theme.colors.error,
    marginTop: theme.spacing.xs,
  },
});

export default QRCode; 