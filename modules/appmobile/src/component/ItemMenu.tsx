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

import { DrawerItem } from "@react-navigation/drawer"
import Icon from 'react-native-vector-icons/Entypo';
import SCREEN_NAME from "../share"
import { theme } from "../theme/colors";
import { StyleSheet } from "react-native";


type ItemMenuProps = {
    navigation: any,
    label: string,
    name_icon: string,
    screen_name: string,
    focused: string,
    onPress?: () => void
}

const ItemMenu = ({navigation, label, name_icon, screen_name, focused, onPress}: ItemMenuProps) => {
    return (
        <DrawerItem
            label={label}
            icon={() => <Icon name={name_icon} style={{color: focused === screen_name ? theme.colors.white : theme.colors.black}} size={24} />}
            onPress={onPress || (() => navigation.navigate(screen_name))}
            focused={focused === screen_name}
            activeBackgroundColor={theme.colors.primary}
            activeTintColor={theme.colors.white}
            style={styles.menuItem}
        />
    )
}

const styles = StyleSheet.create({
    menuItem: {
        marginHorizontal: 0,
        marginVertical: 0,
        padding: 0,
        borderRadius: 8,
    }
})
export default ItemMenu;
