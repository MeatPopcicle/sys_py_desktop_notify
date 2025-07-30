# Desktop Notify User Guide

Complete guide to getting started with the Python Desktop Notify library.

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Basic Usage](#basic-usage)
- [Interactive Notifications](#interactive-notifications)
- [Configuration](#configuration)
- [Icon Management](#icon-management)
- [Backend Management](#backend-management)
- [Real-World Examples](#real-world-examples)
- [Troubleshooting](#troubleshooting)

## 🚀 Installation

### Prerequisites

- **Python 3.8+**
- **Linux** (Ubuntu, Fedora, Arch, etc.)
- **Notification daemon** (Dunst recommended)

### Install via pip

```bash
pip install desktop-notify
```

### Install via pipx (Recommended)

```bash
pipx install desktop-notify
```

### Development Installation

```bash
git clone https://github.com/user/desktop-notify
cd desktop-notify
poetry install
```

### Verify Installation

```python
from desktop_notify import send_notification

# Test notification
success = send_notification("info", "Test", "Desktop Notify is working!")
if success:
    print("✅ Installation successful!")
else:
    print("❌ Installation issue - check dependencies")
```

## ⚡ Quick Start

### Simple Notification

```python
from desktop_notify import send_notification

# Basic notification
send_notification("info", "Hello World", "Your first notification!")
```

### Notification with Options

```python
send_notification(
    icon="warning",
    title="Important Notice", 
    message="Please save your work",
    urgency="critical",
    timeout=5000  # 5 seconds
)
```

### Interactive Notification

```python
# Define available actions
actions = {"save": "Save Now", "later": "Remind Later", "ignore": "Ignore"}

# Send interactive notification
result = send_notification(
    icon="question",
    title="Unsaved Changes",
    message="You have unsaved changes. What would you like to do?",
    actions=actions,
    timeout=10000
)

# Handle user response
if result == "save":
    print("User chose to save")
elif result == "later":
    print("User wants reminder later")
elif result == "ignore":
    print("User chose to ignore")
else:
    print("User didn't respond (timeout)")
```

## 📖 Basic Usage

### Import Options

```python
# Simple API
from desktop_notify import send_notification

# Advanced API  
from desktop_notify import NotificationManager

# Check availability
from desktop_notify import is_notifications_available
```

### Urgency Levels

```python
# Low urgency (subtle notification)
send_notification("info", "Background Task", "Completed", urgency="low")

# Normal urgency (default)
send_notification("info", "Task Complete", "File processed")

# Critical urgency (attention-grabbing)
send_notification("error", "System Error", "Critical failure", urgency="critical")
```

### Timeout Control

```python
# Default timeout (3 seconds)
send_notification("info", "Quick Message", "Default timeout")

# Custom timeout
send_notification("info", "Timed Message", "5 second timeout", timeout=5000)

# Persistent notification (stays until dismissed)
send_notification("warning", "Important", "Please acknowledge", timeout=0)
```

### Notification IDs (Updates)

```python
# Initial notification
send_notification("info", "Processing", "Starting task...", notification_id="task1")

# Update same notification
send_notification("info", "Processing", "50% complete", notification_id="task1")

# Final update
send_notification("success", "Complete", "Task finished!", notification_id="task1")
```

## 🔔 Interactive Notifications

Interactive notifications allow users to respond with predefined actions.

### Basic Actions

```python
def handle_call_action(action_id):
    if action_id == "answer":
        print("📞 Answering call...")
        # Your answer logic here
    elif action_id == "decline":
        print("📵 Declining call...")
        # Your decline logic here

# Call notification with actions
call_actions = {"answer": "Answer", "decline": "Decline"}
result = send_notification(
    icon="phone",
    title="Incoming Call",
    message="John Doe is calling...",
    actions=call_actions,
    action_callback=handle_call_action,
    timeout=30000  # 30 seconds
)
```

### File Operation Actions

```python
import subprocess

def handle_download_action(action_id):
    if action_id == "open":
        subprocess.run(["xdg-open", "/downloads/document.pdf"])
    elif action_id == "folder":
        subprocess.run(["xdg-open", "/downloads/"])

download_actions = {
    "open": "Open File",
    "folder": "Open Folder",
    "dismiss": "Dismiss"
}

result = send_notification(
    icon="download",
    title="Download Complete", 
    message="document.pdf has been downloaded",
    actions=download_actions,
    action_callback=handle_download_action
)
```

### Confirmation Dialogs

```python
def backup_files():
    # Ask for confirmation
    actions = {"yes": "Yes, Backup", "no": "Cancel"}
    result = send_notification(
        icon="question",
        title="Backup Confirmation",
        message="Backup all files to cloud storage?",
        actions=actions,
        timeout=15000
    )
    
    if result == "yes":
        # Perform backup
        send_notification("info", "Backup", "Starting backup...", notification_id="backup")
        # ... backup logic ...
        send_notification("success", "Backup Complete", "All files backed up", notification_id="backup")
    else:
        print("Backup cancelled")
```

## ⚙️ Configuration

### Configuration File

Create `~/.config/desktop-notify/config.toml`:

```toml
[notification]
backend = "dunst"
timeout = 4000
urgency = "normal"
log_icon_resolution = false

[icons]
icon_set = "material"
icon_system_theme = "Papirus"
icon_system_size = 48

[backends.dunst]
command = "dunstify"

[backends.console]
use_colors = true
timestamp = true
```

### Environment Variables

```bash
# Override configuration
export DESKTOP_NOTIFY_BACKEND=console
export DESKTOP_NOTIFY_ICON_SET=minimal
export DESKTOP_NOTIFY_TIMEOUT=6000
export DESKTOP_NOTIFY_URGENCY=low
```

### Runtime Configuration

```python
from desktop_notify import NotificationManager

# Custom configuration
manager = NotificationManager(
    backend="dunst",
    icon_set="material",
    timeout=5000,
    urgency="normal"
)

manager.send("info", "Custom Config", "Using custom settings")
```

## 🎨 Icon Management

### Icon Types

```python
# System icons (requires icon theme)
send_notification("document-save", "Saved", "File saved successfully")

# Material Design icons
send_notification("save", "Saved", "Using Material icon")

# Unicode/Emoji icons  
send_notification("💾", "Saved", "Using emoji icon")

# File paths
send_notification("/path/to/icon.png", "Custom", "Using custom icon")
```

### Icon Set Management

```python
from desktop_notify import NotificationManager

manager = NotificationManager()

# List available icon sets
icon_sets = manager.list_available_icon_sets()
print(f"Available icon sets: {icon_sets}")

# Switch icon set
if manager.switch_icon_set("material"):
    print("Switched to Material Design icons")

# Check current icon set
from desktop_notify.iconsets.manager import get_icon_set_manager
icon_manager = get_icon_set_manager()
current_set = icon_manager.get_active_icon_set()
print(f"Current icon set: {current_set}")
```

### Icon Previews

```python
from desktop_notify.iconsets.manager import get_icon_set_manager

icon_manager = get_icon_set_manager()

# Preview icon set
preview = icon_manager.preview_icon_set("material")
for icon_name, icon_path in preview.items():
    print(f"{icon_name}: {icon_path}")
```

## 🔌 Backend Management

### Check Available Backends

```python
from desktop_notify import NotificationManager

manager = NotificationManager()

# List available backends
backends = manager.list_available_backends()
print(f"Available backends: {backends}")

# Get current backend info
info = manager.get_backend_info()
print(f"Current backend: {info['name']}")
print(f"Features: {info['features']}")
```

### Switch Backends

```python
# Switch to specific backend
if manager.switch_backend("console"):
    print("Switched to console backend")
    
# Test new backend
manager.test_notification()
```

### Backend Features

```python
# Check backend capabilities
info = manager.get_backend_info()

if "actions" in info["features"]:
    # Backend supports interactive actions
    actions = {"ok": "OK"}
    manager.send("info", "Interactive", "This backend supports actions!", actions=actions)
else:
    # Fallback for non-interactive backends
    manager.send("info", "Basic", "This backend shows notifications only")
```

## 💡 Real-World Examples

### Application Notifications

```python
class MyApplication:
    def __init__(self):
        from desktop_notify import NotificationManager
        self.notifier = NotificationManager(
            backend="auto",  # Auto-detect best backend
            icon_set="system",
            timeout=4000
        )
    
    def show_startup_notification(self):
        self.notifier.send(
            "application-startup",
            "MyApp Started", 
            "Application is ready to use"
        )
    
    def show_error_notification(self, error_msg):
        self.notifier.send(
            "error",
            "Application Error",
            f"Error occurred: {error_msg}",
            urgency="critical",
            timeout=0  # Persistent
        )
    
    def show_task_progress(self, task_name, progress):
        self.notifier.send(
            "info",
            f"Task Progress",
            f"{task_name}: {progress}% complete",
            notification_id=f"task_{task_name}"  # Update same notification
        )
```

### Build System Integration

```python
import subprocess
import time

class BuildNotifier:
    def __init__(self):
        from desktop_notify import NotificationManager
        self.notifier = NotificationManager()
    
    def run_build(self):
        # Start notification
        self.notifier.send(
            "compile",
            "Build Started",
            "Compiling project...",
            notification_id="build"
        )
        
        try:
            # Run build command
            result = subprocess.run(["make"], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Success with actions
                actions = {"run": "Run Program", "ok": "OK"}
                selected = self.notifier.send(
                    "success",
                    "Build Successful", 
                    "Ready to run program",
                    notification_id="build",
                    actions=actions
                )
                
                if selected == "run":
                    subprocess.run(["./program"])
            else:
                # Build failed
                self.notifier.send(
                    "error",
                    "Build Failed",
                    f"Error: {result.stderr[:100]}...",
                    notification_id="build",
                    urgency="critical"
                )
                
        except Exception as e:
            self.notifier.send(
                "error",
                "Build System Error", 
                f"Failed to run build: {e}",
                notification_id="build",
                urgency="critical"
            )

# Usage
builder = BuildNotifier()
builder.run_build()
```

### System Monitoring

```python
import psutil
import time

class SystemMonitor:
    def __init__(self):
        from desktop_notify import NotificationManager
        self.notifier = NotificationManager()
        self.last_alert_time = {}
    
    def check_disk_space(self):
        disk_usage = psutil.disk_usage('/')
        percent_used = (disk_usage.used / disk_usage.total) * 100
        
        if percent_used > 90:
            # Critical disk space
            actions = {"cleanup": "Run Cleanup", "ignore": "Ignore"}
            result = self.notifier.send(
                "drive-harddisk",
                "Critical Disk Space",
                f"Disk usage: {percent_used:.1f}% - Only {disk_usage.free // (1024**3)}GB free",
                urgency="critical",
                actions=actions,
                timeout=0  # Persistent
            )
            
            if result == "cleanup":
                # Run cleanup utility
                subprocess.run(["bleachbit"])
                
    def check_memory_usage(self):
        memory = psutil.virtual_memory()
        
        if memory.percent > 85:
            self.notifier.send(
                "memory",
                "High Memory Usage",
                f"RAM usage: {memory.percent:.1f}%",
                urgency="warning"
            )
    
    def monitor_loop(self):
        while True:
            self.check_disk_space()
            self.check_memory_usage()
            time.sleep(300)  # Check every 5 minutes

# Usage
monitor = SystemMonitor()
monitor.monitor_loop()
```

### Voice Recording App

```python
import time
import threading

class VoiceRecorder:
    def __init__(self):
        from desktop_notify import NotificationManager
        self.notifier = NotificationManager()
        self.recording = False
    
    def start_recording(self):
        self.recording = True
        
        # Start recording notification with stop action
        actions = {"stop": "Stop Recording"}
        result = self.notifier.send(
            "microphone",
            "Recording Started",
            "Voice recording in progress...",
            actions=actions,
            notification_id="recording",
            timeout=0  # Persistent until stopped
        )
        
        if result == "stop":
            self.stop_recording()
    
    def stop_recording(self):
        self.recording = False
        filename = f"recording_{int(time.time())}.wav"
        
        # Recording complete with playback actions
        actions = {
            "play": "Play Recording",
            "save": "Save As...",
            "delete": "Delete",
            "ok": "OK"
        }
        
        result = self.notifier.send(
            "audio-x-generic",
            "Recording Complete",
            f"Saved as {filename}",
            actions=actions,
            notification_id="recording"
        )
        
        if result == "play":
            # Play the recording
            subprocess.run(["aplay", filename])
        elif result == "delete":
            # Delete the file
            import os
            os.unlink(filename)
            self.notifier.send("delete", "Deleted", "Recording deleted")

# Usage
recorder = VoiceRecorder()
recorder.start_recording()
```

## 🔧 Troubleshooting

### Common Issues

#### No Notifications Appearing

```python
from desktop_notify import is_notifications_available, get_notification_backend

# Check if notifications work at all
if not is_notifications_available():
    print("❌ Notifications not available")
    print("Install dunst: sudo apt install dunst")
else:
    backend = get_notification_backend()
    print(f"✅ Using backend: {backend}")
```

#### Icons Not Showing

```python
from desktop_notify import NotificationManager

manager = NotificationManager()

# Check icon sets
icon_sets = manager.list_available_icon_sets()
print(f"Available icon sets: {icon_sets}")

# Try different icon types
manager.send("📁", "Test", "Unicode icon")  # Should always work
manager.send("folder", "Test", "Named icon")  # Depends on icon set
```

#### Backend Issues

```python
# Check backend status
manager = NotificationManager()
backends = manager.list_available_backends()
print(f"Available backends: {backends}")

info = manager.get_backend_info()
if info:
    print(f"Current backend: {info['name']}")
    print(f"Available: {info['available']}")
    print(f"Features: {info['features']}")
else:
    print("No backend available")
```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

from desktop_notify import send_notification

# Now all operations will show debug info
send_notification("info", "Debug Test", "Check console for debug info")
```

### Environment Check

```bash
# Check if dunst is running
ps aux | grep dunst

# Check dunstify command
which dunstify

# Test dunstify directly
dunstify "Test" "Direct dunst test"

# Check environment variables
env | grep DESKTOP_NOTIFY
```

### Fallback to Console

```python
# Force console backend for testing
from desktop_notify import NotificationManager

console_manager = NotificationManager(backend="console")
console_manager.send("info", "Console Test", "This should appear in terminal")
```

---

## 📚 Next Steps

- **[API Reference](API_Reference.md)** - Complete API documentation
- **[Configuration Guide](Configuration_Guide.md)** - Detailed configuration options
- **[Examples](Examples/)** - More code examples and use cases

*Desktop Notify v1.0.0 - User Guide*