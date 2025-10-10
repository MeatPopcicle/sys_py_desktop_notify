# Notification Daemon Comparison

## Overview

Different Linux desktop environments use different notification daemons, each with unique behaviors for handling interactive actions. This guide helps you understand which daemon suits your needs and how to adapt your application accordingly.

## Quick Comparison Table

| Feature | Dunst | GNOME Shell | KDE Plasma | mako | notification-daemon |
|---------|-------|-------------|------------|------|---------------------|
| **Visual Action Buttons** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Mouse Click Zones** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **External Menu** | ✅ rofi/dmenu | ❌ N/A | ❌ N/A | ❌ N/A | ❌ N/A |
| **Action Limit** | Unlimited | ~3 typical | ~4 typical | Unlimited | ~3 typical |
| **Wayland Support** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Limited |
| **X11 Support** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| **Configuration** | Text file | GUI/gsettings | GUI/kcfg | Text file | Text file |
| **Footprint** | Minimal | Heavy | Heavy | Minimal | Light |
| **Best For** | Tiling WMs | GNOME | KDE Plasma | Sway/wlroots | Lightweight DEs |

## Detailed Comparison

### Dunst

**Philosophy:** Minimal, keyboard/mouse-driven, text-based configuration

**Action Handling:**
- NO visual buttons on notifications
- Uses mouse click zones on the entire notification window:
  - Left-click → "default" action
  - Right-click → Context menu (via rofi/dmenu)
  - Middle-click → Dismiss
- Entire notification is interactive, not just specific areas

**Visual Example:**
```
┌──────────────────────────────┐
│ Software Update Available    │ ← Left-click triggers default
│ 47 packages can be updated   │ ← Right-click shows menu
│                              │ ← Middle-click dismisses
└──────────────────────────────┘
  (No visible buttons - whole notification is clickable)
```

**Pros:**
- Extremely lightweight and fast
- Highly configurable via dunstrc
- Works perfectly with tiling window managers
- Clean, consistent appearance
- External menu can be themed extensively (rofi)

**Cons:**
- No visual indication of available actions
- Requires user to know the mouse click pattern
- Right-click menu requires rofi/dmenu installation
- Different interaction model from standard desktop environments

**Best For:**
- i3, awesome, bspwm, or other tiling window managers
- Users who prefer keyboard/mouse-driven workflows
- Minimal resource usage environments
- Power users comfortable with non-standard UIs

### GNOME Shell Notification Daemon

**Philosophy:** Integrated desktop experience with visual consistency

**Action Handling:**
- Visual buttons rendered directly on notification
- Buttons appear at bottom of notification
- Click button → triggers action
- Usually displays first 2-3 actions, others in "more" menu

**Visual Example:**
```
┌──────────────────────────────────┐
│ Software Update Available        │
│ 47 packages can be updated       │
│                                  │
│ [Update Now] [View Details]     │ ← Clickable buttons
└──────────────────────────────────┘
```

**Pros:**
- Familiar, standard desktop interaction
- Visual clarity - users see available actions immediately
- Consistent with GNOME design language
- Integrated with GNOME Shell features

**Cons:**
- Heavy resource usage (part of GNOME Shell)
- Limited action count (UI real estate)
- Harder to customize appearance
- Only practical on GNOME desktop

**Best For:**
- GNOME desktop environment users
- Users expecting standard desktop notification behavior
- Applications targeting general desktop users

### KDE Plasma Notification System

**Philosophy:** Feature-rich, highly configurable via GUI

**Action Handling:**
- Visual buttons on notifications
- Supports inline replies and complex interactions
- Action history and notification center
- Typically shows 3-4 actions before wrapping

**Visual Example:**
```
┌────────────────────────────────────┐
│ Software Update Available          │
│ 47 packages can be updated         │
│                                    │
│ [Install] [Details] [Remind Later]│ ← Buttons
└────────────────────────────────────┘
```

**Pros:**
- Rich feature set (history, grouping, etc.)
- Highly configurable through System Settings
- Beautiful visual presentation
- Supports complex interactions (inline replies, progress, etc.)

**Cons:**
- Heavy resource usage
- Requires KDE Plasma environment
- Complex configuration for simple needs
- Can be overwhelming

**Best For:**
- KDE Plasma desktop environment users
- Applications needing rich notification features
- Users who want extensive customization via GUI

### mako (Wayland)

**Philosophy:** Minimal Wayland-native notification daemon

**Action Handling:**
- Visual buttons rendered on notification
- Simple, clean button layout
- Limited to Wayland compositors (Sway, river, etc.)

**Visual Example:**
```
┌─────────────────────────────┐
│ Update Available            │
│ 47 packages ready           │
│                             │
│ [Update] [Later]           │ ← Buttons
└─────────────────────────────┘
```

**Pros:**
- Native Wayland support
- Lightweight and fast
- Visual buttons for clarity
- Simple configuration

**Cons:**
- Wayland-only (no X11)
- Less mature than alternatives
- Fewer features than GNOME/KDE
- Limited theming options

**Best For:**
- Sway, river, Hyprland, or other Wayland compositors
- Users wanting minimal daemon with visual buttons
- Wayland-committed setups

### notification-daemon (Legacy)

**Philosophy:** Original freedesktop.org reference implementation

