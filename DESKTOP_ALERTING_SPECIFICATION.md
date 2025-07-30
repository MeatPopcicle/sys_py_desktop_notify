# Desktop Alerting System - Project Specification

## Executive Summary

Build a comprehensive, backend-agnostic Python interface for desktop notification systems on Linux. This system serves as a unified API that can target multiple notification backends (Dunst, libnotify, systemd notifications) while providing rich icon resolution, configuration management, and extensible backend architecture.

**DEPENDENCY NOTE**: This desktop alerting utility should utilize the icon resolution library located at:
`/home/gauol/Scratch/Projects - Code/icon-mapper` (icon_mapper package) for all SystemIconSet functionality.

## Problem Statement

Linux desktop applications face fragmented notification ecosystems:
- Different notification daemons (Dunst, GNOME Shell, KDE, systemd-based)
- Inconsistent APIs and command-line interfaces
- Icon handling varies between backends
- No standardized configuration approach
- Backend-specific features require different implementations
- Testing and fallback handling is complex

## Project Goals

### Primary Goals
1. **Unified API**: Single Python interface for all notification backends
2. **Backend Abstraction**: Pluggable architecture supporting multiple notification systems
3. **Rich Icon Support**: Comprehensive icon resolution with multiple icon sets
4. **Zero Configuration**: Intelligent backend detection and sane defaults
5. **Extensibility**: Easy to add new backends and icon sets

### Secondary Goals
1. **Configuration Management**: TOML-based configuration with environment variable overrides
2. **Advanced Features**: Notification updates, urgency levels, timeout control
3. **Fallback Systems**: Graceful degradation when backends are unavailable
4. **Testing Framework**: Comprehensive test coverage including integration tests

## Current Implementation Analysis

### Existing Architecture (Successfully Implemented)

The project already includes:

#### 1. Core API Layer (`src/desktop_notify/api.py`)
- **NotificationManager**: Advanced manager with configurable backends
- **Global Functions**: Simple `send_notification()` for basic usage
- **Backend Discovery**: Automatic backend selection with fallbacks

#### 2. Backend System (`src/desktop_notify/backends/`)
- **Base Backend**: Abstract interface for notification backends
- **Dunst Backend**: Full implementation with dunstify integration
- **Plugin Architecture**: Ready for additional backends (libnotify, console, etc.)

#### 3. Icon Resolution System (`src/desktop_notify/iconsets/`)
- **Icon Set Manager**: Centralized icon set management and switching
- **Multiple Icon Sets**: 
  - SystemIconSet: Uses installed desktop theme icons **[UTILIZES: /home/gauol/Scratch/Projects - Code/icon-mapper icon_mapper.IconResolver]**
  - MaterialIconSet: Modern SVG icon collection  
  - NerdFontIconSet: Font-based icons with color support
  - MinimalIconSet: Unicode/emoji fallbacks
- **Smart Resolution**: Automatic fallback between icon sets

#### 4. Configuration System (`src/desktop_notify/config.py`)
- **TOML Configuration**: Structured configuration files
- **Environment Variables**: Override configuration via env vars
- **Validation**: Type checking and validation

## Technical Architecture

### Backend Interface

```python
class NotificationBackend:
    """Abstract base for notification backends."""
    
    def send_notification(self, icon: str, title: str, message: str, 
                         notification_id: Optional[str] = None,
                         urgency: str = 'normal',
                         timeout: Optional[int] = None,
                         **kwargs) -> bool:
        """Send notification with full parameter support."""
        
    def is_available(self) -> bool:
        """Check if backend is available on system."""
        
    def get_backend_info(self) -> Dict[str, Any]:
        """Return backend capabilities and metadata."""
```

### Icon Set Architecture

