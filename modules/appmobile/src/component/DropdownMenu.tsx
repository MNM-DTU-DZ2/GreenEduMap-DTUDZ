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
import { View, StyleSheet } from 'react-native';
import { DrawerItem } from "@react-navigation/drawer";
import Icon from 'react-native-vector-icons/Entypo';
import { theme } from "../theme/colors";

type SubMenuItem = {
    label: string;
    name_icon: string;
    screen_name: string;
}

type DropdownMenuProps = {
    navigation: any;
    label: string;
    name_icon: string;
    focused: string;
    subItems: SubMenuItem[];
}

const DropdownMenu = ({ navigation, label, name_icon, focused, subItems }: DropdownMenuProps) => {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <View>
            <DrawerItem
                label={label}
                icon={() => (
                    <View style={styles.iconContainer}>
                        <Icon 
                            name={name_icon} 
                            style={{
                                color: subItems.some(item => item.screen_name === focused) 
                                    ? theme.colors.white 
                                    : theme.colors.black
                            }} 
                            size={24} 
                        />
                        <Icon 
                            name={isExpanded ? "chevron-down" : "chevron-right"} 
                            style={{
                                color: subItems.some(item => item.screen_name === focused) 
                                    ? theme.colors.white 
                                    : theme.colors.black
                            }} 
                            size={24} 
                        />
                    </View>
                )}
                onPress={() => setIsExpanded(!isExpanded)}
                focused={subItems.some(item => item.screen_name === focused)}
                activeBackgroundColor={theme.colors.primary}
                activeTintColor={theme.colors.white}
                style={styles.menuItem}
            />
            
            {isExpanded && (
                <View style={styles.subItemsContainer}>
                    {subItems.map((item, index) => (
                        <DrawerItem
                            key={index}
                            label={item.label}
                            icon={() => (
                                <Icon 
                                    name={item.name_icon} 
                                    style={{
                                        color: focused === item.screen_name 
                                            ? theme.colors.primary 
                                            : theme.colors.black
                                    }} 
                                    size={20} 
                                />
                            )}
                            onPress={() => navigation.navigate(item.screen_name)}
                            focused={focused === item.screen_name}
                            activeBackgroundColor={theme.colors.white}
                            activeTintColor={theme.colors.primary}
                            style={styles.subItem}
                        />
                    ))}
                </View>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    iconContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        width: 60,
        justifyContent: 'space-between'
    },
    subItemsContainer: {
        marginLeft: 10
    },
    subItem: {
        marginHorizontal: 0,
        marginVertical: 0,
        padding: 0,
        borderRadius: 8,
    },
    menuItem: {
        marginHorizontal: 0,
        marginVertical: 0,
        padding: 0,
        borderRadius: 8,
    }
});

export default DropdownMenu; 