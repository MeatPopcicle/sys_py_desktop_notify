#!/usr/bin/env python3
"""Check which icons we're missing from the 70 standard set."""

# Icons from breeze.yaml
breeze_icons = [
    'info', 'warning', 'error', 'success', 'question', 'alert', 'ok', 'valid',
    'save', 'open', 'new', 'copy', 'cut', 'paste', 'undo', 'redo', 'find', 'delete', 'clear',
    'back', 'forward', 'up', 'down', 'home', 'refresh',
    'play', 'pause', 'stop', 'next', 'previous', 'record', 'music', 'video',
    'microphone', 'mic', 'camera', 'printer', 'scanner', 'speaker', 'headphones', 'battery',
    'settings', 'config', 'preferences', 'user', 'users', 'network', 'wifi', 'bluetooth',
    'power', 'logout', 'lock', 'browser', 'mail', 'editor', 'terminal', 'calculator',
    'folder', 'file', 'document', 'image', 'archive',
    'load', 'loading', 'process', 'working', 'busy'
]

# Icons we already have
existing_icons = [
    'info', 'warning', 'error', 'check_circle', 'help', 'save', 'folder_open',
    'folder', 'insert_drive_file', 'settings', 'person', 'notifications',
    'home', 'check', 'close', 'help_outline', 'edit', 'delete'
]

# Map our existing names to breeze names
our_to_breeze = {
    'check_circle': ['success', 'ok', 'valid'],
    'help': ['question'],
    'insert_drive_file': ['file'],
    'person': ['user'],
    'folder_open': ['open'],  # Note: 'open' in breeze means document-open
}

# Check what we're missing
missing = []
for icon in breeze_icons:
    found = False
    
    # Check if we have it directly
    if icon in existing_icons:
        found = True
    
    # Check if it's mapped
    for our_icon, breeze_aliases in our_to_breeze.items():
        if icon in breeze_aliases:
            found = True
            break
    
    if not found:
        missing.append(icon)

print(f"Total breeze icons: {len(set(breeze_icons))}")
print(f"Icons we have: {len(existing_icons)}")
print(f"Missing icons: {len(missing)}")
print("\nMissing icons:")
for icon in sorted(set(missing)):
    print(f"  - {icon}")