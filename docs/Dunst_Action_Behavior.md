# Dunst Interactive Actions - Mouse Click Behavior

## Overview

Dunst supports interactive notifications with actions that respond to mouse clicks. Understanding how dunstify handles different click types is crucial for proper implementation.

## Mouse Click Behavior

| Click Type | Behavior | dunstify Implementation |
|------------|----------|------------------------|
| **Left-Click** | Triggers "default" action | Requires action with key=`"default"` |
| **Right-Click** | Shows context menu | All non-default actions appear here |
| **Middle-Click** | Dismisses notification | Built-in Dunst behavior |

## How dunstify Actions Work

### Default Action (Left-Click)

The **"default"** action key has special meaning in dunstify:

```bash
dunstify -A "default,Accept" "Title" "Message"
```

- When user **left-clicks** the notification, it immediately triggers the "default" action
- dunstify exits with code `0` and outputs `"default"` to stdout
- No context menu appears

### Context Menu Actions (Right-Click)

Any action with a key **other than "default"**:

```bash
dunstify -A "yes,Yes" -A "no,No" "Title" "Message"
```

- When user **right-clicks** the notification, a context menu appears
- User can select from the available actions
- dunstify exits with code `0` and outputs the selected action key to stdout

### Combining Both

You can have BOTH a default action AND context menu actions:

```bash
dunstify -A "default,Quick Action" -A "yes,Yes" -A "no,No" "Title" "Message"
```

**Behavior:**
- **Left-click** → Immediately triggers "Quick Action" (key=`default`)
- **Right-click** → Shows menu with "Yes" and "No" options
- **Middle-click** → Dismisses the notification

## Return Codes

| Return Code | Meaning |
|-------------|---------|
| `0` | Action was selected (check stdout for action key) |
| `1` | Notification timed out (no action taken) |
| `2` | Notification was dismissed (middle-click or close button) |

## Implementation in Python

### Current desktop_notify API

```python
from desktop_notify import send_notification

# Simple context menu (right-click only)
actions = {
    "yes": "Accept",
    "no": "Decline"
}
result = send_notification(
    icon="question",
    title="Confirmation",
    message="Right-click to see options",
    actions=actions
)
# Returns: "yes", "no", or None

# With default action (left-click)
actions = {
    "default": "Quick Accept",  # Left-click triggers this
    "yes": "Accept",            # Right-click menu
    "no": "Decline"             # Right-click menu
}
result = send_notification(
    icon="question",
    title="Confirmation",
    message="Left-click to accept, right-click for options",
    actions=actions
)
# Returns: "default", "yes", "no", or None
```

### How It Maps to dunstify

```python
# Input actions dict:
actions = {
    "default": "Quick Accept",
    "yes": "Yes",
    "no": "No"
}

# Generated dunstify command:
dunstify \
    -A "default,Quick Accept" \
    -A "yes,Yes" \
    -A "no,No" \
    "Title" "Message"
```

## Best Practices

### 1. Always Provide a Default Action for Quick Response

✅ **Good:** Makes left-click useful
```python
actions = {
    "default": "OK",
    "details": "Show Details",
    "cancel": "Cancel"
}
```

❌ **Suboptimal:** User must right-click for any action
```python
actions = {
    "ok": "OK",
    "cancel": "Cancel"
}
```

### 2. Use Descriptive Labels

✅ **Good:** Clear what happens
```python
actions = {
    "default": "Accept & Continue",
    "decline": "No Thanks",
    "later": "Remind Me Later"
}
```

❌ **Unclear:** User doesn't know what will happen
```python
actions = {
    "default": "OK",
    "other": "Other"
}
```

### 3. Limit Context Menu Items

✅ **Good:** 2-4 actions in context menu
```python
actions = {
    "default": "Accept",
    "decline": "Decline",
    "ignore": "Ignore"
}
```

❌ **Too many:** Context menu becomes unwieldy
```python
actions = {
    "default": "Option 1",
    "opt2": "Option 2",
    "opt3": "Option 3",
    "opt4": "Option 4",
    "opt5": "Option 5",
    "opt6": "Option 6"
}
```

