#!/usr/bin/env python3
# ────────────────────────────────────────────────────────────────────────────────
# Desktop Notify Demo Script
# ────────────────────────────────────────────────────────────────────────────────
"""
demo.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Demonstration script showcasing desktop notification capabilities.
"""

import time
import logging
from desktop_notify import send_notification, NotificationManager, is_notifications_available

# Setup logging to see debug information
# Note: The desktop_notify config will override the log level for its own loggers
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    """
    ///////////////////////////////////////////////////////////////////
    DESKTOP NOTIFY DEMO
    ▄▄▄▄ ▄▄▄▄ ▄▄▄▄▄ ▄▄▄  
    █▄▄▄ █▄▄▄ █▄▄▄▄ █▀▀  
    █▄▄▄ █▄▄▄ █▄▄▄▄ █▄▄  
    ///////////////////////////////////////////////////////////////////
    Demonstration of desktop notification features.
    """
    
    print("🔔 Desktop Notify Demo Starting...")
    print("═" * 50)
    
    # ─────────────────────────────────────────────────────────────────
    # Check availability
    # ─────────────────────────────────────────────────────────────────
    if not is_notifications_available():
        print("❌ No notification backends available!")
        return
    
    print("✅ Notification system available")
    
    # Test our logging configuration
    test_logger = logging.getLogger('desktop_notify')
    test_logger.info("🔧 Desktop-notify logging is configured and working")
    print()
    
    # ─────────────────────────────────────────────────────────────────
    # Basic notification examples
    # ─────────────────────────────────────────────────────────────────
    print("📢 Basic Notifications:")
    print("-" * 30)
    
    # Simple notification
    send_notification("info", "Welcome", "Desktop notification system is working!")
    time.sleep(2)
    
    # Status notifications with different urgency levels
    send_notification("warning", "Process Starting", "Initializing background task...", urgency="low")
    time.sleep(2)
    
    send_notification("error", "Critical Alert", "System requires immediate attention!", urgency="critical")
    time.sleep(2)
    
    # ─────────────────────────────────────────────────────────────────
    # Advanced NotificationManager examples
    # ─────────────────────────────────────────────────────────────────
    print("⚙️ Advanced Notification Manager:")
    print("-" * 35)
    
    # Create custom manager with specific settings
    manager = NotificationManager(
        backend="auto",
        timeout=5000,
        urgency="normal"
    )
    
    # Show manager info
    backend_info = manager.get_backend_info()
    if backend_info:
        print(f"Using backend: {backend_info['name']}")
        print(f"Available backends: {manager.list_available_backends()}")
        print(f"Available icon sets: {manager.list_available_icon_sets()}")
        print()
    
    # ─────────────────────────────────────────────────────────────────
    # Icon variety demonstration
    # ─────────────────────────────────────────────────────────────────
    print("🎨 Icon Variety:")
    print("-" * 15)
    
    icon_demos = [
        ("mic", "Recording Started", "Audio recording in progress"),
        ("camera", "Photo Taken", "Image saved to gallery"),
        ("save", "File Saved", "Document saved successfully"),
        ("load", "Processing", "Loading data..."),
        ("settings", "Configuration", "Settings updated"),
        ("user", "User Login", "Welcome back!"),
        ("network", "Connection", "Network status changed"),
        ("music", "Now Playing", "♪ Your Favorite Song ♪"),
    ]
    
    for icon, title, message in icon_demos:
        manager.send(icon, title, message)
        time.sleep(1.5)
    
    # ─────────────────────────────────────────────────────────────────
    # Notification updates (same ID)
    # ─────────────────────────────────────────────────────────────────
    print("🔄 Notification Updates:")
    print("-" * 25)
    
    # Progress simulation
    progress_id = "progress-demo"
    
    manager.send("load", "Download Starting", "Preparing download...", notification_id=progress_id)
    time.sleep(2)
    
    manager.send("load", "Download Progress", "Downloaded 25%...", notification_id=progress_id)
    time.sleep(2)
    
    manager.send("load", "Download Progress", "Downloaded 75%...", notification_id=progress_id)
    time.sleep(2)
    
    manager.send("valid", "Download Complete", "File downloaded successfully!", notification_id=progress_id)
    time.sleep(2)
    
    # ─────────────────────────────────────────────────────────────────
    # Different timeout examples
    # ─────────────────────────────────────────────────────────────────
    print("⏱️ Timeout Examples:")
    print("-" * 20)
    
    # Quick notification (1 second)
    manager.send("info", "Quick Message", "This disappears quickly", timeout=1000)
    time.sleep(1.5)
    
    # Persistent notification (requires manual dismissal on some systems)
    manager.send("warning", "Persistent Alert", "This notification stays visible", timeout=0)
    time.sleep(2)
    
    # ─────────────────────────────────────────────────────────────────
    # Use case examples
    # ─────────────────────────────────────────────────────────────────
    print("💼 Use Case Examples:")
    print("-" * 22)
    
    # Voice recorder simulation
    manager.send("mic", "Recording Started", "Voice recording in progress")
    time.sleep(3)
    manager.send("save", "Recording Saved", "Audio file saved as recording_001.wav")
    time.sleep(2)
    
    # Build system simulation
    build_id = "build-process"
    manager.send("load", "Build Started", "Compiling project...", notification_id=build_id)
    time.sleep(3)
    manager.send("valid", "Build Success", "Project compiled successfully", notification_id=build_id)
    time.sleep(2)
    
    # System monitoring simulation
    manager.send("warning", "Disk Space", "Disk usage: 85% - Consider cleanup", urgency="normal")
    time.sleep(2)
    
    # Final message
    print("✨ Demo Complete!")
    print("═" * 50)
    
    manager.send("info", "Demo Complete", "Desktop notification demo finished successfully!")

if __name__ == "__main__":
    main()