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

import React, { useState } from 'react';
import {
    View,
    Text,
    TouchableOpacity,
    StyleSheet,
    ActivityIndicator,
    Platform,
} from 'react-native';
import DocumentPicker, { DocumentPickerResponse } from 'react-native-document-picker';
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import { theme } from '../theme/colors';

interface FileUploaderProps {
    onFileSelected: (fileInfo: DocumentPickerResponse) => void;
    onError: (error: any) => void;
}

const FileUploader: React.FC<FileUploaderProps> = ({ onFileSelected, onError }) => {
    const [selectedFile, setSelectedFile] = useState<DocumentPickerResponse | null>(null);

    const pickDocument = async () => {
        try {
            const result = await DocumentPicker.pick({
                type: [DocumentPicker.types.allFiles],
            });
            
            if (result && result.length > 0) {
                const file = result[0];
                setSelectedFile(file);
                onFileSelected(file);
            }
        } catch (error) {
            if (DocumentPicker.isCancel(error)) {
                // Người dùng đã hủy việc chọn tệp
                console.log('User cancelled document picker');
            } else {
                console.error('Error picking document:', error);
                onError(error);
            }
        }
    };

    return (
        <View style={styles.container}>
            {selectedFile ? (
                <View style={styles.fileInfoContainer}>
                    <Text style={styles.fileName}>{selectedFile.name || 'unknown_file'}</Text>
                    <Text style={styles.fileStatus}>Đã chọn</Text>
                </View>
            ) : null}
            
            <TouchableOpacity 
                style={styles.button} 
                onPress={pickDocument}
            >
                <Text style={styles.buttonText}>
                    {selectedFile ? 'Chọn tệp khác' : 'Chọn tệp'}
                </Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        width: '100%',
        alignItems: 'center',
        padding: wp('4%'),
    },
    button: {
        backgroundColor: theme.colors.primary,
        paddingVertical: hp('1.5%'),
        paddingHorizontal: wp('6%'),
        borderRadius: 8,
        marginTop: hp('2%'),
    },
    buttonText: {
        color: '#fff',
        fontSize: wp('4%'),
        fontWeight: '500',
    },
    fileInfoContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#f0f0f0',
        padding: wp('3%'),
        borderRadius: 8,
        marginBottom: hp('1%'),
        width: '100%',
    },
    fileName: {
        flex: 1,
        fontSize: wp('3.5%'),
        color: '#333',
    },
    fileStatus: {
        fontSize: wp('3%'),
        color: 'green',
    },
});

export default FileUploader;