## Common Patterns

### Confirmation Dialog

```python
actions = {
    "default": "Yes",  # Quick yes with left-click
    "no": "No"         # Explicit no via right-click
}
```

### Quick Action + More Options

```python
actions = {
    "default": "Open",      # Quick open with left-click
    "edit": "Edit",         # Right-click for edit
    "properties": "Properties"  # Right-click for properties
}
```

### Dismissable Notification with Action

```python
actions = {
    "default": "View Details"  # Left-click for details
    # No other actions = only left-click and middle-click (dismiss) work
}
```

## Testing

Use the test script to verify behavior:

```bash
python tests/test_action_clicks.py
```

This will walk you through testing:
1. Default action (left-click)
2. Context menu (right-click)
3. Combined behavior

## Troubleshooting

### Problem: Left-click doesn't trigger action

**Possible causes:**

1. **Not using "default" key:**
   ```python
   # Wrong - no default action
   actions = {"accept": "Accept"}

   # Correct - has default action
   actions = {"default": "Accept"}
   ```

2. **dunstrc configured to close on left-click:**

   Check your dunstrc for this setting:
   ```bash
   grep "mouse_left_click" ~/.config/dunst/dunstrc
   ```

   If it shows `mouse_left_click = close_current`, left-click will always close the notification instead of triggering the default action.

   **Solution:** Either change dunstrc to:
   ```ini
   mouse_left_click = do_action, close_current
   ```

   Or don't use "default" actions and rely only on right-click context menu:
   ```python
   # Only use right-click menu - works with close_current
   actions = {
       "yes": "Accept",
       "no": "Decline"
   }
   ```

### Problem: Right-click doesn't show menu

**Most Common Cause: Missing dmenu/rofi**

Dunst requires an external menu program (dmenu or rofi) to display the context menu. Check your dunstrc:

```bash
grep "^[[:space:]]*dmenu" ~/.config/dunst/dunstrc
```

**Solution:**
1. Install dmenu or rofi:
   ```bash
   # Arch/Manjaro
   sudo pacman -S dmenu
   # or
   sudo pacman -S rofi

   # Ubuntu/Debian
   sudo apt install dmenu
   # or
   sudo apt install rofi
   ```

2. Configure dunstrc to use the menu program:
   ```ini
   # For dmenu:
   dmenu = /usr/bin/dmenu -p dunst:

   # For rofi:
   dmenu = /usr/bin/rofi -dmenu -p dunst:
   ```

3. Restart Dunst:
   ```bash
   killall dunst
   # Dunst will auto-restart in most desktop environments
   ```

**Other possible causes:**
1. Only one action (and it's "default") - no menu needed
2. Dunst version doesn't support actions - check `dunstify --capabilities`
3. Desktop environment intercepts right-click

**Verify with direct dunstify test:**

```bash
dunstify -A "yes,Yes" -A "no,No" "Test" "Right-click me"
```

### Problem: Actions don't work at all

**Debugging steps:**
1. Check dunstify supports actions:
   ```bash
   dunstify --capabilities | grep actions
   ```
2. Test with minimal example:
   ```bash
   dunstify -A "test,Test" "Test" "Click me"
   ```
3. Check Dunst is actually running:
   ```bash
   pgrep -a dunst
   ```

## Customizing Action Menu Appearance

The right-click context menu is rendered by rofi (or dmenu). You can customize its appearance to match your desktop theme.

See [Rofi Theming](Rofi_Theming.md) for complete documentation on:
- Installing and configuring rofi themes
- Customizing colors, borders, and layout
- Using your existing rofi color schemes
- Advanced theming options

## References

- [Rofi Theming](Rofi_Theming.md) - Desktop Notify rofi theme customization guide
- [Dunst Documentation](https://dunst-project.org/documentation/)
- [dunstify man page](https://man.archlinux.org/man/dunstify.1)
- [Desktop Notifications Specification](https://specifications.freedesktop.org/notification-spec/latest/)
- [Rofi Documentation](https://github.com/davatorium/rofi)
