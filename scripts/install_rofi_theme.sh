#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# Desktop-Notify Rofi Theme Installer
# ═══════════════════════════════════════════════════════════════════════════════
#
# Installs the desktop-notify rofi notification theme and configures Dunst to use it.
#
# Usage:
#   ./scripts/install_rofi_theme.sh [options]
#
# Options:
#   --dry-run          Show what would be done without making changes
#   --force            Overwrite existing files without prompting
#   --no-dunst-config  Don't modify dunstrc (only install theme)
#   --help             Show this help message
#
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ───────────────────────────────────────────────────────────────────────────────
# Configuration
# ───────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
THEME_SOURCE="$PROJECT_DIR/resources/rofi/notification.rasi"
THEME_DEST="$HOME/.config/rofi/notification.rasi"
DUNSTRC="$HOME/.config/dunst/dunstrc"

DRY_RUN=false
FORCE=false
NO_DUNST_CONFIG=false

# ───────────────────────────────────────────────────────────────────────────────
# Colors for output
# ───────────────────────────────────────────────────────────────────────────────

if [[ -t 1 ]]; then
    COLOR_RESET='\033[0m'
    COLOR_GREEN='\033[0;32m'
    COLOR_YELLOW='\033[1;33m'
    COLOR_RED='\033[0;31m'
    COLOR_BLUE='\033[0;34m'
    COLOR_CYAN='\033[0;36m'
else
    COLOR_RESET=''
    COLOR_GREEN=''
    COLOR_YELLOW=''
    COLOR_RED=''
    COLOR_BLUE=''
    COLOR_CYAN=''
fi

# ───────────────────────────────────────────────────────────────────────────────
# Helper functions
# ───────────────────────────────────────────────────────────────────────────────

print_success() {
    echo -e "${COLOR_GREEN}✓${COLOR_RESET} $1"
}

print_info() {
    echo -e "${COLOR_BLUE}→${COLOR_RESET} $1"
}

print_warning() {
    echo -e "${COLOR_YELLOW}!${COLOR_RESET} $1"
}

print_error() {
    echo -e "${COLOR_RED}✗${COLOR_RESET} $1" >&2
}

show_help() {
    sed -n '/^# Desktop-Notify Rofi Theme Installer/,/^# ═══════════════════════════════════════════════════════════════════════════════$/p' "$0" | sed 's/^# //; s/^#//'
}

# ───────────────────────────────────────────────────────────────────────────────
# Parse command line arguments
# ───────────────────────────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --no-dunst-config)
            NO_DUNST_CONFIG=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Run with --help for usage information"
            exit 1
            ;;
    esac
done

# ───────────────────────────────────────────────────────────────────────────────
# Validate environment
# ───────────────────────────────────────────────────────────────────────────────

validate_environment() {
    print_info "Validating environment..."

    # Check if theme source exists
    if [[ ! -f "$THEME_SOURCE" ]]; then
        print_error "Theme file not found: $THEME_SOURCE"
        exit 1
    fi

    # Check if rofi is installed
    if ! command -v rofi &> /dev/null; then
        print_warning "rofi is not installed"
        print_info "Install rofi to use themed notification menus:"
        print_info "  Arch/Manjaro: sudo pacman -S rofi"
        print_info "  Ubuntu/Debian: sudo apt install rofi"
        exit 1
    fi

    print_success "Environment validation complete"
}

# ───────────────────────────────────────────────────────────────────────────────
# Install rofi theme
# ───────────────────────────────────────────────────────────────────────────────

install_theme() {
    print_info "Installing rofi theme..."

    # Create rofi config directory if it doesn't exist
    if [[ ! -d "$(dirname "$THEME_DEST")" ]]; then
        if [[ "$DRY_RUN" == false ]]; then
            mkdir -p "$(dirname "$THEME_DEST")"
            print_success "Created directory: $(dirname "$THEME_DEST")"
        else
            print_info "[DRY RUN] Would create directory: $(dirname "$THEME_DEST")"
        fi
    fi

    # Check if theme already exists
    if [[ -f "$THEME_DEST" ]] && [[ "$FORCE" == false ]]; then
        print_warning "Theme file already exists: $THEME_DEST"
        read -p "Overwrite? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Skipping theme installation"
            return
        fi
    fi

    # Copy theme file
    if [[ "$DRY_RUN" == false ]]; then
        cp "$THEME_SOURCE" "$THEME_DEST"
        print_success "Installed theme: $THEME_DEST"
    else
        print_info "[DRY RUN] Would copy: $THEME_SOURCE → $THEME_DEST"
    fi
}

