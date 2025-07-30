#!/usr/bin/env python3
"""
Desktop Notify - Interactive Actions Examples

Demonstrates how to create interactive notifications with action buttons
and handle user responses.
"""

import time
import subprocess
from desktop_notify import send_notification, NotificationManager


def basic_actions_example():
    """Simple yes/no action example."""
    print("📋 Basic Actions Example")
    print("=" * 50)
    
    # Define actions
    actions = {"yes": "Yes", "no": "No"}
    
    # Send interactive notification
    result = send_notification(
        icon="question",
        title="Confirmation Required",
        message="Do you want to proceed with the operation?",
        actions=actions,
        timeout=10000  # 10 seconds
    )
    
    # Handle response
    if result == "yes":
        print("✅ User confirmed the operation")
        send_notification("success", "Confirmed", "Operation proceeding...")
    elif result == "no":
        print("❌ User cancelled the operation")
        send_notification("info", "Cancelled", "Operation cancelled")
    else:
        print("⏰ User didn't respond (timeout)")
        send_notification("warning", "Timeout", "No response received")
    
    print()


def file_download_example():
    """File download with action buttons."""
    print("📥 File Download Example")
    print("=" * 50)
    
    def handle_download_action(action_id):
        """Handle download completion actions."""
        if action_id == "open":
            print("📂 Opening file...")
            # In real app: subprocess.run(["xdg-open", "/path/to/file.pdf"])
        elif action_id == "folder":
            print("📁 Opening download folder...")
            # In real app: subprocess.run(["xdg-open", "/downloads/"])
        elif action_id == "share":
            print("📤 Sharing file...")
            # In real app: open share dialog
    
    # Simulate download progress
    send_notification("download", "Download Started", "Downloading document.pdf...")
    
    # Simulate download time
    print("Simulating download...")
    time.sleep(2)
    
    # Download complete with actions
    download_actions = {
        "open": "Open File",
        "folder": "Open Folder", 
        "share": "Share",
        "dismiss": "Dismiss"
    }
    
    result = send_notification(
        icon="success",
        title="Download Complete",
        message="document.pdf has been downloaded successfully",
        actions=download_actions,
        action_callback=handle_download_action,
        timeout=15000
    )
    
    print(f"User selected: {result}")
    print()


def call_notification_example():
    """Incoming call notification with answer/decline."""
    print("📞 Call Notification Example")
    print("=" * 50)
    
    def handle_call_action(action_id):
        """Handle call actions."""
        if action_id == "answer":
            print("📞 Answering call...")
            # Show call answered notification
            send_notification("phone", "Call Active", "Connected to John Doe")
        elif action_id == "decline":
            print("📵 Declining call...")
            # Show call declined notification  
            send_notification("phone", "Call Declined", "Call from John Doe declined")
        elif action_id == "message":
            print("💬 Sending quick message...")
            # Show message sent notification
            send_notification("message", "Message Sent", "Quick reply sent to John Doe")
    
    # Incoming call with multiple actions
    call_actions = {
        "answer": "Answer",
        "decline": "Decline",
        "message": "Send Message"
    }
    
    result = send_notification(
        icon="phone",
        title="Incoming Call",
        message="John Doe is calling...",
        actions=call_actions,
        action_callback=handle_call_action,
        urgency="critical",
        timeout=30000  # 30 seconds for call timeout
    )
    
    if result is None:
        print("📵 Call timed out")
        send_notification("phone", "Missed Call", "Missed call from John Doe")
    
    print()


def backup_confirmation_example():
    """Backup operation with confirmation."""
    print("💾 Backup Confirmation Example")
    print("=" * 50)
    
    def perform_backup():
        """Simulate backup operation."""
        print("Starting backup process...")
        
        # Backup in progress
        send_notification(
            "info",
            "Backup In Progress",
            "Backing up files to cloud storage...",
            notification_id="backup"
        )
        
        # Simulate backup time
        time.sleep(3)
        
        # Backup complete
        send_notification(
            "success",
            "Backup Complete",
            "All files successfully backed up",
            notification_id="backup"
        )
    
    # Ask for confirmation
    backup_actions = {"yes": "Start Backup", "no": "Cancel"}
    
    result = send_notification(
        icon="question",
        title="Backup Confirmation",
        message="Backup all files to cloud storage? This may take several minutes.",
        actions=backup_actions,
        timeout=15000
    )
    
    if result == "yes":
        print("✅ User confirmed backup")
        perform_backup()
    else:
        print("❌ Backup cancelled")
        send_notification("info", "Backup Cancelled", "No backup performed")
    
    print()


