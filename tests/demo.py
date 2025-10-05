#!/usr/bin/env python3
# ────────────────────────────────────────────────────────────────────────────────
# Desktop Notify Comprehensive Demo Script
# ────────────────────────────────────────────────────────────────────────────────
"""
demo.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 2.0.0

Comprehensive demonstration script showcasing all desktop notification capabilities
including interactive actions, different backends, and icon sets.
"""

import argparse
import time
import logging
import sys
import subprocess
from pathlib import Path
from desktop_notify import send_notification, NotificationManager, is_notifications_available, get_notification_backend


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(name)s - %(levelname)s - %(message)s'
    )


def print_header(title: str, width: int = 60):
    """Print a formatted header."""
    print()
    print("═" * width)
    print(f" {title}")
    print("═" * width)


def print_section(title: str, width: int = 40):
    """Print a formatted section header."""
    print()
    print(f"🔸 {title}")
    print("─" * width)


def check_system():
    """Check system capabilities and display info."""
    print_header("DESKTOP NOTIFY SYSTEM CHECK")
    
    # Check if notifications are available
    available = is_notifications_available()
    backend = get_notification_backend()
    
    if not available:
        print("❌ No notification backends available!")
        print("   Install a notification daemon (e.g., dunst) and try again")
        return False
    
    print(f"✅ Notification system available")
    print(f"   Current backend: {backend}")
    
    # Get detailed backend info
    try:
        manager = NotificationManager()
        backend_info = manager.get_backend_info()
        
        if backend_info:
            print(f"   Backend features: {', '.join(backend_info.get('features', []))}")
            print(f"   Available backends: {', '.join(manager.list_available_backends())}")
            print(f"   Available icon sets: {', '.join(manager.list_available_icon_sets())}")
    except Exception as e:
        print(f"   Warning: Could not get backend details: {e}")
    
    return True


def demo_basic_notifications():
    """Demonstrate basic notification functionality."""
    print_section("Basic Notifications")
    
    # Welcome notification
    send_notification("info", "Demo Started", "Desktop notification demo is running!")
    time.sleep(2)
    
    # Different urgency levels
    print("Testing urgency levels...")
    send_notification("info", "Low Priority", "This is a low priority message", urgency="low")
    time.sleep(1.5)
    
    send_notification("warning", "Normal Priority", "This is a normal priority message", urgency="normal")
    time.sleep(1.5)
    
    send_notification("error", "Critical Priority", "This is a critical priority message!", urgency="critical")
    time.sleep(2)
    
    # Different timeout examples
    print("Testing timeouts...")
    send_notification("info", "Quick Message", "Disappears in 1 second", timeout=1000)
    time.sleep(1.5)
    
    send_notification("info", "Default Timeout", "Uses default timeout")
    time.sleep(2)


def demo_icon_variety():
    """Demonstrate different icon types and sets."""
    print_section("Icon Variety")
    
    # Create manager for icon testing
    manager = NotificationManager()
    
    # System/application icons
    print("Testing system icons...")
    system_icons = [
        ("save", "File Saved", "Document saved successfully"),
        ("folder", "Folder Opened", "Directory contents loaded"),
        ("network", "Network Status", "Connection established"),
        ("settings", "Settings Updated", "Configuration applied"),
        ("user", "User Login", "Welcome back!"),
        ("music", "Now Playing", "♪ Your favorite song ♪"),
        ("camera", "Photo Taken", "Image saved to gallery"),
        ("microphone", "Recording", "Audio recording started"),
    ]
    
    for icon, title, message in system_icons:
        manager.send(icon, title, message)
        time.sleep(1)
    
    # Unicode/emoji icons
    print("Testing unicode icons...")
    unicode_icons = [
        ("📁", "File Manager", "Using folder emoji"),
        ("💾", "Save Operation", "Using floppy disk emoji"),
        ("📷", "Camera App", "Using camera emoji"),
        ("🎵", "Music Player", "Using musical note emoji"),
        ("⚙️", "System Settings", "Using gear emoji"),
    ]
    
    for icon, title, message in unicode_icons:
        manager.send(icon, title, message)
        time.sleep(1)