```python
class IconSet:
    """Base class for icon sets."""
    
    def get_icon(self, name: str) -> Optional[str]:
        """Resolve icon name to path/glyph."""
        
    def list_icons(self) -> List[str]:
        """List all available icons."""
        
    def is_available(self) -> bool:
        """Check if icon set is available."""

# INTEGRATION IMPLEMENTATION:
# SystemIconSet should utilize icon_mapper.IconResolver from:
# /home/gauol/Scratch/Projects - Code/icon-mapper
#
# Example implementation:
# from icon_mapper import IconResolver
#
# class SystemIconSet(IconSet):
#     def __init__(self):
#         self.resolver = IconResolver()
#     
#     def get_icon(self, name: str) -> Optional[str]:
#         result = self.resolver.resolve(name)
#         return str(result) if result else None
```

### Usage Examples

#### Basic Usage
```python
from desktop_notify import send_notification

# Simple notification
send_notification("mic", "Recording Started", "Audio recording in progress")

# With parameters
send_notification(
    icon="error",
    title="Process Failed", 
    message="Could not complete operation",
    urgency="critical",
    timeout=5000
)
```

#### Advanced Usage
```python
from desktop_notify import NotificationManager

# Custom backend configuration
manager = NotificationManager(
    backend="dunst",
    default_timeout=3000,
    icon_dir="/custom/icons"
)

# Send with notification ID for updates
manager.send("load", "Processing...", "Starting task", id="task-1")
manager.send("valid", "Complete", "Task finished successfully", id="task-1")
```

#### Icon Set Management
```python
from desktop_notify.iconsets import get_icon_set_manager

icon_manager = get_icon_set_manager()

# Switch icon sets
icon_manager.set_active_icon_set("material")
icon_manager.set_active_icon_set("nerdfonts")

# List available icons
icons = icon_manager.list_icons()
preview = icon_manager.preview_icon_set("material")
```

## Implementation Requirements

### Must Have (Currently Implemented ✅)
1. **Core Notification API**
   - ✅ Simple `send_notification()` function
   - ✅ Advanced `NotificationManager` class
   - ✅ Backend abstraction with plugin system
   
2. **Dunst Backend**
   - ✅ dunstify command integration
   - ✅ Icon resolution and path handling
   - ✅ Notification ID support for updates
   - ✅ Urgency levels and timeout control

3. **Icon Resolution System**
   - ✅ Multiple icon set support (System, Material, NerdFont, Minimal)
   - ✅ Automatic fallback between icon sets
   - ✅ SVG, font glyph, and system icon support
   - ✅ Icon set switching and management

4. **Configuration Management**
   - ✅ TOML-based configuration files
   - ✅ Environment variable overrides
   - ✅ Type validation and error handling

### Should Have (Planned Extensions)
1. **Additional Backends**
   - libnotify backend for GNOME/GTK applications
   - KDE/Qt notification backend
   - systemd user notification backend
   - Console backend for headless environments

2. **Enhanced Features**
   - Notification history and persistence
   - Custom notification templates
   - Batch notification operations
   - Notification queuing and rate limiting

3. **Advanced Icon Features**
   - Dynamic icon generation
   - Icon theme detection and switching
   - Custom icon set creation tools
   - Icon caching and optimization

### Nice to Have (Future Considerations)
1. **Cross-Platform Support**
   - Windows toast notifications
   - macOS notification center
   - Web browser notifications

2. **Integration Helpers**
   - Desktop file parsing for application icons
   - MIME type to icon mapping
   - Theme integration tools

## Backend Implementation Guide

### Adding New Backends

```python
class LibnotifyBackend(NotificationBackend):
    """libnotify backend for GNOME/GTK applications."""
    
    def __init__(self, app_name: str = "desktop-notify"):
        self.app_name = app_name
        # Initialize GI bindings if available
        
    def send_notification(self, icon, title, message, **kwargs):
        # Use GI.Notify to send notifications
        pass
        
    def is_available(self):
        # Check for libnotify availability
        try:
            import gi
            gi.require_version('Notify', '0.7')
            from gi.repository import Notify
            return True
        except:
            return False
```

### Backend Registration

