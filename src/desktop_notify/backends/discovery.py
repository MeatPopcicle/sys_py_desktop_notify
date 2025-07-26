# ────────────────────────────────────────────────────────────────────────────────
# Backend Discovery System
# ────────────────────────────────────────────────────────────────────────────────
"""
discovery.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Automatic backend discovery and selection system.
"""

import logging
from typing import Dict, List, Optional, Type

from .base import NotificationBackend
from .dunst import DunstBackend
from .console import ConsoleBackend


class BackendDiscovery:
    """
    ///////////////////////////////////////////////////////////////////
    BACKEND DISCOVERY
    ▄▄▄▄ ▄▄▄ ▄▄▄▄ ▄▄ ▄▄▄▄ ▄▄▄▄ ▄▄ ▄▄▄
    █▄▄▄ █▀█ █    ██ █▄▄▄ █▄▄▄ ██ █▀▀
    █▄▄▄ █▄█ █▄▄▄ ██ █▄▄▄ █▄▄▄ ██ █▄▄
    ///////////////////////////////////////////////////////////////////
    Automatic discovery and selection of notification backends.
    """
    
    def __init__(self):
        """Initialize backend discovery."""
        self.logger = logging.getLogger(__name__)
        
        # ─────────────────────────────────────────────────────────────────
        # Register default backend classes
        # ─────────────────────────────────────────────────────────────────
        self.backend_classes: Dict[str, Type[NotificationBackend]] = {
            "dunst": DunstBackend,
            "console": ConsoleBackend,
        }
        
        # ─────────────────────────────────────────────────────────────────
        # Cache for initialized backends
        # ─────────────────────────────────────────────────────────────────
        self._backend_cache: Dict[str, NotificationBackend] = {}
        self._available_backends: Optional[List[str]] = None
    
    def register_backend(self, name: str, backend_class: Type[NotificationBackend]) -> None:
        """
        Register a custom backend class.
        
        Args:
            name: Backend name
            backend_class: Backend class to register
        """
        self.backend_classes[name] = backend_class
        self.logger.info(f"Registered backend: {name}")
        
        # Clear cache to force re-discovery
        self._available_backends = None
    
    def get_backend(self, name: str) -> Optional[NotificationBackend]:
        """
        Get a backend instance by name.
        
        Args:
            name: Backend name
            
        Returns:
            Backend instance or None if not available
        """
        if name not in self.backend_classes:
            self.logger.error(f"Unknown backend: {name}")
            return None
        
        # Return cached instance if available
        if name in self._backend_cache:
            return self._backend_cache[name]
        
        # Initialize backend
        try:
            backend_class = self.backend_classes[name]
            backend = backend_class()
            
            # Cache the instance
            self._backend_cache[name] = backend
            
            self.logger.debug(f"Initialized backend: {name}")
            return backend
            
        except Exception as e:
            self.logger.warning(f"Failed to initialize backend '{name}': {e}")
            return None
    
    def discover_available_backends(self) -> List[str]:
        """
        Discover all available backends on the system.
        
        Returns:
            List of available backend names
        """
        if self._available_backends is not None:
            return self._available_backends
        
        available = []
        
        for name in self.backend_classes:
            backend = self.get_backend(name)
            if backend and backend.is_available():
                available.append(name)
                self.logger.debug(f"Backend '{name}' is available")
            else:
                self.logger.debug(f"Backend '{name}' is not available")
        
        # Sort by priority (higher = better)
        available.sort(key=lambda name: self.get_backend(name).priority, reverse=True)
        
        self._available_backends = available
        self.logger.info(f"Discovered {len(available)} available backends: {available}")
        
        return available
    
    def get_best_backend(self, preferred: Optional[str] = None) -> Optional[NotificationBackend]:
        """
        Get the best available backend.
        
        Args:
            preferred: Preferred backend name (None for auto-selection)
            
        Returns:
            Best backend instance or None if none available
        """
        available_backends = self.discover_available_backends()
        
        if not available_backends:
            self.logger.error("No notification backends available")
            return None
        
        # ─────────────────────────────────────────────────────────────────
        # Use preferred backend if specified and available
        # ─────────────────────────────────────────────────────────────────
        if preferred:
            if preferred in available_backends:
                backend = self.get_backend(preferred)
                if backend:
                    self.logger.info(f"Using preferred backend: {preferred}")
                    return backend
            else:
                self.logger.warning(f"Preferred backend '{preferred}' not available")
        
        # ─────────────────────────────────────────────────────────────────
        # Auto-select best backend (highest priority)
        # ─────────────────────────────────────────────────────────────────
        best_backend_name = available_backends[0]  # Already sorted by priority
        backend = self.get_backend(best_backend_name)
        
        if backend:
            self.logger.info(f"Auto-selected backend: {best_backend_name}")
            return backend
        
        return None
    
    def list_all_backends(self) -> List[str]:
        """
        List all registered backend names.
        
        Returns:
            List of all backend names
        """
        return list(self.backend_classes.keys())
    
    def get_backend_info(self, name: str) -> Optional[Dict[str, any]]:
        """
        Get information about a specific backend.
        
        Args:
            name: Backend name
            
        Returns:
            Backend information dictionary or None
        """
        backend = self.get_backend(name)
        if backend:
            return backend.get_backend_info()
        return None
    
    def get_all_backend_info(self) -> Dict[str, Dict[str, any]]:
        """
        Get information about all registered backends.
        
        Returns:
            Dictionary mapping backend names to their info
        """
        info = {}
        
        for name in self.backend_classes:
            backend_info = self.get_backend_info(name)
            if backend_info:
                info[name] = backend_info
        
        return info
    
    def test_backend(self, name: str) -> bool:
        """
        Test a specific backend.
        
        Args:
            name: Backend name to test
            
        Returns:
            True if backend test successful
        """
        backend = self.get_backend(name)
        if not backend:
            return False
        
        if not backend.is_available():
            return False
        
        # Try to send a test notification
        try:
            if hasattr(backend, 'test_notification'):
                return backend.test_notification()
            else:
                # Fallback test
                return backend.send_notification(
                    icon="info",
                    title="Backend Test",
                    message=f"Testing {name} backend",
                    timeout=3000
                )
        except Exception as e:
            self.logger.error(f"Backend test failed for '{name}': {e}")
            return False
    
    def test_all_backends(self) -> Dict[str, bool]:
        """
        Test all available backends.
        
        Returns:
            Dictionary mapping backend names to test results
        """
        results = {}
        available_backends = self.discover_available_backends()
        
        for name in available_backends:
            results[name] = self.test_backend(name)
            
        return results
    
    def clear_cache(self) -> None:
        """Clear backend cache and force re-discovery."""
        self._backend_cache.clear()
        self._available_backends = None
        self.logger.debug("Cleared backend cache")