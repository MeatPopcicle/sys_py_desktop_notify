#!/usr/bin/env python3
"""
Example: Interactive Actions with Different Mouse Clicks

This demonstrates the correct way to use actions with dunst notifications.
"""

from desktop_notify import send_notification
import time

def example_1_default_action_only():
    """Example 1: Single action triggered by left-click."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Default Action (Left-Click Only)")
    print("="*60)
    print("📌 Notification will appear")
    print("📌 LEFT-CLICK to accept")
    print("📌 MIDDLE-CLICK to dismiss")
    print()

    result = send_notification(
        icon="info",
        title="Quick Action",
        message="Click to accept (or middle-click to dismiss)",
        actions={
            "default": "Accept"  # Triggered by left-click
        },
        timeout=15000
    )

    if result == "default":
        print("✅ You clicked Accept!")
    else:
        print("⏰ Dismissed or timed out")

def example_2_context_menu():
    """Example 2: Multiple actions in right-click context menu."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Context Menu (Right-Click)")
    print("="*60)
    print("📌 Notification will appear")
    print("📌 RIGHT-CLICK to see menu with options")
    print("📌 MIDDLE-CLICK to dismiss")
    print()

    result = send_notification(
        icon="question",
        title="Make a Choice",
        message="Right-click to see options",
        actions={
            "yes": "Yes",
            "no": "No",
            "maybe": "Maybe Later"
        },
        timeout=15000
    )

    if result == "yes":
        print("✅ You selected: Yes")
    elif result == "no":
        print("❌ You selected: No")
    elif result == "maybe":
        print("🤔 You selected: Maybe Later")
    else:
        print("⏰ Dismissed or timed out")

def example_3_both_clicks():
    """Example 3: Default action + context menu (best of both worlds)."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Both Left-Click and Right-Click")
    print("="*60)
    print("📌 Notification will appear")
    print("📌 LEFT-CLICK for quick accept")
    print("📌 RIGHT-CLICK for more options")
    print("📌 MIDDLE-CLICK to dismiss")
    print()

    result = send_notification(
        icon="question",
        title="File Download Complete",
        message="Choose an action (left-click to open, right-click for more)",
        actions={
            "default": "Open File",      # Left-click: Quick action
            "folder": "Open Folder",      # Right-click menu
            "delete": "Delete File"       # Right-click menu
        },
        timeout=15000
    )

    if result == "default":
        print("📂 Opening file...")
    elif result == "folder":
        print("📁 Opening folder...")
    elif result == "delete":
        print("🗑️  Deleting file...")
    else:
        print("⏰ Dismissed or timed out")

def example_4_confirmation_dialog():
    """Example 4: Confirmation dialog with clear actions."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Confirmation Dialog")
    print("="*60)
    print("📌 Typical use case: Quick yes/no decision")
    print("📌 LEFT-CLICK for quick 'Yes'")
    print("📌 RIGHT-CLICK for 'No' or 'Cancel'")
    print()

    result = send_notification(
        icon="warning",
        title="Confirm Action",
        message="Delete all temporary files?",
        actions={
            "default": "Yes, Delete",  # Left-click: Quick yes
            "no": "No, Keep Files",    # Right-click: Explicit no
            "cancel": "Cancel"          # Right-click: Cancel operation
        },
        timeout=15000,
        urgency="critical"
    )

    if result == "default":
        print("🗑️  Deleting files...")
    elif result == "no":
        print("✋ Keeping files")
    elif result == "cancel":
        print("❌ Cancelled")
    else:
        print("⏰ Dismissed or timed out")

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║  Interactive Notification Examples                        ║
║  Demonstrating mouse click behaviors                      ║
╚════════════════════════════════════════════════════════════╝

Key Concepts:
  • "default" action → LEFT-CLICK triggers immediately
  • Other actions → RIGHT-CLICK shows context menu
  • MIDDLE-CLICK → Always dismisses notification

""")

    examples = [
        ("Example 1: Default Action Only", example_1_default_action_only),
        ("Example 2: Context Menu", example_2_context_menu),
        ("Example 3: Both Clicks", example_3_both_clicks),
        ("Example 4: Confirmation Dialog", example_4_confirmation_dialog)
    ]

    for i, (name, func) in enumerate(examples, 1):
        print(f"\n{'─'*60}")
        print(f"Running: {name}")
        print(f"{'─'*60}")

        func()
        time.sleep(2)

    print("\n" + "="*60)
    print("Examples Complete!")
    print("="*60)
    print("""
Summary:
  ✅ Use "default" key for left-click actions
  ✅ Use any other key for right-click menu items
  ✅ Combine both for maximum flexibility

See docs/Dunst_Action_Behavior.md for more details.
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted")
        exit(130)