**Action Handling:**
- Basic visual buttons
- Simple, no-frills approach
- Follows spec closely

**Pros:**
- Lightweight
- Well-tested
- Works on various environments

**Cons:**
- Outdated, minimal development
- Basic features only
- Better alternatives available

**Best For:**
- Legacy systems
- Minimal installations where other daemons aren't suitable

## How to Choose

### Use Dunst if:
- ✅ You use a tiling window manager (i3, awesome, bspwm, etc.)
- ✅ You value minimal resource usage
- ✅ You're comfortable with mouse click zones instead of buttons
- ✅ You want extensive text-based configuration
- ✅ You have rofi/dmenu installed or don't mind installing it

### Use GNOME Shell daemon if:
- ✅ You run GNOME desktop environment
- ✅ You want standard desktop notification behavior
- ✅ You need integration with GNOME features
- ✅ You target general desktop users

### Use KDE Plasma if:
- ✅ You run KDE Plasma desktop environment
- ✅ You need rich notification features (history, grouping, etc.)
- ✅ You want GUI-based configuration
- ✅ You need complex interactions (inline replies, etc.)

### Use mako if:
- ✅ You use a Wayland compositor (Sway, river, etc.)
- ✅ You want minimal daemon with visual buttons
- ✅ You don't need X11 support
- ✅ You value simplicity

## Migration Guide

### Coming from Button-Based Daemon to Dunst

If your application expects visual buttons but you're moving to Dunst:

**1. Update Documentation:**
Explain to users that Dunst uses mouse clicks instead of buttons:

```markdown
## Interactive Notifications with Dunst

Dunst uses mouse click zones instead of visual buttons:
- **Left-click** the notification to accept/perform default action
- **Right-click** the notification to see all options
- **Middle-click** to dismiss
```

**2. Design Actions Appropriately:**

```python
# Good for Dunst - clear default action
actions = {
    "default": "Accept",      # Quick left-click action
    "decline": "Decline",     # Right-click menu
    "later": "Remind Later"   # Right-click menu
}

# Also good - no default, all in menu
actions = {
    "yes": "Yes",
    "no": "No",
    "cancel": "Cancel"
}
```

**3. User Education:**
- Mention in README that Dunst users need rofi/dmenu
- Link to Dunst configuration guide
- Explain the mouse click pattern

### Coming from Dunst to Button-Based Daemon

If you're used to Dunst and switching to GNOME/KDE:

**What changes:**
- Actions appear as visual buttons, not click zones
- Click the button directly (not the whole notification)
- No rofi/dmenu menu - buttons are on the notification itself
- No "default" action concept - all actions are equal

**Action Design:**

```python
# Works well on both
actions = {
    "accept": "Accept",
    "decline": "Decline"
}

# Dunst-specific "default" might not have special meaning
actions = {
    "default": "Accept",  # Just another button on GNOME/KDE
    "decline": "Decline"
}
```

## Desktop Notify Library Support

### Current Status

Desktop Notify currently supports:
- ✅ **Dunst** - Full support via dunstify backend
- ⚠️ **Others** - Partial support (actions may not work as expected)

### Future Plans

**Potential enhancements:**

1. **libnotify Backend:**
   - Add backend using libnotify (via PyGObject or notify2)
   - Would work with any freedesktop.org notification daemon
   - Automatic detection of daemon capabilities
   - Button-based daemons would show visual buttons

2. **Daemon Detection:**
   - Auto-detect which daemon is running
   - Adjust behavior based on daemon capabilities
   - Provide appropriate user feedback

3. **Unified API:**
   - Same code works on any daemon
   - Library handles daemon-specific quirks
   - User documentation specific to their daemon

## Return Value Consistency

All daemons return selected action keys via D-Bus, but the user interaction differs:

**Dunst:**
```
User right-clicks → rofi menu → selects "accept" → returns "accept"
```

**GNOME/KDE:**
```
User clicks [Accept] button → returns "accept"
```

**Desktop Notify abstracts this:**
```python
result = send_notification(actions={"accept": "Accept", ...})
# Result is always the KEY, regardless of daemon
if result == "accept":
    handle_accept()
```

## Resources

**Dunst:**
- [Dunst Documentation](https://dunst-project.org/documentation/)
- [dunstify man page](https://man.archlinux.org/man/dunstify.1)

**GNOME:**
- [GNOME Shell Notifications](https://wiki.gnome.org/Projects/GnomeShell/Notifications)
- [GLib Notification API](https://docs.gtk.org/gio/class.Notification.html)

**KDE:**
- [KDE Notification System](https://userbase.kde.org/System_Settings/Notifications)
- [KNotification Documentation](https://api.kde.org/frameworks/knotifications/html/)

**mako:**
- [mako Documentation](https://github.com/emersion/mako)
- [mako man page](https://man.archlinux.org/man/mako.1)

**Freedesktop Spec:**
- [Desktop Notifications Specification](https://specifications.freedesktop.org/notification-spec/latest/)

## See Also

- [Dunst Action Behavior](Dunst_Action_Behavior.md) - Detailed Dunst interaction guide
- [Rofi Theming](Rofi_Theming.md) - Customize Dunst's action menu appearance
- [README](../README.md) - Main documentation
