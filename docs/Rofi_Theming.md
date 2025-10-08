# Rofi Theming for Desktop Notify

This document explains how to customize the appearance of interactive notification action menus using Rofi themes.

## Overview

When using Dunst with interactive actions, right-clicking on a notification displays a context menu. This menu is rendered by Rofi (or dmenu), which can be styled to match your desktop environment.

## Quick Setup

### Automated Installation (Recommended)

Use the included installation script:

```bash
# From the project directory
./scripts/install_rofi_theme.sh

# Dry run to see what would be done
./scripts/install_rofi_theme.sh --dry-run

# Force overwrite existing files
./scripts/install_rofi_theme.sh --force

# Only install theme, don't modify dunstrc
./scripts/install_rofi_theme.sh --no-dunst-config
```

The script will:
- Install the notification theme to `~/.config/rofi/notification.rasi`
- Update your dunstrc to use the theme
- Backup your existing dunstrc before modifications
- Restart Dunst to apply changes

### Manual Installation

If you prefer to install manually:

#### 1. Install the Notification Theme

Copy the included rofi notification theme to your rofi configuration directory:

```bash
cp resources/rofi/notification.rasi ~/.config/rofi/notification.rasi
```

#### 2. Configure Dunst to Use the Theme

Edit your `~/.config/dunst/dunstrc` file and update the `dmenu` path:

```ini
# In the [global] section under "Misc/Advanced"
dmenu = /usr/bin/rofi -dmenu -p dunst: -theme ~/.config/rofi/notification.rasi
```

#### 3. Restart Dunst

```bash
killall dunst
# Dunst will auto-restart in most desktop environments
```

## Theme Customization

### Using Your Existing Color Scheme

The included `notification.rasi` theme imports your current rofi color scheme by default:

```rasi
@import "~/.config/rofi/colors/ayu-dark.rasi"
```

To use a different color scheme, edit `~/.config/rofi/notification.rasi` and change the import:

```rasi
# Use nord color scheme
@import "~/.config/rofi/colors/nord.rasi"

# Use dracula color scheme
@import "~/.config/rofi/colors/dracula.rasi"

# Use gruvbox color scheme
@import "~/.config/rofi/colors/gruvbox.rasi"
```

### Available Color Schemes

The default installation includes these color schemes in `~/.config/rofi/colors/`:

- **ayu-dark** - Dark navy/black with cyan accents (default)
- **nord** - Arctic-inspired color palette
- **dracula** - Dark theme with purple accents
- **gruvbox** - Retro groove colors
- **tokyonight** - Tokyo night-inspired theme
- **catppuccin** - Soothing pastel theme
- **onedark** - Atom's One Dark theme
- And more...

### Color Variables

The notification theme uses these color variables from your color scheme:

| Variable | Purpose | Example (ayu-dark) |
|----------|---------|-------------------|
| `@background` | Menu background | `#0e1419FF` (dark navy) |
| `@foreground` | Text color | `#e5e1cfFF` (light cream) |
| `@selected` | Selection highlight | `#36a3d9FF` (cyan) |
| `@urgent` | Urgent notifications | `#ff3333FF` (red) |
| `@active` | Active items | `#323232FF` (dark gray) |

### Customizing Theme Properties

Edit `~/.config/rofi/notification.rasi` to customize:

#### Window Position

```rasi
window {
    location: north;     /* Options: north, south, east, west, center */
    anchor: north;
    y-offset: 50px;     /* Distance from top/bottom */
    x-offset: 0px;      /* Distance from left/right */
}
```

#### Window Size

```rasi
window {
    width: 500px;       /* Menu width */
}

listview {
    lines: 4;           /* Max number of visible actions */
}
```

#### Border & Corners

```rasi
window {
    border: 2px solid;
    border-radius: 12px;    /* Corner roundness */
    border-color: @selected;
}

element {
    border-radius: 6px;     /* Action button roundness */
}
```

#### Spacing & Padding

```rasi
mainbox {
    padding: 15px;          /* Inner padding */
    spacing: 10px;          /* Space between message and actions */
}

element {
    padding: 10px;          /* Action button padding */
}

listview {
    spacing: 5px;           /* Space between action buttons */
}
```

## Advanced Configuration

### Multiple Themes for Different Urgency Levels

You can create different themes for different notification urgency levels by using Dunst rules:

```ini
# In dunstrc
[urgency_critical]
    dmenu = /usr/bin/rofi -dmenu -p "URGENT:" -theme ~/.config/rofi/notification-urgent.rasi

[urgency_normal]
    dmenu = /usr/bin/rofi -dmenu -p dunst: -theme ~/.config/rofi/notification.rasi
```