# ───────────────────────────────────────────────────────────────────────────────
# Configure dunstrc
# ───────────────────────────────────────────────────────────────────────────────

configure_dunstrc() {
    if [[ "$NO_DUNST_CONFIG" == true ]]; then
        print_info "Skipping dunstrc configuration (--no-dunst-config)"
        return
    fi

    print_info "Configuring dunstrc..."

    # Check if dunstrc exists
    if [[ ! -f "$DUNSTRC" ]]; then
        print_warning "dunstrc not found: $DUNSTRC"
        print_info "Create dunstrc configuration first"
        return
    fi

    # Check if dmenu line exists
    if ! grep -q "^[[:space:]]*dmenu[[:space:]]*=" "$DUNSTRC"; then
        print_warning "No dmenu configuration found in dunstrc"
        print_info "Add this line to the [global] section of $DUNSTRC:"
        echo "    dmenu = /usr/bin/rofi -dmenu -p dunst: -theme ~/.config/rofi/notification.rasi"
        return
    fi

    # Check if already configured for rofi theme
    if grep -q "rofi.*-theme.*notification.rasi" "$DUNSTRC"; then
        print_success "dunstrc already configured for notification theme"
        return
    fi

    # Update dmenu line
    if [[ "$DRY_RUN" == false ]]; then
        # Backup dunstrc
        cp "$DUNSTRC" "$DUNSTRC.backup.$(date +%Y%m%d_%H%M%S)"
        print_success "Created backup: $DUNSTRC.backup.*"

        # Update dmenu line
        sed -i 's|^\([[:space:]]*dmenu[[:space:]]*=.*rofi.*-dmenu\)\(.*\)$|\1 -theme ~/.config/rofi/notification.rasi|' "$DUNSTRC"
        print_success "Updated dunstrc with theme configuration"
    else
        print_info "[DRY RUN] Would update dmenu line in dunstrc"
    fi
}

# ───────────────────────────────────────────────────────────────────────────────
# Restart Dunst
# ───────────────────────────────────────────────────────────────────────────────

restart_dunst() {
    if [[ "$NO_DUNST_CONFIG" == true ]]; then
        print_info "Skipping Dunst restart (--no-dunst-config)"
        return
    fi

    if ! pgrep -x dunst > /dev/null; then
        print_warning "Dunst is not running"
        return
    fi

    print_info "Restarting Dunst to apply changes..."

    if [[ "$DRY_RUN" == false ]]; then
        killall dunst || true
        print_success "Dunst restarted (will auto-start in most desktop environments)"
    else
        print_info "[DRY RUN] Would restart Dunst"
    fi
}

# ───────────────────────────────────────────────────────────────────────────────
# Test theme
# ───────────────────────────────────────────────────────────────────────────────

test_theme() {
    if [[ "$DRY_RUN" == true ]]; then
        print_info "[DRY RUN] Would test theme with rofi"
        return
    fi

    print_info "Testing theme..."
    echo -e "\nYou can test the theme with:"
    echo "  echo -e 'Accept\nDecline\nMaybe Later' | rofi -dmenu -p 'Test:' -theme ~/.config/rofi/notification.rasi"
    echo ""
    echo "Or send a test notification:"
    echo "  dunstify -A 'yes,Yes' -A 'no,No' 'Test' 'Right-click to see menu'"
}

# ───────────────────────────────────────────────────────────────────────────────
# Main installation flow
# ───────────────────────────────────────────────────────────────────────────────

main() {
    echo -e "${COLOR_CYAN}═══════════════════════════════════════════════════════════════════════════════${COLOR_RESET}"
    echo -e "${COLOR_CYAN}  Desktop-Notify Rofi Theme Installer${COLOR_RESET}"
    echo -e "${COLOR_CYAN}═══════════════════════════════════════════════════════════════════════════════${COLOR_RESET}"
    echo ""

    if [[ "$DRY_RUN" == true ]]; then
        print_warning "DRY RUN MODE - No changes will be made"
        echo ""
    fi

    validate_environment
    install_theme
    configure_dunstrc
    restart_dunst

    echo ""
    echo -e "${COLOR_CYAN}═══════════════════════════════════════════════════════════════════════════════${COLOR_RESET}"
    print_success "Installation complete!"
    echo -e "${COLOR_CYAN}═══════════════════════════════════════════════════════════════════════════════${COLOR_RESET}"
    echo ""

    test_theme

    echo ""
    print_info "For customization options, see: docs/Rofi_Theming.md"
}

main
