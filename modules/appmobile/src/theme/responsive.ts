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

import {
  widthPercentageToDP as wp,
  heightPercentageToDP as hp,
} from 'react-native-responsive-screen';

export const responsive = {
  wp,
  hp,
};

// Font sizes
export const FONT_SIZE = {
  xs: wp('3%'),
  sm: wp('3.5%'),
  md: wp('4%'),
  lg: wp('4.5%'),
  xl: wp('5%'),
  '2xl': wp('6%'),
  '3xl': wp('7.5%'),
  '4xl': wp('9%'),
  xxl: wp('6%'),
};

// Spacing
export const SPACING = {
  xs: wp('2%'),
  sm: wp('3%'),
  md: wp('4%'),
  lg: wp('5%'),
  xl: wp('6%'),
  '2xl': wp('10%'),
  xxl: wp('8%'),
};

// Border radius
export const BORDER_RADIUS = {
  xs: wp('1%'),
  sm: wp('2%'),
  md: wp('3%'),
  lg: wp('4%'),
  xl: wp('5%'),
  '2xl': wp('8%'),
  full: wp('50%'),
}; 