### Custom Prompt Text

Change the `-p` parameter in dunstrc:

```ini
dmenu = /usr/bin/rofi -dmenu -p "Choose Action:" -theme ~/.config/rofi/notification.rasi
```

### Using Alternative Fonts

Add font configuration to your notification.rasi:

```rasi
* {
    font: "JetBrains Mono 11";
}
```

### Transparency & Blur

```rasi
window {
    transparency: "real";        /* Enable transparency */
    background-color: #0e1419DD; /* Last 2 digits = alpha (DD = 85%) */
}
```

## Theming Reference

### Complete Color Scheme Template

Create a custom color scheme in `~/.config/rofi/colors/custom.rasi`:

```rasi
* {
    background:     #1e1e2eFF;  /* Dark background */
    background-alt: #1e1e2eFF;  /* Alternative background */
    foreground:     #cdd6f4FF;  /* Light text */
    selected:       #89b4faFF;  /* Highlight color */
    active:         #a6e3a1FF;  /* Active item color */
    urgent:         #f38ba8FF;  /* Urgent/error color */
}
```

Then import it in notification.rasi:

```rasi
@import "~/.config/rofi/colors/custom.rasi"
```

### Testing Your Theme

Test the theme directly with rofi:

```bash
echo -e "Accept\nDecline\nMaybe Later" | rofi -dmenu -p "Test:" -theme ~/.config/rofi/notification.rasi
```

Or use the included test scripts:

```bash
# Run interactive notification test
python tests/example_interactive_actions.py
```

## Troubleshooting

### Theme Not Loading

**Problem**: Rofi still uses default theme

**Solutions**:
1. Verify theme file exists:
   ```bash
   ls -l ~/.config/rofi/notification.rasi
   ```

2. Check dunstrc configuration:
   ```bash
   grep "^[[:space:]]*dmenu" ~/.config/dunst/dunstrc
   ```

3. Test theme manually:
   ```bash
   rofi -dmenu -theme ~/.config/rofi/notification.rasi
   ```

4. Restart Dunst:
   ```bash
   killall dunst
   ```

### Colors Not Matching

**Problem**: Colors don't match your desktop theme

**Solutions**:
1. Verify color scheme import in notification.rasi
2. Check that the color scheme file exists:
   ```bash
   ls -l ~/.config/rofi/colors/
   ```
3. Use absolute path in import if needed:
   ```rasi
   @import "/home/username/.config/rofi/colors/ayu-dark.rasi"
   ```

### Menu Position Issues

**Problem**: Menu appears in wrong location

**Solution**: Adjust window location and anchor in notification.rasi:

```rasi
window {
    location: north;        /* Where to place the window */
    anchor: north;          /* Which edge to anchor to */
    y-offset: 50px;        /* Offset from anchor point */
}
```

Common combinations:
- **Top center**: `location: north; anchor: north;`
- **Bottom center**: `location: south; anchor: south;`
- **Center**: `location: center; anchor: center;`
- **Top right**: `location: northeast; anchor: northeast;`

### Rofi Syntax Errors

**Problem**: Rofi shows syntax error

**Solution**: Validate your rasi file:

```bash
rofi -dump-theme -theme ~/.config/rofi/notification.rasi
```

Common issues:
- Missing semicolons after property values
- Incorrect color format (must be `#RRGGBBAA`)
- Invalid property names

## Examples

### Minimal Theme

```rasi
@import "~/.config/rofi/colors/ayu-dark.rasi"

window {
    width: 400px;
    location: north;
    y-offset: 30px;
    border-radius: 8px;
    background-color: @background;
}

element selected {
    background-color: @selected;
}
```

### Detailed Theme with Icons

```rasi
@import "~/.config/rofi/colors/nord.rasi"

* {
    font: "Fira Code 10";
}

window {
    width: 600px;
    location: north;
    anchor: north;
    y-offset: 50px;
    border: 3px solid;
    border-radius: 15px;
    border-color: @selected;
    background-color: @background;
}

element {
    padding: 12px;
    border-radius: 8px;
}

element selected {
    background-color: @selected;
    text-color: @background;
    font: "Fira Code Bold 10";
}
```

## Resources

- [Rofi Documentation](https://github.com/davatorium/rofi)
- [Rofi Theme Tutorial](https://github.com/davatorium/rofi/blob/next/doc/rofi-theme.5.markdown)
- [adi1090x Rofi Themes](https://github.com/adi1090x/rofi)
- [Dunst Documentation](https://dunst-project.org/documentation/)

## See Also

- [Dunst Action Behavior](Dunst_Action_Behavior.md) - Interactive notification setup
- [README.md](../README.md) - Main documentation
