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
Correlation Analysis - Phân tích tương quan
Phân tích mối liên hệ giữa môi trường (AQI) và giáo dục (Green Score)
"""
import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class CorrelationAnalysis:
    """Phân tích tương quan môi trường - giáo dục"""
    
    def __init__(self, min_samples: int = 3):
        """
        Initialize correlation analysis
        
        Args:
            min_samples: Số mẫu tối thiểu để phân tích
        """
        self.min_samples = min_samples
    
    def prepare_data(self, 
                     environment_data: List[Dict[str, Any]], 
                     education_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Chuẩn bị dữ liệu cho phân tích tương quan
        Merge environment và education data theo vị trí địa lý
        
        Args:
            environment_data: AQI data với latitude, longitude
            education_data: School data với latitude, longitude, green_score
        
        Returns:
            DataFrame đã merge
        """
        if not environment_data or not education_data:
            raise ValueError("Insufficient data for correlation analysis")
        
        # Convert to DataFrames
        env_df = pd.DataFrame(environment_data)
        edu_df = pd.DataFrame(education_data)
        
        # For simplicity, match by closest location (simplified version)
        # In production, use proper spatial join
        merged_data = []
        
        for _, school in edu_df.iterrows():
            # Find closest environment measurement
            school_lat = school.get('latitude')
            school_lon = school.get('longitude')
            
            if school_lat is None or school_lon is None:
                continue
            
            # Calculate distances
            env_df['distance'] = np.sqrt(
                (env_df['latitude'] - school_lat)**2 + 
                (env_df['longitude'] - school_lon)**2
            )
            
            # Get closest measurement
            closest_env = env_df.loc[env_df['distance'].idxmin()]
            
            # Combine data
            merged_data.append({
                'school_id': school.get('id'),
                'school_name': school.get('name'),
                'green_score': school.get('green_score', 0),
                'total_students': school.get('total_students', 0),
                'aqi': closest_env.get('aqi', 0),
                'pm25': closest_env.get('pm25', 0),
                'latitude': school_lat,
                'longitude': school_lon,
                'distance_km': closest_env.get('distance') * 111  # Convert to km (rough)
            })
        
        df = pd.DataFrame(merged_data)
        
        logger.info(f"Prepared {len(df)} matched records for correlation")
        return df
    
    def pearson_correlation(self, x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """
        Tính Pearson correlation coefficient
        
        Args:
            x: Variable 1
            y: Variable 2
        
        Returns:
            (correlation, p_value)
        """
        if len(x) < self.min_samples:
            raise ValueError(f"Need at least {self.min_samples} samples")
        
        correlation, p_value = stats.pearsonr(x, y)
        return correlation, p_value
    
    def spearman_correlation(self, x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """
        Tính Spearman correlation coefficient (non-parametric)
        
        Args:
            x: Variable 1
            y: Variable 2
        
        Returns:
            (correlation, p_value)
        """
        if len(x) < self.min_samples:
            raise ValueError(f"Need at least {self.min_samples} samples")
        
        correlation, p_value = stats.spearmanr(x, y)
        return correlation, p_value
    
    def analyze(self, 
                environment_data: List[Dict[str, Any]], 
                education_data: List[Dict[str, Any]], 
                method: str = 'pearson') -> Dict[str, Any]:
        """
        Phân tích tương quan chính
        
        Args:
            environment_data: Environment measurements
            education_data: School data
            method: 'pearson' hoặc 'spearman'
        
        Returns:
            Correlation analysis results
        """
        df = self.prepare_data(environment_data, education_data)
        
        if len(df) < self.min_samples:
            raise ValueError(f"Insufficient data: need at least {self.min_samples} samples, got {len(df)}")
        
        results = {
            'n_samples': len(df),
            'correlations': {},
            'insights': []
        }
        
        # 1. AQI vs Green Score (chính)
        aqi = df['aqi'].values
        green_score = df['green_score'].values
        
        if method == 'pearson':
            corr, p_value = self.pearson_correlation(aqi, green_score)
        else:
            corr, p_value = self.spearman_correlation(aqi, green_score)
        
        results['correlations']['aqi_vs_green_score'] = {
            'correlation': round(float(corr), 4),
            'p_value': round(float(p_value), 4),
            'significant': p_value < 0.05,
            'interpretation': self._interpret_correlation(corr, p_value)
        }
        
        # 2. PM2.5 vs Green Score
        if 'pm25' in df.columns:
            pm25 = df['pm25'].values
            if method == 'pearson':
                corr_pm, p_pm = self.pearson_correlation(pm25, green_score)
            else:
                corr_pm, p_pm = self.spearman_correlation(pm25, green_score)
            
            results['correlations']['pm25_vs_green_score'] = {
                'correlation': round(float(corr_pm), 4),
                'p_value': round(float(p_pm), 4),
                'significant': p_pm < 0.05,
                'interpretation': self._interpret_correlation(corr_pm, p_pm)
            }
        
        # 3. AQI vs Student Count (optional)
        if 'total_students' in df.columns:
            students = df['total_students'].values
            if method == 'pearson':
                corr_st, p_st = self.pearson_correlation(aqi, students)
            else:
                corr_st, p_st = self.spearman_correlation(aqi, students)
            
            results['correlations']['aqi_vs_students'] = {
                'correlation': round(float(corr_st), 4),
                'p_value': round(float(p_st), 4),
                'significant': p_st < 0.05
            }
        
        # Generate insights
        results['insights'] = self._generate_insights(results['correlations'], df)
        
        # Summary statistics
        results['summary'] = {
            'avg_aqi': round(float(df['aqi'].mean()), 2),
            'avg_green_score': round(float(df['green_score'].mean()), 2),
            'aqi_range': [round(float(df['aqi'].min()), 2), round(float(df['aqi'].max()), 2)],
            'green_score_range': [round(float(df['green_score'].min()), 2), round(float(df['green_score'].max()), 2)]
        }
        
        logger.info(f"Correlation analysis completed with {len(df)} samples")
        return results
    
    def _interpret_correlation(self, corr: float, p_value: float) -> str:
        """Diễn giải correlation coefficient"""
        if p_value >= 0.05:
            return "Không có mối tương quan có ý nghĩa thống kê"
        
        abs_corr = abs(corr)
        strength = ""
        if abs_corr < 0.3:
            strength = "yếu"
        elif abs_corr < 0.7:
            strength = "trung bình"
        else:
            strength = "mạnh"
        
        direction = "nghịch" if corr < 0 else "thuận"
        
        return f"Tương quan {direction} {strength} (r={corr:.3f}, p<0.05)"
    
    def _generate_insights(self, correlations: Dict[str, Any], df: pd.DataFrame) -> List[str]:
        """Tạo insights từ correlation analysis"""
        insights = []
        
        # Main correlation
        main_corr = correlations.get('aqi_vs_green_score', {})
        if main_corr.get('significant'):
            corr_val = main_corr['correlation']
            if corr_val < -0.3:
                insights.append(
                    f"🌿 Phát hiện: Trường có Green Score cao thường ở khu vực có AQI thấp hơn "
                    f"(tương quan nghịch r={corr_val:.3f}). "
                    f"Điều này cho thấy giáo dục xanh có thể liên quan đến môi trường tốt hơn."
                )
            elif corr_val > 0.3:
                insights.append(
                    f"⚠️ Cảnh báo: Trường có Green Score cao lại ở khu vực AQI cao "
                    f"(tương quan thuận r={corr_val:.3f}). "
                    f"Cần đầu tư cải thiện môi trường xung quanh các trường."
                )
        else:
            insights.append(
                "📊 Không tìm thấy mối tương quan rõ ràng giữa AQI và Green Score. "
                "Cần thêm dữ liệu hoặc các yếu tố khác ảnh hưởng."
            )
        
        # Best and worst areas
        best_areas = df.nsmallest(3, 'aqi')[['school_name', 'aqi', 'green_score']]
        insights.append(
            f"✅ Top 3 khu vực tốt nhất: {', '.join(best_areas['school_name'].tolist())} "
            f"với AQI trung bình {best_areas['aqi'].mean():.1f}"
        )
        
        worst_areas = df.nlargest(3, 'aqi')[['school_name', 'aqi', 'green_score']]
        insights.append(
            f"🚨 Top 3 khu vực cần cải thiện: {', '.join(worst_areas['school_name'].tolist())} "
            f"với AQI trung bình {worst_areas['aqi'].mean():.1f}"
        )
        
        return insights

