# ────────────────────────────────────────────────────────────────────────────────
# Desktop Notify Main API
# ────────────────────────────────────────────────────────────────────────────────
"""
api.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Main API interface for desktop notification system.
"""

import logging
import time
from typing import Any, Dict, List, Optional, Callable, Union

from .backends.discovery import BackendDiscovery
from .iconsets.manager import get_icon_set_manager
from .config import get_config
from .exceptions import DesktopNotifyError, BackendError, IconError
from .types import NotificationResult, IconResolutionInfo


class NotificationManager:
    """
    ///////////////////////////////////////////////////////////////////
    NOTIFICATION MANAGER
    ▄▄▄▄▄ ▄▄▄▄ ▄▄▄ ▄▄▄▄▄ ▄▄▄ ▄▄▄▄▄ ▄▄▄ ▄▄▄  ▄▄
    █▄▄▄▄ █▄▄▄ █▀▀   █   █▀█   █   █   █▀▀  ██
    █▄▄▄▄ █▄▄▄ █▄▄   █   █▄█   █   █▄▄ █▄▄  ██
    ///////////////////////////////////////////////////////////////////
    Advanced notification manager with configurable backends and icons.
    """
    
    def __init__(
        self,
        backend: str = "auto",
        icon_set: str = "auto",
        timeout: Optional[int] = None,
        urgency: str = "normal",
        **kwargs
    ):
        """
        Initialize notification manager.
        
        Args:
            backend: Backend name ("auto", "dunst", "console")
            icon_set: Icon set name ("auto", "system", "material", "minimal")
            timeout: Default timeout in milliseconds
            urgency: Default urgency level ("low", "normal", "critical")
            **kwargs: Additional configuration options
        """
        self.logger = logging.getLogger(__name__)
        
        # ─────────────────────────────────────────────────────────────────
        # Load configuration
        # ─────────────────────────────────────────────────────────────────
        self.config = get_config()
        
        # ─────────────────────────────────────────────────────────────────
        # Initialize backend discovery
        # ─────────────────────────────────────────────────────────────────
        self.backend_discovery = BackendDiscovery()
        
        # ─────────────────────────────────────────────────────────────────
        # Set configuration overrides from parameters
        # ─────────────────────────────────────────────────────────────────
        self.preferred_backend = backend if backend != "auto" else self.config.backend
        self.preferred_icon_set = icon_set if icon_set != "auto" else self.config.icon_set
        self.default_timeout = timeout if timeout is not None else self.config.timeout
        self.default_urgency = urgency if urgency != "normal" else self.config.urgency
        
        # ─────────────────────────────────────────────────────────────────
        # Initialize components
        # ─────────────────────────────────────────────────────────────────
        self.backend = None
        self.icon_manager = None
        self._last_notification_result: Optional[NotificationResult] = None
        
        self._initialize_backend()
        self._initialize_icon_manager()
        
        self.logger.debug(f"NotificationManager initialized with backend: {self.backend.name if self.backend else 'None'}")
    
    def _initialize_backend(self) -> None:
        """Initialize the notification backend."""
        try:
            self.backend = self.backend_discovery.get_best_backend(
                preferred=self.preferred_backend if self.preferred_backend != "auto" else None
            )
            
            if not self.backend:
                raise BackendError("No notification backends available")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize backend: {e}")
            self.backend = None
    
    def _initialize_icon_manager(self) -> None:
        """Initialize the icon manager."""
        try:
            self.icon_manager = get_icon_set_manager(
                preferred_icon_set=self.preferred_icon_set
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize icon manager: {e}")
            self.icon_manager = None
    
    def send(
        self,
        icon: str,
        title: str,
        message: str,
        notification_id: Optional[str] = None,
        urgency: Optional[str] = None,
        timeout: Optional[int] = None,
        actions: Optional[Dict[str, str]] = None,
        action_callback: Optional[Callable[[str], None]] = None,
        **kwargs
    ) -> Union[bool, str]:
        """
        Send a desktop notification with backward-compatible return value.
        
        For detailed information including icon resolution details,
        use send_detailed() or get_last_notification_result().
        """
        result = self.send_detailed(
            icon=icon,
            title=title,
            message=message,
            notification_id=notification_id,
            urgency=urgency,
            timeout=timeout,
            actions=actions,
            action_callback=action_callback,
            **kwargs
        )
        
        # Return backward-compatible value
        if actions:
            return result.action_result
        else:
            return result.success
    
    def send_detailed(
        self,
        icon: str,
        title: str,
        message: str,
        notification_id: Optional[str] = None,
        urgency: Optional[str] = None,
        timeout: Optional[int] = None,
        actions: Optional[Dict[str, str]] = None,
        action_callback: Optional[Callable[[str], None]] = None,
        **kwargs
    ) -> NotificationResult:
        """
        Send a desktop notification with detailed resolution information.
        
        Returns:
            NotificationResult with complete details about the notification
            and icon resolution process.
        """
        total_start_time = time.time()
        
        # Initialize result object
        result = NotificationResult(
            success=False,
            backend_used=self.backend.name if self.backend else None,
            notification_id=notification_id
        )
        
        if not self.backend:
            result.error_message = "No notification backend available"
            self.logger.error(result.error_message)
            self._last_notification_result = result
            return result
        
        try:
            # ─────────────────────────────────────────────────────────────────
            # Resolve icon with detailed information
            # ─────────────────────────────────────────────────────────────────
            icon_resolution = self._resolve_icon_detailed(icon)
            result.icon_resolution = icon_resolution
            
            # ─────────────────────────────────────────────────────────────────
            # Use defaults for unspecified parameters
            # ─────────────────────────────────────────────────────────────────
            final_urgency = urgency or self.default_urgency
            final_timeout = timeout if timeout is not None else self.default_timeout
            
            # ─────────────────────────────────────────────────────────────────
            # Send notification via backend
            # ─────────────────────────────────────────────────────────────────
            send_start_time = time.time()
            
            backend_result = self.backend.send_notification(
                icon=icon_resolution.resolved_path or icon,
                title=title,
                message=message,
                notification_id=notification_id,
                urgency=final_urgency,
                timeout=final_timeout,
                actions=actions,
                action_callback=action_callback,
                **kwargs
            )
            
            result.send_time_ms = (time.time() - send_start_time) * 1000
            result.total_time_ms = (time.time() - total_start_time) * 1000
            
            if actions:
                # For interactive notifications
                result.action_result = backend_result if isinstance(backend_result, str) else None
                result.success = backend_result is not None
                
                if result.action_result:
                    self.logger.debug(f"Action selected for '{title}': {result.action_result}")
                else:
                    self.logger.debug(f"No action selected for '{title}' (timeout/dismiss)")
            else:
                # For regular notifications
                result.success = bool(backend_result)
                
                if result.success:
                    self.logger.debug(f"Sent notification: {title}")
                else:
                    self.logger.warning(f"Failed to send notification: {title}")
            
            self._last_notification_result = result
            return result
            
        except Exception as e:
            error_msg = f"Error sending notification: {e}"
            result.error_message = error_msg
            result.total_time_ms = (time.time() - total_start_time) * 1000
            self.logger.error(error_msg)
            self._last_notification_result = result
            return result
    
    def _resolve_icon(self, icon: str) -> str:
        """
        Resolve icon name to path/glyph using icon manager.
        
        Args:
            icon: Icon name to resolve
            
        Returns:
            Resolved icon path/glyph or fallback
        """
        if not self.icon_manager:
            self.logger.debug(f"📎 No icon manager available, using '{icon}' as-is")
            return icon  # Return as-is if no icon manager
        
        try:
            # Check if we should log resolution
            should_log = self._should_log_resolution()
            
            if should_log:
                active_set = self.icon_manager.get_active_icon_set()
                self.logger.info(f"🎨 Resolving icon '{icon}' using set: {active_set}")
            
            resolved = self.icon_manager.get_icon(icon, fallback=True)
            
            if resolved and resolved != icon:
                if should_log:
                    self.logger.info(f"🎯 Final resolution: '{icon}' → '{resolved}'")
                else:
                    self.logger.debug(f"Icon resolved: '{icon}' -> '{resolved}'")
                return resolved
            else:
                if should_log:
                    self.logger.info(f"📎 Using original icon name: '{icon}'")
                return icon
                
        except Exception as e:
            self.logger.error(f"Icon resolution failed for '{icon}': {e}")
            return icon
    
    def _resolve_icon_detailed(self, icon: str) -> IconResolutionInfo:
        """
        Resolve icon name with detailed information.
        
        Args:
            icon: Icon name to resolve
            
        Returns:
            IconResolutionInfo with complete resolution details
        """
        if not self.icon_manager:
            # Create basic resolution info for missing icon manager
            from .types import IconResolutionSource
            return IconResolutionInfo(
                original_name=icon,
                resolved_path=icon,
                source=IconResolutionSource.NOT_FOUND
            )
        
        try:
            return self.icon_manager.get_icon_detailed(icon, fallback=True)
        except Exception as e:
            self.logger.error(f"Icon resolution failed for '{icon}': {e}")
            from .types import IconResolutionSource
            return IconResolutionInfo(
                original_name=icon,
                resolved_path=icon,
                source=IconResolutionSource.NOT_FOUND
            )
    
    def _should_log_resolution(self) -> bool:
        """Check if icon resolution should be logged based on config."""
        try:
            return self.config.log_icon_resolution
        except:
            return False
    
    def is_available(self) -> bool:
        """
        Check if notification system is available.
        
        Returns:
            True if notifications can be sent
        """
        return self.backend is not None and self.backend.is_available()
    
    def get_backend_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the current backend.
        
        Returns:
            Backend information dictionary or None
        """
        if self.backend:
            return self.backend.get_backend_info()
        return None
    
    def list_available_backends(self) -> List[str]:
        """
        List available notification backends.
        
        Returns:
            List of backend names
        """
        return self.backend_discovery.discover_available_backends()
    
    def switch_backend(self, backend_name: str) -> bool:
        """
        Switch to a different notification backend.
        
        Args:
            backend_name: Name of backend to switch to
            
        Returns:
            True if switch successful
        """
        try:
            new_backend = self.backend_discovery.get_backend(backend_name)
            
            if not new_backend:
                self.logger.error(f"Backend '{backend_name}' not available")
                return False
            
            if not new_backend.is_available():
                self.logger.error(f"Backend '{backend_name}' is not available")
                return False
            
            self.backend = new_backend
            self.preferred_backend = backend_name
            
            self.logger.info(f"Switched to backend: {backend_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to switch backend: {e}")
            return False
    
    def switch_icon_set(self, icon_set_name: str) -> bool:
        """
        Switch to a different icon set.
        
        Args:
            icon_set_name: Name of icon set to switch to
            
        Returns:
            True if switch successful
        """
        if not self.icon_manager:
            return False
        
        return self.icon_manager.set_active_icon_set(icon_set_name)
    
    def list_available_icon_sets(self) -> List[str]:
        """
        List available icon sets.
        
        Returns:
            List of icon set names
        """
        if self.icon_manager:
            return self.icon_manager.list_available_sets()
        return []
    
    def get_last_notification_result(self) -> Optional[NotificationResult]:
        """
        Get detailed information about the last notification sent.
        
        Returns:
            NotificationResult with details, or None if no notifications sent yet
        """
        return self._last_notification_result
    
    def get_last_resolved_icon(self) -> Optional[IconResolutionInfo]:
        """
        Get details about the last icon resolution.
        
        Returns:
            IconResolutionInfo for the last resolved icon, or None if no resolution yet
        """
        if self.icon_manager:
            return self.icon_manager.get_last_resolved_icon()
        return None
    
    def test_notification(self) -> bool:
        """
        Send a test notification.
        
        Returns:
            True if test successful
        """
        result = self.send_detailed(
            icon="info",
            title="Desktop Notify Test",
            message="Test notification from desktop-notify library",
            timeout=3000
        )
        return result.success


# ═══════════════════════════════════════════════════════════════════════════════
# Global notification manager instance
# ═══════════════════════════════════════════════════════════════════════════════
_global_manager: Optional[NotificationManager] = None


def get_notification_manager(**kwargs) -> NotificationManager:
    """
    Get the global notification manager instance.
    
    Args:
        **kwargs: Configuration overrides for manager initialization
        
    Returns:
        NotificationManager instance
    """
    global _global_manager
    
    if _global_manager is None:
        _global_manager = NotificationManager(**kwargs)
    
    return _global_manager


# ═══════════════════════════════════════════════════════════════════════════════
# Simple API Functions
# ═══════════════════════════════════════════════════════════════════════════════

def send_notification(
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
    ///////////////////////////////////////////////////////////////////
    SEND DESKTOP NOTIFICATION
    ▄▄▄▄▄ ▄▄▄▄ ▄▄ ▄▄▄▄  
    █▄▄▄▄ █▄▄▄ ██ █▄▄▄  
    ▄▄▄▄█ █▄▄▄ ██ █▄▄▄  
    ///////////////////////////////////////////////////////////////////
    Send a desktop notification using the global manager.
    
    Args:
        icon: Icon name or path
        title: Notification title
        message: Notification message
        notification_id: Optional ID for notification updates
        urgency: Urgency level ('low', 'normal', 'critical')
        timeout: Timeout in milliseconds (None = default, 0 = persistent)
        actions: Optional dict of action_id -> label for notification buttons
        action_callback: Optional callback function for handling action selection
        **kwargs: Additional backend-specific parameters
        
    Returns:
        For notifications without actions: True if sent successfully, False otherwise
        For notifications with actions: Selected action_id string or None if timeout/dismissed
        
    Example:
        send_notification("mic", "Recording Started", "Audio recording in progress")
    """
    manager = get_notification_manager()
    return manager.send(
        icon=icon,
        title=title,
        message=message,
        notification_id=notification_id,
        urgency=urgency,
        timeout=timeout,
        actions=actions,
        action_callback=action_callback,
        **kwargs
    )


def is_notifications_available() -> bool:
    """
    Check if desktop notifications are available.
    
    Returns:
        True if notifications can be sent
    """
    try:
        manager = get_notification_manager()
        return manager.is_available()
    except Exception:
        return False


def get_notification_backend() -> Optional[str]:
    """
    Get the name of the current notification backend.
    
    Returns:
        Backend name or None if no backend available
    """
    try:
        manager = get_notification_manager()
        if manager.backend:
            return manager.backend.name
        return None
    except Exception:
        return None