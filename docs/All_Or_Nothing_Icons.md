# All-or-Nothing Icon Resolution

## Overview

The py_desktop_notify library now supports an "all-or-nothing" icon resolution strategy. This ensures consistent visual appearance by using icons from a single source - either all from the system theme or all from a bundled fallback set.

## How It Works

When all-or-nothing mode is enabled (default), the icon manager:

1. **Validates Required Icons**: Checks if the system theme has ALL required icons
2. **Makes a Single Decision**: If ANY icon is missing, switches to the complete fallback set
3. **Ensures Consistency**: No mixing of icon styles - all icons come from one source

## Implementation Details

### Icon Validation

The system uses the icon-mapper's `validate_icons()` API to efficiently check multiple icons at once:

```python
# System icon set validation
results = resolver.validate_icons(['info', 'warning', 'error', 'save', ...])
missing = [name for name, path in results.items() if path is None]

if missing:
    # Fall back to material-complete icon set
    use_fallback_icons()
```

### Default Icon Set

The `MaterialCompleteIconSet` provides comprehensive Material Design icons as fallbacks:

- **250+ icon mappings** covering all common desktop scenarios
- **Intelligent name resolution** with aliases and category-based fallbacks
- **Self-contained** - doesn't depend on system resources

### Required Icons

By default, these essential icons must be present for a theme to be used:

- Status: info, warning, error, success, question
- Actions: save, open, close, folder, file
- System: settings, user, notification, home
- UI: check, cross, help

## Configuration

### Enable/Disable All-or-Nothing Mode

```python
from desktop_notify import get_icon_set_manager

manager = get_icon_set_manager()

# Check current mode
print(manager.get_all_or_nothing_mode())  # True by default

# Disable all-or-nothing (allow mixed icons)
manager.set_all_or_nothing_mode(False)

# Re-enable all-or-nothing
manager.set_all_or_nothing_mode(True)
```

### Customize Required Icons

```python
# Set custom list of required icons
manager.set_required_icons([
    'info', 'warning', 'error',  # Only these must exist
    'save', 'open'
])
```

### Force Specific Icon Set

```python
# Force use of material-complete regardless of system icons
manager.set_active_icon_set('material-complete')

# Or during initialization
from desktop_notify import get_notification_manager

notifier = get_notification_manager(icon_set='material-complete')
```

## Example Usage

```python
from desktop_notify import get_notification_manager

# Initialize with all-or-nothing enabled (default)
notifier = get_notification_manager()

# Send notification - icons will be consistent
notifier.send(
    icon='info',
    title='System Update',
    message='Updates are available'
)

# All these icons will come from the same source
notifier.send(icon='warning', title='Warning', message='Low disk space')
notifier.send(icon='error', title='Error', message='Operation failed')
notifier.send(icon='success', title='Success', message='File saved')
```

## Benefits

1. **Visual Consistency**: All icons have the same style and appearance
2. **Predictable Behavior**: No surprises with missing or mismatched icons
3. **Better User Experience**: Consistent visual language across notifications
4. **Fallback Reliability**: Always have working icons, even on minimal systems

## Icon Set Priority

When in auto mode, icon sets are tried in this order:

1. **System** (priority 100) - Native theme icons via icon-mapper
2. **Material Complete** (priority 70) - Comprehensive Material Design set
3. **Material** (priority 80) - Basic Material Design icons
4. **Minimal** (priority 10) - Unicode/emoji fallbacks

If validation fails at any level, the next set is tried until one passes validation or we reach the minimal set.

## Debugging

Enable debug logging to see icon resolution details:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now you'll see validation results
notifier = get_notification_manager()
# Output: Icon set 'system' missing icons: ['close', 'file', ...]
# Output: Using material-complete icon set (all-or-nothing fallback)
```