def multi_step_workflow_example():
    """Multi-step workflow with actions."""
    print("🔄 Multi-Step Workflow Example")
    print("=" * 50)
    
    def step_one():
        """First step of workflow."""
        actions = {"continue": "Continue", "cancel": "Cancel"}
        
        result = send_notification(
            icon="info",
            title="Step 1 of 3",
            message="Initialize project setup?",
            actions=actions,
            timeout=10000
        )
        
        if result == "continue":
            return step_two()
        else:
            send_notification("info", "Cancelled", "Workflow cancelled at step 1")
            return False
    
    def step_two():
        """Second step of workflow."""
        actions = {"continue": "Continue", "back": "Go Back", "cancel": "Cancel"}
        
        result = send_notification(
            icon="info",
            title="Step 2 of 3",
            message="Configure project settings?",
            actions=actions,
            timeout=10000
        )
        
        if result == "continue":
            return step_three()
        elif result == "back":
            return step_one()
        else:
            send_notification("info", "Cancelled", "Workflow cancelled at step 2")
            return False
    
    def step_three():
        """Final step of workflow."""
        actions = {"finish": "Finish", "back": "Go Back", "cancel": "Cancel"}
        
        result = send_notification(
            icon="question",
            title="Step 3 of 3",
            message="Ready to finalize project setup?",
            actions=actions,
            timeout=10000
        )
        
        if result == "finish":
            send_notification("success", "Complete", "Project setup finished!")
            return True
        elif result == "back":
            return step_two()
        else:
            send_notification("info", "Cancelled", "Workflow cancelled at step 3")
            return False
    
    # Start workflow
    success = step_one()
    if success:
        print("✅ Workflow completed successfully")
    else:
        print("❌ Workflow was cancelled")
    
    print()


def error_handling_example():
    """Error handling with retry actions."""
    print("⚠️ Error Handling Example")
    print("=" * 50)
    
    def simulate_operation(attempt=1):
        """Simulate an operation that might fail."""
        print(f"Attempting operation (attempt {attempt})...")
        
        # Simulate failure on first two attempts
        if attempt < 3:
            error_actions = {
                "retry": "Retry",
                "details": "Show Details",
                "cancel": "Cancel"
            }
            
            result = send_notification(
                icon="error",
                title=f"Operation Failed (Attempt {attempt})",
                message="Network connection failed. Would you like to retry?",
                actions=error_actions,
                urgency="critical",
                timeout=15000
            )
            
            if result == "retry":
                time.sleep(1)
                return simulate_operation(attempt + 1)
            elif result == "details":
                send_notification(
                    "info",
                    "Error Details",
                    "Connection timeout after 30 seconds. Check network settings.",
                    timeout=10000
                )
                return simulate_operation(attempt)  # Show options again
            else:
                send_notification("info", "Cancelled", "Operation cancelled by user")
                return False
        else:
            # Success on third attempt
            send_notification("success", "Success", "Operation completed successfully!")
            return True
    
    success = simulate_operation()
    if success:
        print("✅ Operation eventually succeeded")
    else:
        print("❌ Operation was cancelled")
    
    print()


def advanced_notification_manager_example():
    """Advanced example using NotificationManager."""
    print("🔧 Advanced NotificationManager Example")
    print("=" * 50)
    
    # Create manager with specific configuration
    manager = NotificationManager(
        backend="auto",
        icon_set="material",
        timeout=8000
    )
    
    # Check if actions are supported
    backend_info = manager.get_backend_info()
    supports_actions = "actions" in backend_info.get("features", [])
    
    print(f"Current backend: {backend_info['name']}")
    print(f"Supports actions: {supports_actions}")
    
    if supports_actions:
        # Interactive notification
        def handle_settings_action(action_id):
            if action_id == "open":
                print("🔧 Opening settings...")
            elif action_id == "restart":
                print("🔄 Restarting application...")
                
        settings_actions = {"open": "Open Settings", "restart": "Restart App", "ok": "OK"}
        
        result = manager.send(
            icon="settings",
            title="Configuration Updated",
            message="New settings have been applied. Restart recommended.",
            actions=settings_actions,
            action_callback=handle_settings_action
        )
        
        print(f"User response: {result}")
    else:
        # Fallback for backends without action support
        manager.send(
            icon="settings",
            title="Configuration Updated", 
            message="New settings applied. Please restart the application.",
            urgency="normal"
        )
        print("Sent non-interactive notification (backend doesn't support actions)")
    
    print()


def main():
    """Run all interactive action examples."""
    print("🔔 Desktop Notify - Interactive Actions Examples")
    print("=" * 60)
    print()
    
    # Check if notifications are available
    from desktop_notify import is_notifications_available
    if not is_notifications_available():
        print("❌ Desktop notifications are not available on this system")
        print("Please install a notification daemon (e.g., dunst) and try again")
        return
    
    # Introduction notification
    send_notification(
        "info",
        "Interactive Examples",
        "Starting interactive notification examples...",
        timeout=3000
    )
    
    try:
        # Run examples
        basic_actions_example()
        time.sleep(1)
        
        file_download_example()
        time.sleep(1)
        
        call_notification_example()
        time.sleep(1)
        
        backup_confirmation_example()
        time.sleep(1)
        
        multi_step_workflow_example()
        time.sleep(1)
        
        error_handling_example()
        time.sleep(1)
        
        advanced_notification_manager_example()
        
        # Completion notification
        send_notification(
            "success",
            "Examples Complete",
            "All interactive notification examples finished!",
            timeout=5000
        )
        
        print("✅ All examples completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Examples interrupted by user")
        send_notification("warning", "Interrupted", "Examples stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error running examples: {e}")
        send_notification("error", "Error", f"Example failed: {e}")


if __name__ == "__main__":
    main()