# ────────────────────────────────────────────────────────────────────────────────
# Base Notification Backend Interface
# ────────────────────────────────────────────────────────────────────────────────
"""
base.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Abstract base class for notification backend implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable, Union


class NotificationBackend(ABC):
    """
    ///////////////////////////////////////////////////////////////////
    NOTIFICATION BACKEND BASE
    ▄▄▄▄ ▄▄▄▄ ▄▄▄▄ ▄▄ ▄▄▄ ▄▄▄▄▄ ▄▄▄
    █▄▄▄ █▄▄▄ █    ██ █▀█   █   █▀▀
    █▄▄▄ █▄▄▄ █▄▄▄ ██ █▄█   █   █▄▄
    ///////////////////////////////////////////////////////////////////
    Abstract base class for notification backend implementations.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this backend."""
        pass
    
    @property
    @abstractmethod
    def priority(self) -> int:
        """Return the priority of this backend (higher = more preferred)."""
        pass
    
    @abstractmethod
    def send_notification(
        self,
        icon: str,
        title: str,
        message: str,
        notification_id: Optional[str] = None,
        urgency: str = 'normal',
        timeout: Optional[int] = None,
        actions: Optional[Dict[str, str]] = None,
        action_callback: Optional[Callable[[str], None]] = None,
        **kwargs
    ) -> Union[bool, str]:
        """
        Send a desktop notification.
        
        Args:
            icon: Icon name or path
            title: Notification title
            message: Notification message/body
            notification_id: Optional ID for notification updates
            urgency: Urgency level ('low', 'normal', 'critical')
            timeout: Timeout in milliseconds (None = default, 0 = persistent)
            actions: Optional dict of action_id -> label for notification buttons
            action_callback: Optional callback function for handling action selection
            **kwargs: Backend-specific parameters
            
        Returns:
            For notifications without actions: True if sent successfully, False otherwise
            For notifications with actions: Selected action_id string or None if timeout/dismissed
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this backend is available on the system.
        
        Returns:
            True if backend can be used, False otherwise
        """
        pass
    
    @abstractmethod
    def get_backend_info(self) -> Dict[str, Any]:
        """
        Get information about this backend.
        
        Returns:
            Dictionary containing backend metadata and capabilities
        """
        pass
    
    def supports_feature(self, feature: str) -> bool:
        """
        Check if backend supports a specific feature.
        
        Args:
            feature: Feature name ('notification_id', 'urgency', 'timeout', 
                    'markup', 'actions', 'sound', 'persistent', 'callbacks')
            
        Returns:
            True if feature is supported, False otherwise
        """
        info = self.get_backend_info()
        features = info.get('features', [])
        return feature in features
    
    def validate_urgency(self, urgency: str) -> str:
        """
        Validate and normalize urgency level.
        
        Args:
            urgency: Urgency level to validate
            
        Returns:
            Normalized urgency level
        """
        valid_urgencies = ['low', 'normal', 'critical']
        urgency_lower = urgency.lower()
        
        if urgency_lower in valid_urgencies:
            return urgency_lower
        
        # Map common alternatives
        urgency_map = {
            'info': 'normal',
            'information': 'normal',
            'warn': 'normal', 
            'warning': 'normal',
            'error': 'critical',
            'high': 'critical',
            'urgent': 'critical',
        }
        
        return urgency_map.get(urgency_lower, 'normal')
    
    def validate_timeout(self, timeout: Optional[int]) -> Optional[int]:
        """
        Validate and normalize timeout value.
        
        Args:
            timeout: Timeout in milliseconds
            
        Returns:
            Validated timeout value
        """
        if timeout is None:
            return None
        
        # Ensure non-negative
        if timeout < 0:
            return 0
            
        # Some backends have limits
        max_timeout = 60000  # 60 seconds
        if timeout > max_timeout:
            return max_timeout
            
        return timeout