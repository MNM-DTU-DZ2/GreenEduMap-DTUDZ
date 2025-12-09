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

"""Firebase Admin SDK initialization."""
import os
import logging
from typing import Optional
from pathlib import Path

try:
    import firebase_admin
    from firebase_admin import credentials, messaging
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    logging.warning("Firebase Admin SDK not installed. FCM notifications disabled.")

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global Firebase app instance
_firebase_app: Optional[firebase_admin.App] = None


def init_firebase() -> Optional[firebase_admin.App]:
    """
    Initialize Firebase Admin SDK.
    
    Returns:
        Firebase App instance or None if Firebase is disabled/unavailable
    """
    global _firebase_app
    
    if not FIREBASE_AVAILABLE:
        logger.warning("Firebase Admin SDK not available")
        return None
    
    if not settings.FCM_ENABLED:
        logger.info("FCM is disabled in settings")
        return None
    
    if _firebase_app is not None:
        logger.debug("Firebase already initialized")
        return_firebase_app
    
    try:
        # Check if credentials file exists
        cred_path = settings.FIREBASE_CREDENTIALS_PATH
        
        if not cred_path or not os.path.exists(cred_path):
            logger.error(f"Firebase credentials file not found: {cred_path}")
            logger.info("FCM notifications will be disabled")
            return None
        
        # Initialize Firebase app
        cred = credentials.Certificate(cred_path)
        _firebase_app = firebase_admin.initialize_app(cred, {
            'projectId': settings.FIREBASE_PROJECT_ID,
        })
        
        logger.info(f"✅ Firebase initialized successfully (Project: {settings.FIREBASE_PROJECT_ID})")
        return _firebase_app
        
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        logger.info("FCM notifications will be disabled")
        return None


def get_firebase_app() -> Optional[firebase_admin.App]:
    """
    Get Firebase app instance (dependency injection).
    
    Returns:
        Firebase App instance or None if not initialized
    """
    if _firebase_app is None:
        return init_firebase()
    return _firebase_app


def is_fcm_enabled() -> bool:
    """Check if FCM is enabled and properly configured."""
    return FIREBASE_AVAILABLE and settings.FCM_ENABLED and _firebase_app is not None
