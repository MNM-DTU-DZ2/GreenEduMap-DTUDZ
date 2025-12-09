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

"""FCM (Firebase Cloud Messaging) service for push notifications."""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status

try:
    from firebase_admin import messaging
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

from app.models import FCMToken, User
from app.core.firebase import get_firebase_app, is_fcm_enabled

logger = logging.getLogger(__name__)


class FCMService:
    """Service for managing FCM tokens and sending push notifications."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def register_token(
        self,
        user_id: str,
        token: str,
        device_type: str = "ios",
        device_name: Optional[str] = None,
        device_id: Optional[str] = None
    ) -> FCMToken:
        """
        Register or update FCM token for a user.
        
        If token already exists, update it.
        If device_id exists for this user, update that token.
        Otherwise, create new token.
        """
        # Check if token already exists
        stmt = select(FCMToken).where(FCMToken.token == token)
        result = await self.db.execute(stmt)
        existing_token = result.scalar_one_or_none()
        
        if existing_token:
            # Update existing token
            existing_token.user_id = user_id
            existing_token.device_type = device_type
            existing_token.device_name = device_name
            existing_token.device_id = device_id
            existing_token.is_active = True
            existing_token.updated_at = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(existing_token)
            logger.info(f"Updated FCM token for user {user_id}")
            return existing_token
        
        # Check if device_id exists for this user
        if device_id:
            stmt = select(FCMToken).where(
                FCMToken.user_id == user_id,
                FCMToken.device_id == device_id
            )
            result = await self.db.execute(stmt)
            device_token = result.scalar_one_or_none()
            
            if device_token:
                # Update token for this device
                device_token.token = token
                device_token.device_type = device_type
                device_token.device_name = device_name
                device_token.is_active = True
                device_token.updated_at = datetime.utcnow()
                await self.db.commit()
                await self.db.refresh(device_token)
                logger.info(f"Updated FCM token for device {device_id}")
                return device_token
        
        # Create new token
        fcm_token = FCMToken(
            user_id=user_id,
            token=token,
            device_type=device_type,
            device_name=device_name,
            device_id=device_id,
            is_active=True
        )
        
        self.db.add(fcm_token)
        await self.db.commit()
        await self.db.refresh(fcm_token)
        
        logger.info(f"Registered new FCM token for user {user_id}")
        return fcm_token
    
    async def get_user_tokens(self, user_id: str, active_only: bool = True) -> List[FCMToken]:
        """Get all FCM tokens for a user."""
        stmt = select(FCMToken).where(FCMToken.user_id == user_id)
        
        if active_only:
            stmt = stmt.where(FCMToken.is_active == True)
        
        stmt = stmt.order_by(FCMToken.created_at.desc())
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def remove_token(self, token_id: str, user_id: str) -> bool:
        """
        Deactivate an FCM token.
        
        Returns:
            True if token was deactivated, False if not found
        """
        stmt = select(FCMToken).where(
            FCMToken.id == token_id,
            FCMToken.user_id == user_id
        )
        result = await self.db.execute(stmt)
        token = result.scalar_one_or_none()
        
        if not token:
            return False
        
        token.is_active = False
        token.updated_at = datetime.utcnow()
        await self.db.commit()
        
        logger.info(f"Deactivated FCM token {token_id}")
        return True
    
    async def send_notification(
        self,
        user_id: str,
        title: str,
        body: str,
        data: Optional[Dict[str, str]] = None,
        image_url: Optional[str] = None,
        sound: str = "default"
    ) -> Dict[str, Any]:
        """
        Send push notification to all active devices of a user.
        
        Returns:
            Dictionary with success/failure counts and details
        """
        if not is_fcm_enabled():
            logger.warning("FCM is not enabled or configured")
            return {
                "success": False,
                "sent_count": 0,
                "failed_count": 0,
                "message": "FCM is not enabled",
                "details": None
            }
        
        # Get user's active tokens
        tokens = await self.get_user_tokens(user_id, active_only=True)
        
        if not tokens:
            logger.warning(f"No active FCM tokens found for user {user_id}")
            return {
                "success": False,
                "sent_count": 0,
                "failed_count": 0,
                "message": "No active FCM tokens found for user",
                "details": None
            }
        
        # Build notification
        notification = messaging.Notification(
            title=title,
            body=body,
            image=image_url
        )
        
        # Build message for each token
        sent_count = 0
        failed_count = 0
        failed_tokens = []
        
        for fcm_token in tokens:
            try:
                message = messaging.Message(
                    notification=notification,
                    data=data or {},
                    token=fcm_token.token,
                    apns=messaging.APNSConfig(
                        payload=messaging.APNSPayload(
                            aps=messaging.Aps(
                                sound=sound,
                                badge=1
                            )
                        )
                    )
                )
                
                # Send message
                response = messaging.send(message)
                
                # Update token stats
                fcm_token.notification_count += 1
                fcm_token.last_used = datetime.utcnow()
                sent_count += 1
                
                logger.info(f"Sent notification to token {fcm_token.id}: {response}")
                
            except messaging.UnregisteredError:
                # Token is invalid, deactivate it
                fcm_token.is_active = False
                failed_count += 1
                failed_tokens.append(str(fcm_token.id))
                logger.warning(f"Token {fcm_token.id} is unregistered, deactivating")
                
            except Exception as e:
                failed_count += 1
                failed_tokens.append(str(fcm_token.id))
                logger.error(f"Failed to send notification to token {fcm_token.id}: {e}")
        
        await self.db.commit()
        
        return {
            "success": sent_count > 0,
            "sent_count": sent_count,
            "failed_count": failed_count,
            "message": f"Sent to {sent_count} device(s), {failed_count} failed",
            "details": {
                "failed_tokens": failed_tokens
            } if failed_tokens else None
        }
    
    async def send_batch_notification(
        self,
        user_ids: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Send notification to multiple users.
        
        Returns:
            Dictionary with total sent/failed counts
        """
        total_sent = 0
        total_failed = 0
        
        for user_id in user_ids:
            result = await self.send_notification(user_id, title, body, data)
            total_sent += result["sent_count"]
            total_failed += result["failed_count"]
        
        return {
            "success": total_sent > 0,
            "sent_count": total_sent,
            "failed_count": total_failed,
            "message": f"Batch sent to {total_sent} device(s), {total_failed} failed",
            "total_users": len(user_ids)
        }
