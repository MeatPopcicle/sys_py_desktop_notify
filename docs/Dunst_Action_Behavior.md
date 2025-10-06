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

**Solution:** Make sure you're using the `"default"` key:

```python
# Wrong - no default action
actions = {"accept": "Accept"}

# Correct - has default action
actions = {"default": "Accept"}
```

### Problem: Right-click doesn't show menu

**Possible causes:**
1. Only one action (and it's "default") - no menu needed
2. Dunst version doesn't support actions - check `dunstify --capabilities`
3. Desktop environment intercepts right-click

**Solution:** Verify with direct dunstify test:

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

## References

- [Dunst Documentation](https://dunst-project.org/documentation/)
- [dunstify man page](https://man.archlinux.org/man/dunstify.1)
- [Desktop Notifications Specification](https://specifications.freedesktop.org/notification-spec/latest/)
