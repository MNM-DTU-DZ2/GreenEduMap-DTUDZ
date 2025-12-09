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

import { StyleSheet, Text, TextInput, View } from "react-native";
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';

type TextAreaCustomProps = {
    title: string;
    placeholder?: string;
    value?: string;
    onChangeText?: (text: string) => void;
    onBlur?: () => void;
    type?: 'default' | 'number';
}

const TextAreaCustom = ({ title, placeholder, value, onChangeText, onBlur, type = 'default' }: TextAreaCustomProps) => {
    return (
        <View style={styles.formContainer}>
            {title && <Text style={styles.titleInput}>{title}</Text>}
            <TextInput
                style={styles.textarea}
                multiline={true}
                numberOfLines={6}
                placeholder={placeholder}
                value={value}
                onChangeText={onChangeText}
                textAlignVertical="top"
                placeholderTextColor="#999"
                keyboardType={type === 'number' ? 'numeric' : 'default'}
            />
        </View>
    )
}

const styles = StyleSheet.create({
    textarea: {
        width: '100%',
        height: hp('20%'),
        backgroundColor: '#F5F5F5',
        borderRadius: 8,
        color: '#333',
        borderWidth: 1,
        borderColor: '#E0E0E0',
        padding: hp('1.5%'),
        marginTop: hp('1%'),
        fontSize: hp('1.8%'),
    },
    formContainer: {
        marginTop: hp('2%'),
    },
    titleInput: {
        fontSize: hp('1.8%'),
        fontWeight: 'bold',
        color: '#666',
        marginBottom: hp('0.5%'),
    },
})

export default TextAreaCustom;