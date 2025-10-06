#!/usr/bin/env python3
"""
Test different click behaviors for dunst actions.

This test helps understand and verify:
- Left-click behavior (should trigger default action)
- Right-click behavior (should show context menu)
- Middle-click behavior (should dismiss)
"""

import subprocess
import time

def test_default_action():
    """Test default action (left-click)."""
    print("\n" + "="*60)
    print("TEST 1: Default Action (Left-Click)")
    print("="*60)
    print("📌 A notification will appear")
    print("📌 LEFT-CLICK directly on the notification")
    print("📌 It should trigger the 'default' action immediately")
    print("📌 Timeout: 15 seconds")

    input("\nPress ENTER to start...")

    result = subprocess.run([
        "dunstify",
        "-A", "default,Accept",  # default = left-click action
        "-t", "15000",
        "Left-Click Test",
        "Click this notification (left-click)"
    ], capture_output=True, text=True, timeout=20)

    print(f"\nReturn code: {result.returncode}")
    print(f"Action selected: '{result.stdout.strip()}'")

    if result.returncode == 0 and result.stdout.strip() == "default":
        print("✅ SUCCESS: Left-click triggered default action!")
        return True
    elif result.returncode == 1:
        print("⏰ TIMEOUT: No action taken")
        return False
    elif result.returncode == 2:
        print("❌ DISMISSED: Notification was dismissed")
        return False
    else:
        print(f"❓ UNEXPECTED: Return code {result.returncode}")
        return False

def test_context_menu():
    """Test context menu (right-click)."""
    print("\n" + "="*60)
    print("TEST 2: Context Menu (Right-Click)")
    print("="*60)
    print("📌 A notification will appear")
    print("📌 RIGHT-CLICK on the notification")
    print("📌 A context menu should appear with 3 options")
    print("📌 Select any option")
    print("📌 Timeout: 15 seconds")

    input("\nPress ENTER to start...")

    result = subprocess.run([
        "dunstify",
        "-A", "yes,Yes",
        "-A", "no,No",
        "-A", "cancel,Cancel",
        "-t", "15000",
        "Right-Click Test",
        "Right-click to see context menu"
    ], capture_output=True, text=True, timeout=20)

    print(f"\nReturn code: {result.returncode}")
    print(f"Action selected: '{result.stdout.strip()}'")

    if result.returncode == 0:
        action = result.stdout.strip()
        if action in ["yes", "no", "cancel"]:
            print(f"✅ SUCCESS: Selected '{action}' from context menu!")
            return True
        else:
            print(f"❓ UNEXPECTED: Got action '{action}'")
            return False
    else:
        print("❌ FAILED: No action selected")
        return False

def test_both():
    """Test default + context menu together."""
    print("\n" + "="*60)
    print("TEST 3: Default + Context Menu (Both Clicks)")
    print("="*60)
    print("📌 A notification will appear")
    print("📌 Try LEFT-CLICK first (should trigger 'Accept')")
    print("📌 Timeout: 15 seconds")

    input("\nPress ENTER to start LEFT-CLICK test...")

    result1 = subprocess.run([
        "dunstify",
        "-A", "default,Accept",  # Left-click
        "-A", "yes,Yes",         # Right-click menu
        "-A", "no,No",           # Right-click menu
        "-t", "15000",
        "Mixed Actions Test",
        "Try LEFT-click first"
    ], capture_output=True, text=True, timeout=20)

    print(f"\nLeft-click test:")
    print(f"  Return code: {result1.returncode}")
    print(f"  Action: '{result1.stdout.strip()}'")

    if result1.returncode == 0 and result1.stdout.strip() == "default":
        print("  ✅ Left-click worked!")
    else:
        print("  ❌ Left-click didn't trigger default")

    time.sleep(2)

    print("\n📌 Now testing RIGHT-CLICK (should show menu with Yes/No)")
    input("Press ENTER to start RIGHT-CLICK test...")

    result2 = subprocess.run([
        "dunstify",
        "-A", "default,Accept",  # Left-click
        "-A", "yes,Yes",         # Right-click menu
        "-A", "no,No",           # Right-click menu
        "-t", "15000",
        "Mixed Actions Test",
        "Try RIGHT-click for menu"
    ], capture_output=True, text=True, timeout=20)

    print(f"\nRight-click test:")
    print(f"  Return code: {result2.returncode}")
    print(f"  Action: '{result2.stdout.strip()}'")

    if result2.returncode == 0:
        action = result2.stdout.strip()
        if action in ["yes", "no"]:
            print(f"  ✅ Right-click menu worked! Selected '{action}'")
            return True
        elif action == "default":
            print("  ⚠️  Got default instead of menu (maybe left-clicked?)")
            return False

    return False

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║  Dunst Action Click Testing Suite                         ║
║  Testing different mouse click behaviors                  ║
╚════════════════════════════════════════════════════════════╝
""")

    # Check if dunstify exists
    result = subprocess.run(["which", "dunstify"], capture_output=True)
    if result.returncode != 0:
        print("❌ ERROR: dunstify not found!")
        print("   Install dunst to use this test")
        return 1

    # Check capabilities
    result = subprocess.run(["dunstify", "--capabilities"], capture_output=True, text=True)
    if "actions" not in result.stdout:
        print("❌ ERROR: Your dunst doesn't support actions!")
        return 1

    print("✅ dunstify found and supports actions\n")

    # Run tests
    test_default_action()
    test_context_menu()
    test_both()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("""
Expected behavior:
  • Left-click on notification → triggers "default" action
  • Right-click on notification → shows context menu
  • Middle-click → dismisses notification
  • Actions without "default" key only appear in context menu
    """)

    return 0

if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
        exit(130)