```python
# In NotificationManager.__init__()
self.backends = {
    "dunst": DunstNotificationBackend,
    "libnotify": LibnotifyBackend,
    "console": ConsoleBackend,
    "systemd": SystemdNotificationBackend,
}
```

## Icon Set Implementation Guide

### Creating Custom Icon Sets

```python
class CustomSVGIconSet(SVGIconSet):
    """Custom SVG icon collection."""
    
    def __init__(self):
        icons_dir = Path("/path/to/custom/icons")
        icon_mappings = {
            "custom_icon": "my-icon.svg",
            "special": "special-icon.svg",
        }
        super().__init__(icons_dir, icon_mappings)
    
    @property
    def name(self):
        return "custom"
    
    def is_available(self):
        return self.icons_dir.exists()
```

## Configuration Schema

### Main Configuration (config.toml)
```toml
[notification]
backend = "auto"  # auto, dunst, libnotify, console
timeout = 3000
urgency = "normal"

[icons]
icon_set = "auto"  # auto, material, system, nerdfonts, minimal
icon_system_theme = "Papirus"
icon_system_size = 48

[backends.dunst]
command = "dunstify"
supports_markup = true

[backends.libnotify] 
app_name = "desktop-notify"
```

### Environment Variable Overrides
```bash
DESKTOP_NOTIFY_BACKEND=dunst
DESKTOP_NOTIFY_ICON_SET=material
DESKTOP_NOTIFY_TIMEOUT=5000
DESKTOP_NOTIFY_URGENCY=low
```

## Testing Strategy

### Unit Tests (Implemented)
- ✅ Backend interface compliance
- ✅ Configuration loading and validation
- ✅ Icon resolution and fallback logic
- ✅ API function behavior

### Integration Tests (Implemented)
- ✅ End-to-end notification flow
- ✅ Backend switching and fallbacks
- ✅ Icon set switching
- ✅ Configuration file loading

### Manual Testing
- Real notification daemon interaction
- Icon theme compatibility
- Performance under load
- Error condition handling

## Quality Standards

### Code Quality (Current)
- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ >90% test coverage
- ✅ Black/ruff formatting with custom style preferences
- ✅ Pre-commit hooks

### Code Style Guidelines

Inspired by visual alignment and clarity patterns, the codebase should emphasize readability through consistent spacing and visual organization.

#### Variable Alignment & Spacing
```python
# Prefer visual alignment for related variables (when practical)
# JavaScript style inspiration: const globalEnv = require(...)
from pathlib import Path
from typing  import Optional, Dict, List

# Variable assignments with visual alignment
backend_name     = "dunst"
icon_set         = "material"
timeout_ms       = 3000
notification_id  = "app-notify-001"

# Function parameters with aligned naming
def send_notification(
    icon:              str,
    title:             str,
    message:           str,
    notification_id:   Optional[str] = None,
    urgency:           str = 'normal',
    timeout:           Optional[int] = None
) -> bool:
    """Send notification with aligned parameters for clarity."""
```

#### Header Comments & Banners
```python
# ────────────────────────────────────────────────────────────────────────────────
# Module Header (inspired by /* ---- */ style)
# ────────────────────────────────────────────────────────────────────────────────
"""
desktop_notify.py
AUTHOR: Your Name
DATE: 2024-01-15
VERSION: 1.0.0

Professional desktop notification system for Linux applications.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS & CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
import logging
from pathlib import Path
from typing  import Dict, List, Optional

# ───────────────────────────────────────────────────────────────────────────────
# Core Classes
# ───────────────────────────────────────────────────────────────────────────────
```

