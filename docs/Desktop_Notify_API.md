# Desktop Notify API Reference

Complete API documentation for the Python Desktop Notify library.

## 📋 Table of Contents

- [Core Functions](#core-functions)
- [NotificationManager Class](#notificationmanager-class)
- [Backend System](#backend-system)
- [Icon System](#icon-system)
- [Type Definitions](#type-definitions)
- [Exceptions](#exceptions)

## 🚀 Core Functions

### `send_notification()`

Send a desktop notification using the global manager.

```python
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
) -> Union[bool, str]
```

**Parameters:**
- `icon` (str): Icon name, path, or unicode character
- `title` (str): Notification title
- `message` (str): Notification message/body
- `notification_id` (Optional[str]): ID for notification updates/replacement
- `urgency` (str): Urgency level - 'low', 'normal', 'critical'
- `timeout` (Optional[int]): Timeout in milliseconds (None=default, 0=persistent)
- `actions` (Optional[Dict[str, str]]): Dict of action_id -> label for buttons
- `action_callback` (Optional[Callable]): Function called when action is selected
- `**kwargs`: Backend-specific parameters

**Returns:**
- Without actions: `True` if sent successfully, `False` otherwise
- With actions: Selected `action_id` string or `None` if timeout/dismissed

**Examples:**

```python
# Basic notification
success = send_notification("info", "Task Complete", "File processed successfully")

# Interactive notification with actions
def handle_action(action_id):
    if action_id == "open":
        subprocess.run(["xdg-open", "/path/to/file"])

actions = {"open": "Open File", "dismiss": "Dismiss"}
result = send_notification(
    icon="save",
    title="Download Complete",
    message="document.pdf has been downloaded",
    actions=actions,
    action_callback=handle_action
)
```

### `is_notifications_available()`

Check if desktop notifications are available on the system.

```python
def is_notifications_available() -> bool
```

**Returns:** `True` if notifications can be sent, `False` otherwise

### `get_notification_backend()`

Get the name of the current notification backend.

```python
def get_notification_backend() -> Optional[str]
```

**Returns:** Backend name ('dunst', 'console', etc.) or `None` if unavailable

## 🔧 NotificationManager Class

Advanced notification manager with configurable backends and features.

### Constructor

```python
class NotificationManager:
    def __init__(
        self,
        backend: str = "auto",
        icon_set: str = "auto", 
        timeout: Optional[int] = None,
        urgency: str = "normal",
        **kwargs
    )
```

**Parameters:**
- `backend` (str): Backend name ('auto', 'dunst', 'console')
- `icon_set` (str): Icon set name ('auto', 'system', 'material', 'minimal')
- `timeout` (Optional[int]): Default timeout in milliseconds
- `urgency` (str): Default urgency level
- `**kwargs`: Additional configuration options

### Core Methods

#### `send()`

Send a notification with backward-compatible return value.

```python
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
) -> Union[bool, str]
```

Same parameters and return value as `send_notification()`.

#### `send_detailed()`

Send a notification with detailed feedback including icon resolution information.

```python
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
) -> NotificationResult
```

**Returns:** `NotificationResult` with complete details about the notification and icon resolution process.

**Example:**
```python
result = manager.send_detailed("save", "Processing", "Working on files...")
print(f"Backend used: {result.backend_used}")
print(f"Icon resolved to: {result.icon_resolution.resolved_path}")
print(f"Icon source: {result.icon_resolution.source.value}")
print(f"Resolution time: {result.icon_resolution.resolution_time_ms:.2f}ms")
```

### Information Methods

#### `get_last_notification_result()`

Get detailed information about the last notification sent.

```python
def get_last_notification_result(self) -> Optional[NotificationResult]
```

**Returns:** `NotificationResult` with details, or `None` if no notifications sent yet.

#### `get_last_resolved_icon()`

Get details about the last icon resolution.

```python
def get_last_resolved_icon(self) -> Optional[IconResolutionInfo]
```

**Returns:** `IconResolutionInfo` for the last resolved icon, or `None` if no resolution yet.

#### `get_backend_info()`

```python
def get_backend_info(self) -> Optional[Dict[str, Any]]
```

Get detailed information about the current backend.

**Returns:** Dictionary with backend metadata:
```python
{
    "name": "dunst",
    "priority": 90,
    "available": True,
    "features": ["actions", "urgency", "timeout", "icons"],
    "version": "1.9.0",
    "description": "Dunst notification daemon backend"
}
```

#### `is_available()`

```python
def is_available(self) -> bool
```

Check if the manager's notification system is available.

### Management Methods

#### `list_available_backends()`

```python
def list_available_backends(self) -> List[str]
```

List all available notification backends on the system.

#### `switch_backend()`

```python
def switch_backend(self, backend_name: str) -> bool
```

Switch to a different notification backend.

#### `list_available_icon_sets()`

```python
def list_available_icon_sets(self) -> List[str]
```

List all available icon sets.

#### `switch_icon_set()`

```python
def switch_icon_set(self, icon_set_name: str) -> bool
```

Switch to a different icon set.

#### `test_notification()`

```python
def test_notification(self) -> bool
```

Send a test notification to verify functionality.

## 🔌 Backend System

### NotificationBackend (Base Class)

Abstract base class for notification backends.

```python
class NotificationBackend(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    
    @property  
    @abstractmethod
    def priority(self) -> int: ...
    
    @abstractmethod
    def send_notification(...) -> Union[bool, str]: ...
    
    @abstractmethod
    def is_available(self) -> bool: ...
    
    @abstractmethod
    def get_backend_info(self) -> Dict[str, Any]: ...
```

### Available Backends

#### DunstBackend

High-priority backend for Dunst notification daemon.

**Features:**
- Interactive actions with user selection
- Notification IDs for updates/replacement
- Urgency levels (low, normal, critical)
- Timeout control
- Icon support (system icons, paths, unicode)
- Markup support
- Sound control

#### ConsoleBackend  

Fallback backend that outputs to terminal/console.

**Features:**
- Colored output with urgency indicators
- Timestamp support
- Icon to unicode conversion
- Actions display (non-interactive)

## 🎨 Icon System

### Icon Sets

#### SystemIconSet

Uses system-installed icon themes via the `icon-mapper` library.

#### MaterialIconSet

Material Design icon collection with SVG support.

#### MinimalIconSet

Unicode/emoji fallback icon set.

### Icon Manager

Central management for icon sets with automatic fallback.

```python
from desktop_notify.iconsets.manager import get_icon_set_manager

manager = get_icon_set_manager()

# Switch icon sets
manager.set_active_icon_set("material")

# Get icon with fallback
icon = manager.get_icon("save", fallback=True)

# Get detailed resolution info
resolution = manager.get_icon_detailed("save", fallback=True)
```

## 📝 Type Definitions

### NotificationResult

```python
@dataclass
class NotificationResult:
    success: bool                          # Whether notification was sent
    action_result: Optional[str] = None    # Selected action (for interactive notifications)
    icon_resolution: Optional[IconResolutionInfo] = None
    backend_used: Optional[str] = None     # Which backend was used
    notification_id: Optional[str] = None  # ID used for the notification
    send_time_ms: Optional[float] = None   # Time taken to send
    total_time_ms: Optional[float] = None  # Total time including resolution
    error_message: Optional[str] = None    # Error details if failed
```

### IconResolutionInfo

```python
@dataclass
class IconResolutionInfo:
    original_name: str                    # Original icon name requested
    resolved_path: Optional[str]          # Final resolved path/glyph
    source: IconResolutionSource          # Where the icon came from
    icon_set_used: Optional[str] = None   # Which icon set was used
    theme_name: Optional[str] = None      # System theme name (if applicable)
    size: Optional[int] = None            # Icon size (if applicable)
    is_fallback: bool = False             # Whether fallback was used
    attempted_sources: list = None        # List of sources tried
    fallback_chain: list = None           # Chain of fallback attempts
    resolution_time_ms: Optional[float] = None  # Time taken to resolve
    cached: bool = False                  # Whether result was cached
```

### IconResolutionSource

```python
class IconResolutionSource(Enum):
    SYSTEM_THEME = "system_theme"     # Resolved from system icon theme
    MATERIAL = "material"             # Material Design icon set
    NERDFONTS = "nerdfonts"          # Nerd Fonts icon set  
    MINIMAL = "minimal"              # Unicode/emoji fallback
    FILE_PATH = "file_path"          # Direct file path
    UNICODE = "unicode"              # Unicode character/emoji
    FALLBACK = "fallback"            # Final fallback icon
    NOT_FOUND = "not_found"          # Icon not resolved
```

## ⚠️ Exceptions

### DesktopNotifyError

Base exception for all desktop notify errors.

### BackendError

Raised when backend operations fail.

### IconError

Raised when icon resolution fails.

---

## 📚 Usage Examples

### Basic Usage

```python
from desktop_notify import send_notification

# Simple notification
send_notification("info", "Hello", "Desktop notifications working!")

# With parameters
send_notification(
    icon="warning",
    title="Low Disk Space", 
    message="Only 500MB remaining",
    urgency="critical",
    timeout=10000
)
```

### Advanced Usage with Manager

```python
from desktop_notify import NotificationManager

# Create manager with specific configuration
manager = NotificationManager(
    backend="dunst",
    icon_set="material",
    timeout=5000
)

# Send notifications (backward compatible)
manager.send("save", "Backup Complete", "Files saved to cloud")

# NEW: Send with detailed feedback
result = manager.send_detailed("save", "Processing", "Working on files...")
print(f"Backend used: {result.backend_used}")
print(f"Icon resolved to: {result.icon_resolution.resolved_path}")
print(f"Icon source: {result.icon_resolution.source.value}")
print(f"Resolution time: {result.icon_resolution.resolution_time_ms:.2f}ms")
```

### Interactive Notifications

```python
def handle_download_action(action_id):
    if action_id == "open":
        subprocess.run(["xdg-open", "/path/to/file.pdf"])
    elif action_id == "folder":
        subprocess.run(["xdg-open", "/downloads/"])

download_actions = {
    "open": "Open File",
    "folder": "Open Folder",
    "dismiss": "Dismiss"
}

result = manager.send(
    icon="success",
    title="Download Complete",
    message="document.pdf has been downloaded",
    actions=download_actions,
    action_callback=handle_download_action,
    timeout=15000
)

print(f"User selected: {result}")
```

### Icon Resolution Feedback

```python
# Send notification and get detailed resolution info
result = manager.send_detailed("unknown_icon", "Test", "Fallback test")

if result.icon_resolution:
    resolution = result.icon_resolution
    print(f"Original: {resolution.original_name}")
    print(f"Resolved: {resolution.resolved_path}")
    print(f"Source: {resolution.source.value}")
    print(f"Fallback used: {resolution.is_fallback}")
    print(f"Resolution time: {resolution.resolution_time_ms:.2f}ms")
    
    if resolution.fallback_chain:
        print(f"Fallback chain: {resolution.fallback_chain}")
```

---

*Desktop Notify v1.0.0 - API Reference*