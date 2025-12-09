#!/usr/bin/env python3
"""
GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
Copyright (C) 2025 DTU-DZ2 Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

"""
Prediction Model - Dự báo AQI
Sử dụng Linear Regression và Moving Average để dự báo AQI
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class AQIPrediction:
    """Dự báo chất lượng không khí (AQI)"""
    
    def __init__(self, forecast_days: int = 7):
        """
        Initialize prediction model
        
        Args:
            forecast_days: Số ngày dự báo (mặc định 7)
        """
        self.forecast_days = forecast_days
        self.model = LinearRegression()
        self.is_fitted = False
    
    def prepare_time_series(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Chuẩn bị time series data
        
        Args:
            data: List of dict với keys: measured_at, aqi, location_id
        
        Returns:
            DataFrame với time series
        """
        if not data:
            raise ValueError("No data provided for prediction")
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Parse datetime
        df['measured_at'] = pd.to_datetime(df['measured_at'])
        
        # Sort by time
        df = df.sort_values('measured_at')
        
        # Set datetime as index
        df = df.set_index('measured_at')
        
        logger.info(f"Prepared time series with {len(df)} records")
        return df
    
    def create_features(self, df: pd.DataFrame) -> tuple:
        """
        Tạo features cho model
        
        Args:
            df: Time series DataFrame
        
        Returns:
            (X, y) features and target
        """
        # Tạo features: day number, hour, day of week
        df['day_num'] = (df.index - df.index[0]).days
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        
        # Rolling averages
        df['aqi_ma_3'] = df['aqi'].rolling(window=3, min_periods=1).mean()
        df['aqi_ma_7'] = df['aqi'].rolling(window=7, min_periods=1).mean()
        
        # Features
        feature_cols = ['day_num', 'hour', 'day_of_week', 'aqi_ma_3', 'aqi_ma_7']
        X = df[feature_cols].values
        y = df['aqi'].values
        
        return X, y
    
    def fit(self, data: List[Dict[str, Any]]) -> 'AQIPrediction':
        """
        Train prediction model
        
        Args:
            data: Historical AQI data
        
        Returns:
            self
        """
        df = self.prepare_time_series(data)
        X, y = self.create_features(df)
        
        self.model.fit(X, y)
        self.is_fitted = True
        self.last_date = df.index[-1]
        self.last_aqi = df['aqi'].iloc[-1]
        
        # Store recent history for MA calculation
        self.recent_aqi = df['aqi'].tail(7).tolist()
        
        logger.info(f"Prediction model trained on {len(data)} samples")
        return self
    
    def predict_future(self, base_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Dự báo AQI cho các ngày tới
        
        Args:
            base_date: Ngày bắt đầu dự báo (mặc định: ngày cuối của training data)
        
        Returns:
            List of predictions
        """
        if not self.is_fitted:
            raise ValueError("Model not trained yet")
        
        if base_date is None:
            base_date = self.last_date
        
        predictions = []
        current_aqi_history = self.recent_aqi.copy()
        
        for day in range(1, self.forecast_days + 1):
            forecast_date = base_date + timedelta(days=day)
            
            # Calculate features
            day_num = (forecast_date - self.last_date).days + self.last_date.day
            hour = 12  # Noon prediction
            day_of_week = forecast_date.weekday()
            aqi_ma_3 = np.mean(current_aqi_history[-3:]) if len(current_aqi_history) >= 3 else self.last_aqi
            aqi_ma_7 = np.mean(current_aqi_history[-7:]) if len(current_aqi_history) >= 7 else self.last_aqi
            
            # Predict
            X = np.array([[day_num, hour, day_of_week, aqi_ma_3, aqi_ma_7]])
            predicted_aqi = float(self.model.predict(X)[0])
            
            # Ensure AQI is in valid range
            predicted_aqi = max(0, min(500, predicted_aqi))
            
            predictions.append({
                'date': forecast_date.strftime('%Y-%m-%d'),
                'predicted_aqi': round(predicted_aqi, 2),
                'confidence': self._calculate_confidence(day),
                'category': self._aqi_category(predicted_aqi)
            })
            
            # Update history for next prediction
            current_aqi_history.append(predicted_aqi)
        
        logger.info(f"Generated {len(predictions)} predictions")
        return predictions
    
    def _calculate_confidence(self, days_ahead: int) -> str:
        """Tính confidence level dựa trên khoảng cách dự báo"""
        if days_ahead <= 2:
            return "high"
        elif days_ahead <= 5:
            return "medium"
        else:
            return "low"
    
    def _aqi_category(self, aqi: float) -> str:
        """Phân loại AQI"""
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"
    
    def simple_moving_average(self, data: List[Dict[str, Any]], window: int = 7) -> List[Dict[str, Any]]:
        """
        Phương pháp dự báo đơn giản bằng Moving Average
        
        Args:
            data: Historical data
            window: Window size for MA
        
        Returns:
            Predictions
        """
        df = self.prepare_time_series(data)
        recent_aqi = df['aqi'].tail(window).values
        avg_aqi = np.mean(recent_aqi)
        
        predictions = []
        base_date = df.index[-1]
        
        for day in range(1, self.forecast_days + 1):
            forecast_date = base_date + timedelta(days=day)
            # Simple: assume next days similar to average
            predicted_aqi = avg_aqi * (1 + np.random.uniform(-0.1, 0.1))  # Add small variation
            
            predictions.append({
                'date': forecast_date.strftime('%Y-%m-%d'),
                'predicted_aqi': round(predicted_aqi, 2),
                'method': 'moving_average',
                'category': self._aqi_category(predicted_aqi)
            })
        
        return predictions