#### Section Dividers & Visual Blocks
```python
class NotificationManager:
    """Main notification manager with visual organization."""
    
    def __init__(self, backend: str = "auto", timeout: int = 3000):
        # ─────────────────────────────────────────────────────────────────
        # Initialize core properties
        # ─────────────────────────────────────────────────────────────────
        self.backend_name    = backend
        self.timeout         = timeout
        self.backends        = {}
        self.icon_manager    = None
        
        # ─────────────────────────────────────────────────────────────────
        # Setup logging and validation
        # ─────────────────────────────────────────────────────────────────
        self.logger = logging.getLogger(__name__)
        self._validate_configuration()

    def send_notification(self, icon: str, title: str, message: str) -> bool:
        """
        ///////////////////////////////////////////////////////////////////
        SEND DESKTOP NOTIFICATION
        ▄▄▄  ▄▄▄ ▄▄ ▄▄▄▄ ▄▄▄▄▄ ▄▄▄  ▄▄▄ ▄▄ 
        ▀▀█  █▀▀  ██  █  █   █  █▀▀  ▀▀█ ██ 
         ▄█  █▄▄  ██  █  █   █  █▄▄   ▄█ ██ 
        ///////////////////////////////////////////////////////////////////
        Send notification through configured backend with icon resolution.
        """
        # Check backend availability
        if not self._is_backend_available():
            self.logger.warning("No notification backend available")
            return False
            
        # ─────────────────────────────────────────────────────────────────
        # Resolve icon path
        # ─────────────────────────────────────────────────────────────────
        icon_path = self._resolve_icon(icon)
        if not icon_path:
            self.logger.debug(f"Using fallback icon for: {icon}")
            icon_path = self._get_fallback_icon()
            
        # ─────────────────────────────────────────────────────────────────
        # Send through backend
        # ─────────────────────────────────────────────────────────────────
        return self.backend.send_notification(
            icon=icon_path,
            title=title,
            message=message,
            timeout=self.timeout
        )
```

#### Comment Patterns
- **Header banners**: Use `─` (U+2500) for visual separation
- **Major sections**: Use `═` (U+2550) for primary divisions  
- **ASCII art headers**: Occasional decorative text for major functions
- **Inline alignment**: Variables aligned with spaces for visual clarity
- **Block comments**: Group related functionality with dividers

#### When to Break Formatting Rules
- **Readability first**: If alignment improves comprehension, override Black
- **Related variables**: Group and align assignments that belong together
- **Function signatures**: Align parameters when it clarifies the API
- **Data structures**: Align dictionary/list items when patterns emerge

#### Configuration for Tools
- Black: `skip-string-normalization = true` for visual string alignment
- Ruff: Ignore E501 (line length) when used for intentional visual alignment
- Pre-commit: Allow manual override for alignment-focused formatting

### Performance Targets
- Notification send: <50ms (including icon resolution)
- Backend initialization: <100ms
- Icon resolution: <10ms (cached), <50ms (uncached)
- Memory usage: <20MB for typical usage

### Error Handling
- Never crash on missing backends or icons
- Clear error messages with actionable guidance
- Graceful degradation to fallback systems
- Optional debug mode with detailed logging

## Distribution and Installation

### Poetry-Based Development
```bash
# Development setup
git clone https://github.com/user/desktop-notify
cd desktop-notify

# DEPENDENCY SETUP: Install icon_mapper library from local path
poetry add --editable /home/gauol/Scratch/Projects\ -\ Code/icon-mapper

poetry install
poetry shell

# Run tests
poetry run pytest
poetry run pytest --cov=desktop_notify

# Run demo
poetry run python demo.py
```

### Package Installation
```bash
# Standard installation
pip install desktop-notify

# Arch Linux (recommended)
pipx install desktop-notify

# Development/editable
pipx install --editable .
```

## API Reference

### Core Functions

```python
def send_notification(
    icon: str,
    title: str, 
    message: str,
    notification_id: Optional[str] = None,
    urgency: str = 'normal',
    timeout: Optional[int] = None,
    **kwargs
) -> bool:
    """Send a desktop notification."""

def is_notifications_available() -> bool:
    """Check if notifications are available."""

def get_notification_backend() -> NotificationBackend:
    """Get the global notification backend."""
```

### Advanced Classes

