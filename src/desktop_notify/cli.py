# ────────────────────────────────────────────────────────────────────────────────
# Desktop Notify CLI Interface
# ────────────────────────────────────────────────────────────────────────────────
"""
cli.py
AUTHOR: Desktop Notify Team
DATE: 2025-10-05
VERSION: 1.0.0

Command-line interface for desktop notification system.
"""

import argparse
import sys
from typing import Optional, Dict

from . import __version__
from .api import send_notification, NotificationManager, is_notifications_available
from .exceptions import DesktopNotifyError


def parse_actions(actions_str: str) -> Dict[str, str]:
    """
    Parse action string into action dictionary.

    Format: "key1:Label1,key2:Label2"
    Example: "yes:Accept,no:Decline,later:Remind Later"

    Args:
        actions_str: Comma-separated list of key:label pairs

    Returns:
        Dictionary mapping action keys to labels
    """
    actions = {}
    if not actions_str:
        return actions

    for action_pair in actions_str.split(','):
        if ':' not in action_pair:
            print(f"Warning: Invalid action format '{action_pair}'. Expected 'key:label'")
            continue
        key, label = action_pair.split(':', 1)
        actions[key.strip()] = label.strip()

    return actions


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog='desktop-notify',
        description='Send desktop notifications from the command line',
        epilog='For more information, visit: https://github.com/MeatPopcicle/sys_py_desktop_notify'
    )

    # ─────────────────────────────────────────────────────────────────
    # Version
    # ─────────────────────────────────────────────────────────────────
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'desktop-notify {__version__}'
    )

    # ─────────────────────────────────────────────────────────────────
    # Required Arguments
    # ─────────────────────────────────────────────────────────────────
    parser.add_argument(
        'title',
        help='Notification title'
    )

    parser.add_argument(
        'message',
        nargs='?',
        default='',
        help='Notification message (optional)'
    )

    # ─────────────────────────────────────────────────────────────────
    # Optional Arguments
    # ─────────────────────────────────────────────────────────────────
    parser.add_argument(
        '-i', '--icon',
        default='info',
        help='Icon name or path (default: info)'
    )

    parser.add_argument(
        '-u', '--urgency',
        choices=['low', 'normal', 'critical'],
        default='normal',
        help='Urgency level (default: normal)'
    )

    parser.add_argument(
        '-t', '--timeout',
        type=int,
        metavar='MS',
        help='Timeout in milliseconds (default: backend default)'
    )

    parser.add_argument(
        '-a', '--actions',
        metavar='ACTIONS',
        help='Interactive actions as "key1:Label1,key2:Label2"'
    )

    parser.add_argument(
        '-n', '--notification-id',
        metavar='ID',
        help='Notification ID for updates/replacements'
    )

    # ─────────────────────────────────────────────────────────────────
    # Backend Configuration
    # ─────────────────────────────────────────────────────────────────
    parser.add_argument(
        '-b', '--backend',
        help='Force specific backend (e.g., dunst, console)'
    )

    parser.add_argument(
        '--icon-set',
        help='Force specific icon set (e.g., system, material, minimal)'
    )

    # ─────────────────────────────────────────────────────────────────
    # Utility Options
    # ─────────────────────────────────────────────────────────────────
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check if notification system is available'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug output'
    )

    return parser


def main() -> int:
    """
    Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args()

    # ─────────────────────────────────────────────────────────────────
    # Handle --check flag
    # ─────────────────────────────────────────────────────────────────
    if args.check:
        available = is_notifications_available()
        if available:
            print("✅ Notification system is available")
            return 0
        else:
            print("❌ Notification system is not available")
            return 1

    # ─────────────────────────────────────────────────────────────────
    # Enable debug logging if requested
    # ─────────────────────────────────────────────────────────────────
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    # ─────────────────────────────────────────────────────────────────
    # Parse actions if provided
    # ─────────────────────────────────────────────────────────────────
    actions = None
    if args.actions:
        actions = parse_actions(args.actions)
        if not actions:
            print("Error: No valid actions parsed", file=sys.stderr)
            return 1

    # ─────────────────────────────────────────────────────────────────
    # Send notification
    # ─────────────────────────────────────────────────────────────────
    try:
        # Create manager if custom backend/icon-set specified
        if args.backend or args.icon_set:
            manager = NotificationManager(
                backend=args.backend or "auto",
                icon_set=args.icon_set or "auto",
                timeout=args.timeout,
                urgency=args.urgency
            )
            result = manager.send(
                icon=args.icon,
                title=args.title,
                message=args.message,
                notification_id=args.notification_id,
                actions=actions
            )
        else:
            # Use simple API for default behavior
            result = send_notification(
                icon=args.icon,
                title=args.title,
                message=args.message,
                notification_id=args.notification_id,
                urgency=args.urgency,
                timeout=args.timeout,
                actions=actions
            )

        # ─────────────────────────────────────────────────────────────────
        # Handle result
        # ─────────────────────────────────────────────────────────────────
        if actions:
            if result:
                print(f"User selected: {result}")
            else:
                print("No action selected (timeout or dismissed)")

        return 0

    except DesktopNotifyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
