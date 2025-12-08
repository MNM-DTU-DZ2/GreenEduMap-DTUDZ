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
Clustering Model - Phân vùng xanh/vàng/đỏ
Sử dụng K-Means để phân vùng dựa trên AQI và Green Score
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class EnvironmentClustering:
    """Phân vùng môi trường - giáo dục"""
    
    def __init__(self, n_clusters: int = 3):
        """
        Initialize clustering model
        
        Args:
            n_clusters: Số clusters (mặc định 3: xanh, vàng, đỏ)
        """
        self.n_clusters = n_clusters
        self.model = None
        self.scaler = StandardScaler()
        self.cluster_labels = {
            0: "green",    # Vùng tốt
            1: "yellow",   # Vùng trung bình
            2: "red"       # Vùng kém
        }
    
    def prepare_data(self, data: List[Dict[str, Any]]) -> np.ndarray:
        """
        Chuẩn bị dữ liệu cho clustering
        
        Args:
            data: List of dict với keys: aqi, green_score, latitude, longitude
        
        Returns:
            numpy array đã normalize
        """
        if not data:
            raise ValueError("No data provided for clustering")
        
        # Extract features
        features = []
        for item in data:
            features.append([
                item.get('aqi', 0),
                item.get('green_score', 0),
                item.get('latitude', 0),
                item.get('longitude', 0)
            ])
        
        X = np.array(features)
        
        # Normalize
        X_scaled = self.scaler.fit_transform(X)
        
        logger.info(f"Prepared {len(data)} samples for clustering")
        return X_scaled
    
    def fit(self, X: np.ndarray) -> 'EnvironmentClustering':
        """
        Train clustering model
        
        Args:
            X: Normalized feature matrix
        
        Returns:
            self
        """
        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=42,
            n_init=10
        )
        self.model.fit(X)
        
        logger.info(f"Clustering model trained with {self.n_clusters} clusters")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict cluster labels
        
        Args:
            X: Feature matrix
        
        Returns:
            Cluster labels
        """
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        return self.model.predict(X)
    
    def assign_zones(self, data: List[Dict[str, Any]], labels: np.ndarray) -> List[Dict[str, Any]]:
        """
        Gán nhãn vùng (green/yellow/red) dựa trên AQI trung bình của cluster
        
        Args:
            data: Original data
            labels: Cluster labels from model
        
        Returns:
            Data với zone labels
        """
        # Tính AQI trung bình cho mỗi cluster
        cluster_aqi = {}
        for i in range(self.n_clusters):
            cluster_mask = labels == i
            cluster_data = [data[j] for j in range(len(data)) if cluster_mask[j]]
            avg_aqi = np.mean([d.get('aqi', 0) for d in cluster_data])
            cluster_aqi[i] = avg_aqi
        
        # Sắp xếp clusters theo AQI (thấp -> cao)
        sorted_clusters = sorted(cluster_aqi.items(), key=lambda x: x[1])
        
        # Map clusters to zones
        cluster_to_zone = {}
        if self.n_clusters == 3:
            cluster_to_zone[sorted_clusters[0][0]] = "green"    # AQI thấp nhất
            cluster_to_zone[sorted_clusters[1][0]] = "yellow"   # AQI trung bình
            cluster_to_zone[sorted_clusters[2][0]] = "red"      # AQI cao nhất
        else:
            # For other n_clusters, use generic naming
            for idx, (cluster_id, _) in enumerate(sorted_clusters):
                cluster_to_zone[cluster_id] = f"zone_{idx}"
        
        # Gán zone cho từng data point
        results = []
        for i, item in enumerate(data):
            result = item.copy()
            cluster_id = int(labels[i])
            result['cluster_id'] = cluster_id
            result['zone'] = cluster_to_zone[cluster_id]
            result['zone_avg_aqi'] = cluster_aqi[cluster_id]
            results.append(result)
        
        logger.info(f"Assigned zones to {len(results)} points")
        return results
    
    def fit_predict(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Train và predict trong một bước
        
        Args:
            data: Input data
        
        Returns:
            Data với cluster assignments
        """
        X = self.prepare_data(data)
        self.fit(X)
        labels = self.predict(X)
        results = self.assign_zones(data, labels)
        
        return results
    
    def get_cluster_stats(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Thống kê các clusters
        
        Args:
            results: Clustering results
        
        Returns:
            Statistics dict
        """
        stats = {
            'total_points': len(results),
            'zones': {}
        }
        
        for zone in ['green', 'yellow', 'red']:
            zone_data = [r for r in results if r.get('zone') == zone]
            if zone_data:
                stats['zones'][zone] = {
                    'count': len(zone_data),
                    'avg_aqi': np.mean([d.get('aqi', 0) for d in zone_data]),
                    'avg_green_score': np.mean([d.get('green_score', 0) for d in zone_data]),
                    'percentage': len(zone_data) / len(results) * 100
                }
        
        return stats