```python
class NotificationManager:
    def __init__(self, backend="auto", **kwargs): ...
    def send(self, icon, title, message, **kwargs) -> bool: ...
    def get_backend_info(self) -> Dict[str, Any]: ...
    def list_available_backends(self) -> List[str]: ...

class IconSetManager:
    def set_active_icon_set(self, name: str) -> bool: ...
    def get_icon(self, name: str, fallback=True) -> Optional[str]: ...
    def list_available_sets(self) -> List[str]: ...
    def preview_icon_set(self, name: str) -> Dict[str, str]: ...
```

## Use Case Examples

### 1. Voice Recording Application
```python
from desktop_notify import send_notification

class VoiceRecorder:
    def start_recording(self):
        send_notification("mic", "Recording Started", "Voice recording in progress")
        
    def stop_recording(self, filename):
        send_notification("save", "Recording Saved", f"Saved as {filename}")
        
    def transcription_complete(self, text):
        send_notification("typing", "Transcription Ready", text[:50] + "...")
```

### 2. System Monitoring
```python
manager = NotificationManager(urgency="critical", timeout=0)

def alert_system_error(component, error):
    manager.send("error", f"{component} Error", str(error))
    
def alert_disk_space(usage_percent):
    icon = "warning" if usage_percent > 90 else "info"
    manager.send(icon, "Disk Space", f"Usage: {usage_percent}%")
```

### 3. Development Build System
```python
from desktop_notify import NotificationManager

class BuildNotifier:
    def __init__(self):
        self.manager = NotificationManager()
        
    def build_started(self):
        self.manager.send("load", "Build Started", "Compiling project...", id="build")
        
    def build_success(self):
        self.manager.send("valid", "Build Success", "Ready for deployment", id="build")
        
    def build_failed(self, error):
        self.manager.send("error", "Build Failed", str(error), id="build")
```

## Roadmap and Next Steps

### Phase 1: Backend Expansion (Weeks 1-2)
- Implement libnotify backend for GNOME integration
- Add systemd user notification backend
- Create console backend for headless systems
- Add backend capability detection

### Phase 2: Enhanced Features (Weeks 3-4)
- Notification history and persistence
- Custom notification templates
- Batch notification operations
- Performance optimization and caching

### Phase 3: Cross-Platform (Weeks 5-6)
- Windows toast notification backend
- macOS notification center backend
- Platform detection and automatic selection

### Phase 4: Advanced Integration (Week 7)
- Desktop file parsing for app icons
- MIME type to icon mapping
- Theme detection and switching
- Icon generation tools

## Success Metrics

1. **Adoption**: Integration into 3+ open source projects
2. **Backend Coverage**: Support for 4+ notification systems
3. **Performance**: All performance targets met
4. **Reliability**: <1% failure rate in production
5. **Test Coverage**: Maintain >90% code coverage

## Integration with Existing Projects

This desktop notification system is designed to integrate seamlessly with existing applications:

### Legacy API Compatibility
```python
# Drop-in replacement for existing notification systems
from desktop_notify import send_notification

class ApplicationNotifier:
    def notify_process_start(self):
        send_notification("load", "Processing", "Operation started")
        
    def notify_process_complete(self, result):
        send_notification("valid", "Complete", f"Operation finished: {result}")
```

### Migration Support
- Drop-in replacement for common notification functions
- Maintains same function signature as popular libraries
- Enhanced icon resolution and backend support
- Configuration through standard TOML files

## Conclusion

The desktop-notify project successfully implements a comprehensive notification system with:

1. **Complete Backend Architecture**: Pluggable system supporting multiple notification daemons
2. **Advanced Icon Resolution**: Multi-format icon support with intelligent fallbacks
3. **Professional Configuration**: TOML-based config with environment overrides
4. **Extensive Testing**: Unit and integration tests with high coverage
5. **Production Ready**: Type hints, documentation, and error handling

The system is ready for immediate use and provides a solid foundation for expanding Linux desktop notification capabilities across multiple projects and environments.