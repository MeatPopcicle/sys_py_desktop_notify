# Desktop Notify API Reference

Complete API documentation for the Python Desktop Notify library.

## 📋 Table of Contents

- [Core Functions](#core-functions)
- [NotificationManager Class](#notificationmanager-class)
- [Backend System](#backend-system)
- [Icon System](#icon-system)
- [Configuration](#configuration)
- [Exceptions](#exceptions)
- [Type Definitions](#type-definitions)

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

# Notification with timeout and urgency
send_notification(
    icon="warning",
    title="Low Disk Space", 
    message="Only 500MB remaining",
    urgency="critical",
    timeout=10000  # 10 seconds
)

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

**Example:**
```python
if is_notifications_available():
    send_notification("info", "System Ready", "All services started")
else:
    print("Desktop notifications not available")
```

### `get_notification_backend()`

Get the name of the current notification backend.

```python
def get_notification_backend() -> Optional[str]
```

**Returns:** Backend name ('dunst', 'console', etc.) or `None` if unavailable

**Example:**
```python
backend = get_notification_backend()
print(f"Using backend: {backend}")
```

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

### Methods

#### `send()`

Send a notification with full parameter control.

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

#### `is_available()`

```python
def is_available(self) -> bool
```

Check if the manager's notification system is available.

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

**Parameters:**
- `backend_name` (str): Name of backend to switch to

**Returns:** `True` if switch successful

#### `switch_icon_set()`

```python
def switch_icon_set(self, icon_set_name: str) -> bool
```

Switch to a different icon set.

**Parameters:**
- `icon_set_name` (str): Name of icon set ('system', 'material', 'minimal')

**Returns:** `True` if switch successful

#### `list_available_icon_sets()`

```python
def list_available_icon_sets(self) -> List[str]
```

List all available icon sets.

#### `test_notification()`

```python
def test_notification(self) -> bool
```

Send a test notification to verify functionality.

### Usage Examples

```python
from desktop_notify import NotificationManager

# Create manager with specific backend
manager = NotificationManager(
    backend="dunst",
    icon_set="material", 
    timeout=5000,
    urgency="normal"
)

# Send notifications
manager.send("save", "Backup Complete", "Files saved to cloud")

# Check backend info
info = manager.get_backend_info()
print(f"Backend: {info['name']}, Features: {info['features']}")

# Switch backends
if manager.switch_backend("console"):
    print("Switched to console backend")

# Interactive notification example
def call_handler(action):
    if action == "answer":
        print("Answering call...")
    elif action == "decline":
        print("Declining call...")

call_actions = {"answer": "Answer", "decline": "Decline"}
result = manager.send(
    icon="phone",
    title="Incoming Call",
    message="Alice is calling...",
    actions=call_actions,
    action_callback=call_handler,
    timeout=30000  # 30 second timeout
)
```

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
    
    def supports_feature(self, feature: str) -> bool: ...
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

**Configuration:**
```python
backend = DunstBackend(command="dunstify")
```

#### ConsoleBackend  

Fallback backend that outputs to terminal/console.

**Features:**
- Colored output with urgency indicators
- Timestamp support
- Icon to unicode conversion
- Actions display (non-interactive)

**Configuration:**
```python
backend = ConsoleBackend(use_colors=True, timestamp=True)
```

### Backend Discovery

The system automatically discovers and prioritizes available backends.

```python
from desktop_notify.backends.discovery import BackendDiscovery

discovery = BackendDiscovery()

# Get best available backend
backend = discovery.get_best_backend()

# Get specific backend
dunst = discovery.get_backend("dunst")

# List all available
available = discovery.discover_available_backends()
```

## 🎨 Icon System

### Icon Sets

#### SystemIconSet

Uses system-installed icon themes via the `icon-mapper` library.

**Features:**
- Desktop theme integration
- Scalable icon resolution
- Fallback chains

**Usage:**
```python
from desktop_notify.iconsets.system import SystemIconSet

icon_set = SystemIconSet()
icon_path = icon_set.get_icon("document-save")
```

#### MaterialIconSet

Material Design icon collection with SVG support.

**Usage:**
```python
from desktop_notify.iconsets.material import MaterialIconSet

icon_set = MaterialIconSet()
icon_path = icon_set.get_icon("save")
```

#### MinimalIconSet

Unicode/emoji fallback icon set.

**Usage:**
```python
from desktop_notify.iconsets.minimal import MinimalIconSet

icon_set = MinimalIconSet() 
icon = icon_set.get_icon("save")  # Returns "💾"
```

### Icon Manager

Central management for icon sets with automatic fallback.

```python
from desktop_notify.iconsets.manager import get_icon_set_manager

manager = get_icon_set_manager()

# Switch icon sets
manager.set_active_icon_set("material")

# Get icon with fallback
icon = manager.get_icon("save", fallback=True)

# List available sets
sets = manager.list_available_sets()

# Preview icon set
preview = manager.preview_icon_set("minimal")
```

## ⚙️ Configuration

### Configuration Loading

```python
from desktop_notify.config import get_config

config = get_config()
print(f"Default backend: {config.backend}")
print(f"Default icon set: {config.icon_set}")
```

### Configuration Schema

```toml
[notification]
backend = "auto"           # Backend preference
timeout = 3000            # Default timeout (ms)
urgency = "normal"        # Default urgency
log_icon_resolution = false

[icons]
icon_set = "auto"         # Icon set preference  
icon_system_theme = "Papirus"
icon_system_size = 48

[backends.dunst]
command = "dunstify"
supports_markup = true

[backends.console]
use_colors = true
timestamp = true
```

### Environment Variables

Override configuration with environment variables:

```bash
export DESKTOP_NOTIFY_BACKEND=dunst
export DESKTOP_NOTIFY_ICON_SET=material
export DESKTOP_NOTIFY_TIMEOUT=5000
export DESKTOP_NOTIFY_URGENCY=low
```

## ⚠️ Exceptions

### DesktopNotifyError

Base exception for all desktop notify errors.

```python
from desktop_notify.exceptions import DesktopNotifyError

try:
    send_notification("invalid", "Test", "Message")
except DesktopNotifyError as e:
    print(f"Notification error: {e}")
```

### BackendError

Raised when backend operations fail.

```python
from desktop_notify.exceptions import BackendError
```

### IconError

Raised when icon resolution fails.

```python
from desktop_notify.exceptions import IconError
```

## 📝 Type Definitions

### ActionCallback

```python
from typing import Callable

ActionCallback = Callable[[str], None]

def my_callback(action_id: str) -> None:
    print(f"Action selected: {action_id}")
```

### ActionDict

```python
from typing import Dict

ActionDict = Dict[str, str]  # action_id -> label

actions: ActionDict = {
    "save": "Save File",
    "cancel": "Cancel Operation"
}
```

### BackendInfo

```python
from typing import Dict, Any, List

BackendInfo = Dict[str, Any]

example_info: BackendInfo = {
    "name": str,
    "priority": int,
    "available": bool,
    "features": List[str],
    "description": str
}
```

---

## 📚 Advanced Usage Examples

### Application Integration

```python
class MyApplication:
    def __init__(self):
        self.notifier = NotificationManager(
            backend="dunst",
            icon_set="material",
            timeout=5000
        )
    
    def process_file(self, filename):
        # Start notification
        self.notifier.send(
            "info", "Processing", f"Working on {filename}...",
            notification_id="process"
        )
        
        try:
            # Do work...
            time.sleep(2)
            
            # Success notification (replaces previous)
            self.notifier.send(
                "success", "Complete", f"{filename} processed",
                notification_id="process"
            )
        except Exception as e:
            # Error notification
            self.notifier.send(
                "error", "Failed", f"Error: {e}",
                notification_id="process",
                urgency="critical"
            )
```

### Interactive Workflows

```python
def download_with_actions():
    def handle_download_action(action):
        if action == "open":
            subprocess.run(["xdg-open", "/downloads/file.pdf"])
        elif action == "folder":
            subprocess.run(["xdg-open", "/downloads/"])
    
    # Simulate download
    send_notification("info", "Downloading", "file.pdf starting...")
    time.sleep(3)
    
    # Download complete with actions
    actions = {
        "open": "Open File",
        "folder": "Open Folder", 
        "dismiss": "Dismiss"
    }
    
    result = send_notification(
        icon="download",
        title="Download Complete",
        message="file.pdf ready",
        actions=actions,
        action_callback=handle_download_action,
        timeout=15000
    )
    
    print(f"User selected: {result}")
```

### Custom Backend Example

```python
from desktop_notify.backends.base import NotificationBackend

class EmailBackend(NotificationBackend):
    def __init__(self, smtp_server, email):
        self.smtp_server = smtp_server
        self.email = email
    
    @property
    def name(self):
        return "email"
    
    @property  
    def priority(self):
        return 50
    
    def send_notification(self, icon, title, message, **kwargs):
        # Send email notification
        import smtplib
        # Implementation here...
        return True
    
    def is_available(self):
        return True  # Check SMTP connectivity
    
    def get_backend_info(self):
        return {
            "name": self.name,
            "priority": self.priority,
            "features": ["email"],
            "smtp_server": self.smtp_server
        }
```

---

*Desktop Notify v1.0.0 - Complete API Reference*