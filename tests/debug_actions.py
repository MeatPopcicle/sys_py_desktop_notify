#!/usr/bin/env python3
"""
Debug action interactions step by step
"""

import subprocess
import time

def test_dunstify_direct():
    """Test dunstify actions directly."""
    print("🔍 Testing dunstify actions directly...")
    print("   A notification should appear.")
    print("   Try right-clicking on it.")
    print("   This will timeout in 10 seconds if no action is taken.")
    
    # Test with dunstify directly
    result = subprocess.run([
        "dunstify", 
        "-A", "yes,Yes Please", 
        "-A", "no,No Thanks",
        "-t", "10000",  # 10 second timeout
        "Action Test", 
        "Right-click this notification!"
    ], capture_output=True, text=True)
    
    print(f"   dunstify return code: {result.returncode}")
    
    if result.returncode == 0:
        action = result.stdout.strip()
        print(f"   ✅ Action selected: '{action}'")
        return action
    elif result.returncode == 1:
        print("   ⏰ Notification timed out (no action selected)")
        return None
    elif result.returncode == 2:
        print("   ❌ Notification was dismissed")
        return None
    else:
        print(f"   ❓ Unexpected return code: {result.returncode}")
        print(f"   stdout: {result.stdout}")
        print(f"   stderr: {result.stderr}")
        return None

def test_capabilities():
    """Check Dunst capabilities."""
    print("\n🔍 Checking Dunst capabilities...")
    
    result = subprocess.run(["dunstify", "--capabilities"], capture_output=True, text=True)
    
    if result.returncode == 0:
        capabilities = result.stdout.strip().split('\n')
        print("   Supported capabilities:")
        for cap in capabilities:
            print(f"     - {cap}")
        
        if "actions" in capabilities:
            print("   ✅ Actions are supported!")
            return True
        else:
            print("   ❌ Actions are NOT supported!")
            return False
    else:
        print(f"   ❌ Could not get capabilities: {result.stderr}")
        return False

def test_single_action():
    """Test with a single action (should work with middle-click too)."""
    print("\n🔍 Testing single action...")
    print("   Try right-clicking OR middle-clicking this notification")
    
    result = subprocess.run([
        "dunstify",
        "-A", "default,Click Me!",
        "-t", "15000",
        "Single Action Test",
        "Click this notification!"
    ], capture_output=True, text=True)
    
    print(f"   Return code: {result.returncode}")
    if result.returncode == 0:
        print(f"   ✅ Action triggered: '{result.stdout.strip()}'")
        return True
    else:
        print("   ❌ No action triggered")
        return False

def main():
    print("🔧 Dunst Action Debugging")
    print("=" * 50)
    
    # Step 1: Check capabilities
    supports_actions = test_capabilities()
    
    if not supports_actions:
        print("\n❌ Your Dunst installation doesn't support actions!")
        print("   You may need to update Dunst or check compilation flags.")
        return 1
    
    input("\nPress ENTER to test actions...")
    
    # Step 2: Test direct dunstify
    action = test_dunstify_direct()
    
    if action:
        print(f"\n✅ SUCCESS: Actions work! You selected '{action}'")
    else:
        print("\n❌ Actions didn't work. Trying single action test...")
        
        # Step 3: Try single action
        time.sleep(2)
        if test_single_action():
            print("\n✅ Single actions work!")
            print("   Issue might be with multi-action context menu.")
        else:
            print("\n❌ Even single actions don't work.")
            print("\n🔍 TROUBLESHOOTING SUGGESTIONS:")
            print("   1. Check if notifications appear at all")
            print("   2. Try clicking directly on the notification text")
            print("   3. Check Dunst logs: journalctl -u dunst")
            print("   4. Verify mouse settings in your desktop environment")
    
    return 0

if __name__ == "__main__":
    exit(main())