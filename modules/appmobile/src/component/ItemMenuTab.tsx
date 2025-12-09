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

import { Image, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { heightPercentageToDP as hp, widthPercentageToDP as wp } from 'react-native-responsive-screen';

type ItemMenuTabProps = {
    image: any;
    text: string;
    onPress: () => void;
}

const ItemMenuTab = ({ image, text, onPress }: ItemMenuTabProps) => {
    return (
        <TouchableOpacity style={styles.item} onPress={onPress}>
            <Image source={image} style={styles.icon} />
                <Text 
                style={styles.text}
                numberOfLines={2}
                adjustsFontSizeToFit
            >
                {text}
                </Text>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    item: {
        backgroundColor: 'white',
        borderRadius: hp('1%'),
        margin: hp('1%'),
        paddingHorizontal: hp('1%'),
        height: hp('16%'),
        width: wp('26.2%'),
        alignItems: 'center',
        justifyContent: 'center',
        shadowColor: '#000',
        shadowOffset: {width: 0, height: 6},
        shadowOpacity: 0.15,
        shadowRadius: 10,
        elevation: 10,
    },
    icon: {
        width: hp('9%'),
        height: hp('9%'),
        resizeMode: 'contain',
    },
    text: {
        fontSize: hp('1.7%'),
        fontWeight: 'bold',
        textAlign: 'center',
        marginTop: hp('0.8%'),
        flexWrap: 'wrap',
        width: '100%',
    },
});

export default ItemMenuTab;