def demo_notification_updates():
    """Demonstrate notification updates using IDs."""
    print_section("Notification Updates")
    
    manager = NotificationManager()
    
    # Simulate a download process
    print("Simulating download process...")
    download_id = "download-demo"
    
    manager.send("info", "Download Starting", "Preparing download...", notification_id=download_id)
    time.sleep(2)
    
    for progress in [20, 40, 60, 80]:
        manager.send("info", "Download Progress", f"Downloaded {progress}%...", notification_id=download_id)
        time.sleep(1.5)
    
    manager.send("success", "Download Complete", "File downloaded successfully!", notification_id=download_id)
    time.sleep(2)
    
    # Simulate a build process
    print("Simulating build process...")
    build_id = "build-demo"
    
    manager.send("info", "Build Started", "Compiling project...", notification_id=build_id)
    time.sleep(2)
    
    manager.send("info", "Build Progress", "Linking libraries...", notification_id=build_id)
    time.sleep(2)
    
    manager.send("success", "Build Complete", "Project compiled successfully!", notification_id=build_id)
    time.sleep(2)


def demo_interactive_actions():
    """Demonstrate interactive notifications with action buttons."""
    print_section("Interactive Actions")
    
    # Check if current backend supports actions
    manager = NotificationManager()
    backend_info = manager.get_backend_info()
    supports_actions = backend_info and "actions" in backend_info.get("features", [])
    
    if not supports_actions:
        print(f"⚠️  Current backend ({backend_info['name'] if backend_info else 'unknown'}) doesn't support interactive actions")
        print("   Showing fallback notifications instead...")
        manager.send("info", "Interactive Demo", "This backend doesn't support action buttons")
        return
    
    print("✅ Backend supports interactive actions!")
    print()
    print("🔍 INTERACTION INSTRUCTIONS:")
    print("   1. Notifications will appear on your desktop")
    print("   2. RIGHT-CLICK on the notification to open context menu")
    print("   3. Select an action from the context menu")
    print("   4. The demo will show your selection")
    print("   5. If no action is taken, the notification will timeout")
    print()
    print("   NOTE: Your Dunst config now has right-click = context ✅")
    print()
    input("Press ENTER when ready to start interactive demos...")
    
    # Simple yes/no confirmation
    print("Testing basic confirmation...")
    
    def handle_confirmation(action_id):
        if action_id == "yes":
            print("   User confirmed the action")
        elif action_id == "no":
            print("   User declined the action")
    
    confirm_actions = {"yes": "Yes", "no": "No"}
    result = manager.send(
        icon="question",
        title="Confirmation Test",
        message="Do you want to proceed with the demo?",
        actions=confirm_actions,
        action_callback=handle_confirmation,
        timeout=10000
    )
    
    if result == "yes":
        print("   ✅ Proceeding with interactive demos...")
    elif result == "no":
        print("   ❌ User chose not to continue")
        return
    else:
        print("   ⏰ No response (timeout)")
        return
    
    time.sleep(1)
    
    # File download simulation with actions
    print("Testing file download actions...")
    
    def handle_download_action(action_id):
        if action_id == "open":
            print("   📂 Would open downloaded file")
        elif action_id == "folder":
            print("   📁 Would open download folder")
        elif action_id == "share":
            print("   📤 Would open share dialog")
    
    # Simulate download
    manager.send("info", "Download Started", "Downloading document.pdf...")
    time.sleep(2)
    
    download_actions = {
        "open": "Open File",
        "folder": "Open Folder",
        "share": "Share",
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
    
    print(f"   User selected: {result}")
    time.sleep(1)
    
    # Call notification simulation
    print("Testing call notification...")
    
    def handle_call_action(action_id):
        if action_id == "answer":
            print("   📞 Answering call...")
            manager.send("phone", "Call Active", "Connected to demo caller")
        elif action_id == "decline":
            print("   📵 Declining call...")  
            manager.send("phone", "Call Declined", "Call declined")
        elif action_id == "message":
            print("   💬 Sending quick message...")
            manager.send("message", "Message Sent", "Quick reply sent")
    
    call_actions = {
        "answer": "Answer",
        "decline": "Decline", 
        "message": "Send Message"
    }
    
    result = manager.send(
        icon="phone",
        title="Incoming Call",
        message="Demo Caller is calling...",
        actions=call_actions,
        action_callback=handle_call_action,
        urgency="critical",
        timeout=15000
    )
    
    if result is None:
        print("   📵 Call timed out")
        manager.send("phone", "Missed Call", "Missed call from Demo Caller")
    
    time.sleep(1)
    
    # Error handling with retry
    print("Testing error handling with retry...")
    
    def simulate_operation(attempt=1):
        def handle_error_action(action_id):
            if action_id == "retry":
                print(f"   🔄 Retrying operation (attempt {attempt + 1})")
                if attempt < 2:
                    simulate_operation(attempt + 1)
                else:
                    manager.send("success", "Operation Success", "Finally succeeded!")
            elif action_id == "cancel":
                print("   ❌ Operation cancelled by user")
        
        if attempt <= 2:
            error_actions = {"retry": "Retry", "cancel": "Cancel"}
            result = manager.send(
                icon="error",
                title=f"Operation Failed (Attempt {attempt})",
                message="Network timeout occurred. Retry?",
                actions=error_actions,
                action_callback=handle_error_action,
                urgency="critical",
                timeout=10000
            )
        else:
            manager.send("success", "Operation Success", "Completed successfully!")
    
    simulate_operation()
    time.sleep(2)


def demo_real_world_scenarios():
    """Demonstrate real-world usage scenarios."""
    print_section("Real-World Scenarios")
    
    manager = NotificationManager()
    
    # Voice recording workflow
    print("Voice recording workflow...")
    manager.send("microphone", "Recording Started", "Voice recording in progress...")
    time.sleep(3)
    
    filename = "recording_demo.wav"
    
    # Check if actions are supported for post-recording options
    backend_info = manager.get_backend_info()
    if backend_info and "actions" in backend_info.get("features", []):
        def handle_recording_action(action_id):
            if action_id == "play":
                print(f"   🔊 Would play {filename}")
            elif action_id == "save":
                print(f"   💾 Would save {filename} with custom name")
            elif action_id == "delete":
                print(f"   🗑️  Would delete {filename}")
        
        recording_actions = {
            "play": "Play Recording",
            "save": "Save As...",
            "delete": "Delete",
            "ok": "OK"
        }
        
        result = manager.send(
            icon="success",
            title="Recording Complete",
            message=f"Saved as {filename}",
            actions=recording_actions,
            action_callback=handle_recording_action,
            timeout=15000
        )
        
        print(f"   User chose: {result}")
    else:
        manager.send("success", "Recording Complete", f"Saved as {filename}")
    
    time.sleep(2)
    
    # System monitoring alerts
    print("System monitoring alerts...")
    
    # Disk space warning
    manager.send(
        "warning", 
        "Disk Space Warning", 
        "Disk usage: 85% - Consider cleanup",
        urgency="normal"
    )
    time.sleep(2)
    
    # Memory usage alert
    manager.send(
        "warning",
        "High Memory Usage",
        "RAM usage: 92% - Close unused applications",
        urgency="critical"
    )
    time.sleep(2)
    
    # Application workflow
    print("Application workflow...")
    
    # App startup
    manager.send("info", "Application Started", "MyApp is ready to use")
    time.sleep(1)
    
    # Background task
    task_id = "background-task"
    manager.send("info", "Background Task", "Processing data...", notification_id=task_id)
    time.sleep(2)
    
    manager.send("success", "Task Complete", "Data processed successfully", notification_id=task_id)
    time.sleep(2)


def demo_icon_showcase():
    """Showcase all 70 standard icons one by one."""
    print_section("Icon Showcase - All 70 Standard Icons")
    
    manager = NotificationManager()
    
    # The 70 standard icons from breeze.yaml (removing duplicates)
    all_icons = [
        # Status/Dialog (8)
        ('info', 'Information', 'Status and information messages'),
        ('warning', 'Warning', 'Warning messages and alerts'),
        ('error', 'Error', 'Error messages and failures'),
        ('success', 'Success', 'Success confirmations'),
        ('question', 'Question', 'Help and questions'),
        ('alert', 'Alert', 'Important alerts'),
        ('ok', 'OK', 'Confirmation and approval'),
        ('valid', 'Valid', 'Validation success'),
        
        # Actions (19)
        ('save', 'Save', 'Save documents and files'),
        ('open', 'Open', 'Open files and folders'),
        ('new', 'New', 'Create new items'),
        ('copy', 'Copy', 'Copy to clipboard'),
        ('cut', 'Cut', 'Cut to clipboard'),
        ('paste', 'Paste', 'Paste from clipboard'),
        ('undo', 'Undo', 'Undo last action'),
        ('redo', 'Redo', 'Redo last action'),
        ('find', 'Find', 'Search and find'),
        ('delete', 'Delete', 'Delete items'),
        ('clear', 'Clear', 'Clear content'),
        ('back', 'Back', 'Navigate backwards'),
        ('forward', 'Forward', 'Navigate forwards'),
        ('up', 'Up', 'Navigate up'),
        ('down', 'Down', 'Navigate down'),
        ('home', 'Home', 'Go to home'),
        ('refresh', 'Refresh', 'Refresh content'),
        ('edit', 'Edit', 'Edit content'),
        ('close', 'Close', 'Close windows'),
        
        # Media (8)
        ('play', 'Play', 'Play media'),
        ('pause', 'Pause', 'Pause playback'),
        ('stop', 'Stop', 'Stop playback'),
        ('next', 'Next', 'Next track'),
        ('previous', 'Previous', 'Previous track'),
        ('record', 'Record', 'Record audio/video'),
        ('music', 'Music', 'Music files'),
        ('video', 'Video', 'Video files'),
        
        # Devices (8)
        ('microphone', 'Microphone', 'Audio input device'),
        ('camera', 'Camera', 'Camera device'),
        ('printer', 'Printer', 'Print documents'),
        ('scanner', 'Scanner', 'Scan documents'),
        ('speaker', 'Speaker', 'Audio output'),
        ('headphones', 'Headphones', 'Audio headphones'),
        ('battery', 'Battery', 'Battery status'),
        ('mic', 'Mic', 'Microphone (short)'),
        
        # System (11)
        ('settings', 'Settings', 'System settings'),
        ('user', 'User', 'User account'),
        ('users', 'Users', 'Multiple users'),
        ('network', 'Network', 'Network connections'),
        ('wifi', 'WiFi', 'Wireless network'),
        ('bluetooth', 'Bluetooth', 'Bluetooth connectivity'),
        ('power', 'Power', 'System power'),
        ('logout', 'Logout', 'Log out of system'),
        ('lock', 'Lock', 'Lock screen'),
        ('config', 'Config', 'Configuration'),
        ('preferences', 'Preferences', 'User preferences'),
        
        # Applications (10)
        ('browser', 'Browser', 'Web browser'),
        ('mail', 'Mail', 'Email application'),
        ('editor', 'Editor', 'Text editor'),
        ('terminal', 'Terminal', 'Command terminal'),
        ('calculator', 'Calculator', 'Calculator app'),
        ('folder', 'Folder', 'File folders'),
        ('file', 'File', 'Generic files'),
        ('document', 'Document', 'Text documents'),
        ('image', 'Image', 'Image files'),
        ('archive', 'Archive', 'Archive files'),
        
        # Status/Loading (5)
        ('load', 'Load', 'Loading content'),
        ('loading', 'Loading', 'Loading in progress'),
        ('process', 'Process', 'Processing data'),
        ('working', 'Working', 'Work in progress'),
        ('busy', 'Busy', 'System busy'),
    ]
    
    print(f"Showcasing {len(all_icons)} standard icons...")
    print("Each icon will be displayed for 4 seconds.")
    print("Press Ctrl+C to interrupt the showcase.")
    print()
    
    input("Press ENTER to start the icon showcase...")
    
    for i, (icon_name, title, description) in enumerate(all_icons, 1):
        print(f"[{i:2d}/{len(all_icons)}] Showing: {icon_name} - {title}")
        
        try:
            manager.send(
                icon=icon_name,
                title=f"{title} ({icon_name})",
                message=description,
                timeout=4000
            )
            
            # Wait 4 seconds before next icon
            time.sleep(4)
            
        except Exception as e:
            print(f"   ⚠️  Error showing {icon_name}: {e}")
            time.sleep(1)
    
    print(f"\n🎉 Showcase complete! Displayed {len(all_icons)} icons.")


def demo_icon_sets_and_all_or_nothing():
    """Demonstrate icon sets and all-or-nothing functionality."""
    print_section("Icon Sets & All-or-Nothing Mode")
    
    manager = NotificationManager()
    icon_manager = manager.icon_manager
    
    if not icon_manager:
        print("❌ Could not get icon manager")
        return
    
    print(f"Available icon sets: {', '.join(icon_manager.list_available_sets())}")
    print(f"Current icon set: {icon_manager.get_active_icon_set()}")
    print(f"All-or-nothing mode: {icon_manager.get_all_or_nothing_mode()}")
    
    # Show current icon resolution for some icons
    test_icons = ['info', 'warning', 'error', 'save', 'folder']
    print(f"\nCurrent icon resolution (using {icon_manager.get_active_icon_set()}):")
    for icon in test_icons:
        resolved = icon_manager.get_icon(icon)
        if resolved:
            if resolved.startswith('/'):
                print(f"  {icon}: {Path(resolved).name}")
            else:
                print(f"  {icon}: {resolved}")
        else:
            print(f"  {icon}: NOT FOUND")
    
    # Demonstrate switching icon sets
    available_sets = icon_manager.list_available_sets()
    
    if 'material-complete' in available_sets:
        print("\nSwitching to material-complete icon set...")
        icon_manager.set_active_icon_set('material-complete')
        manager.send("info", "Icon Set Changed", "Now using Material Design Complete icons")
        time.sleep(2)
        
        print(f"Current icon set: {icon_manager.get_active_icon_set()}")
        for icon in test_icons:
            resolved = icon_manager.get_icon(icon)
            if resolved:
                print(f"  {icon}: {Path(resolved).name if resolved.startswith('/') else resolved}")
    
    if 'minimal' in available_sets:
        print("\nSwitching to minimal icon set...")
        icon_manager.set_active_icon_set('minimal')
        manager.send("info", "Icon Set Changed", "Now using minimal unicode icons")
        time.sleep(2)
        
        print(f"Current icon set: {icon_manager.get_active_icon_set()}")
        for icon in test_icons:
            resolved = icon_manager.get_icon(icon)
            if resolved:
                print(f"  {icon}: {resolved}")
    
    # Demonstrate all-or-nothing mode
    print("\nDemonstrating all-or-nothing mode...")
    
    # First disable all-or-nothing to see mixed behavior
    print("Disabling all-or-nothing mode...")
    icon_manager.set_all_or_nothing_mode(False)
    manager.send("info", "All-or-Nothing Disabled", "May use mixed icon sources")
    time.sleep(2)
    
    # Re-enable all-or-nothing
    print("Re-enabling all-or-nothing mode...")
    icon_manager.set_all_or_nothing_mode(True)
    manager.send("success", "All-or-Nothing Enabled", "Consistent icon style guaranteed")
    time.sleep(2)
    
    print(f"Final icon set: {icon_manager.get_active_icon_set()}")


def demo_backend_features():
    """Demonstrate backend-specific features."""
    print_section("Backend Features")
    
    manager = NotificationManager()
    backend_info = manager.get_backend_info()
    
    if not backend_info:
        print("❌ Could not get backend information")
        return
    
    print(f"Current backend: {backend_info['name']}")
    print(f"Backend priority: {backend_info['priority']}")
    print(f"Features: {', '.join(backend_info['features'])}")
    
    # Test backend-specific features
    if "markup" in backend_info['features']:
        print("Testing markup support...")
        manager.send(
            "info",
            "Markup Test", 
            "<b>Bold text</b> and <i>italic text</i>",
            markup=True
        )
        time.sleep(2)
    
    if "persistent" in backend_info['features']:
        print("Testing persistent notification...")
        manager.send(
            "warning",
            "Persistent Alert",
            "This notification requires manual dismissal",
            timeout=0
        )
        time.sleep(2)
    
    # Test different backends if available
    available_backends = manager.list_available_backends()
    print(f"Available backends: {', '.join(available_backends)}")
    
    if len(available_backends) > 1:
        print("Testing backend switching...")
        original_backend = backend_info['name']
        
        for backend_name in available_backends:
            if backend_name != original_backend:
                if manager.switch_backend(backend_name):
                    print(f"   Switched to {backend_name}")
                    manager.send("info", f"{backend_name.title()} Backend", "Testing alternate backend")
                    time.sleep(2)
                    break
        
        # Switch back
        if manager.switch_backend(original_backend):
            print(f"   Switched back to {original_backend}")


def run_quick_test():
    """Run a quick test of basic functionality."""
    print_header("QUICK TEST MODE")
    
    if not check_system():
        return False
    
    print("Running quick functionality test...")
    
    # Basic notification
    send_notification("info", "Quick Test", "Testing basic notification...")
    time.sleep(1)
    
    # Test with manager
    manager = NotificationManager()
    manager.send("success", "Test Complete", "Quick test passed!")
    
    print("✅ Quick test completed successfully")
    return True


def run_full_demo():
    """Run the complete demo suite."""
    print_header("DESKTOP NOTIFY COMPREHENSIVE DEMO")
    
    if not check_system():
        return False
    
    try:
        demo_basic_notifications()
        demo_icon_variety()
        demo_icon_sets_and_all_or_nothing()
        demo_notification_updates()
        demo_interactive_actions()
        demo_real_world_scenarios()
        demo_backend_features()
        
        # Final completion message
        print_header("DEMO COMPLETE")
        
        manager = NotificationManager()
        backend_info = manager.get_backend_info()
        
        # Final notification with actions if supported
        if backend_info and "actions" in backend_info.get("features", []):
            def handle_completion(action_id):
                if action_id == "again":
                    print("   🔄 User wants to run demo again")
                elif action_id == "docs":
                    print("   📚 User wants to see documentation")
                    docs_path = Path(__file__).parent.parent / "docs"
                    if docs_path.exists():
                        print(f"   Documentation available at: {docs_path}")
            
            completion_actions = {
                "again": "Run Again",
                "docs": "View Docs", 
                "ok": "Finish"
            }
            
            result = manager.send(
                icon="success",
                title="Demo Complete!",
                message="Desktop notification demo finished successfully",
                actions=completion_actions,
                action_callback=handle_completion,
                timeout=15000
            )
            
            print(f"User selected: {result}")
        else:
            manager.send("success", "Demo Complete!", "All features demonstrated successfully")
        
        print("✨ All demo sections completed successfully!")
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        send_notification("warning", "Demo Interrupted", "Demo stopped by user")
        return False
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        send_notification("error", "Demo Error", f"Demo failed: {e}")
        return False


def run_interactive_only():
    """Run only the interactive actions demo."""
    print_header("INTERACTIVE ACTIONS DEMO")
    
    if not check_system():
        return False
    
    try:
        demo_interactive_actions()
        print("✨ Interactive demo completed!")
        return True
    except KeyboardInterrupt:
        print("\n\n⚠️  Interactive demo interrupted")
        return False
    except Exception as e:
        print(f"\n\n❌ Error during interactive demo: {e}")
        return False


def run_icon_demo():
    """Run only the icon sets and all-or-nothing demo."""
    print_header("ICON SETS & ALL-OR-NOTHING DEMO")
    
    if not check_system():
        return False
    
    try:
        demo_icon_sets_and_all_or_nothing()
        print("✨ Icon demo completed!")
        return True
    except KeyboardInterrupt:
        print("\n\n⚠️  Icon demo interrupted")
        return False
    except Exception as e:
        print(f"\n\n❌ Error during icon demo: {e}")
        return False


def run_icon_showcase():
    """Run icon showcase showing all 70 standard icons."""
    print_header("ICON SHOWCASE - ALL 70 STANDARD ICONS")
    
    if not check_system():
        return False
    
    try:
        demo_icon_showcase()
        print("✨ Icon showcase completed!")
        return True
    except KeyboardInterrupt:
        print("\n\n⚠️  Icon showcase interrupted")
        return False
    except Exception as e:
        print(f"\n\n❌ Error during icon showcase: {e}")
        return False


def main():
    """Main demo function with command-line argument handling."""
    parser = argparse.ArgumentParser(
        description="Desktop Notify Comprehensive Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python demo.py                         # Run full demo
  python demo.py --quick                 # Quick functionality test
  python demo.py --interactive           # Interactive actions only
  python demo.py --icons                 # Icon sets and all-or-nothing demo
  python demo.py --showcase              # Showcase all 70 standard icons
  python demo.py --verbose               # Full demo with debug output
  python demo.py --backend console       # Force specific backend
  python demo.py --icon-set material-complete  # Force material-complete icons
        """
    )
    
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Run quick test instead of full demo"
    )
    
    parser.add_argument(
        "--interactive", "-i", 
        action="store_true",
        help="Run only interactive actions demo"
    )
    
    parser.add_argument(
        "--icons", 
        action="store_true",
        help="Run only icon sets and all-or-nothing demo"
    )
    
    parser.add_argument(
        "--showcase", 
        action="store_true",
        help="Run icon showcase displaying all 70 standard icons"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true", 
        help="Enable verbose/debug output"
    )
    
    parser.add_argument(
        "--backend", "-b",
        type=str,
        help="Force specific backend (dunst, console, auto)"
    )
    
    parser.add_argument(
        "--icon-set", "-s",
        type=str,
        help="Force specific icon set (system, material, material-complete, minimal, auto)"
    )
    
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        help="Default timeout in milliseconds"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Configure manager if specific options provided
    manager_kwargs = {}
    if args.backend:
        manager_kwargs['backend'] = args.backend
    if args.icon_set:
        manager_kwargs['icon_set'] = args.icon_set
    if args.timeout:
        manager_kwargs['timeout'] = args.timeout
    
    # Apply global configuration if provided
    if manager_kwargs:
        try:
            # Create a test manager to validate options
            test_manager = NotificationManager(**manager_kwargs)
            print(f"Using custom configuration: {manager_kwargs}")
        except Exception as e:
            print(f"❌ Invalid configuration: {e}")
            return 1
    
    # Run appropriate demo mode
    success = True
    
    if args.quick:
        success = run_quick_test()
    elif args.interactive:
        success = run_interactive_only()
    elif args.icons:
        success = run_icon_demo()
    elif args.showcase:
        success = run_icon_showcase()
    else:
        success = run_full_demo()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())