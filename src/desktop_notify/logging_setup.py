# ────────────────────────────────────────────────────────────────────────────────
# Desktop Notify Logging Setup
# ────────────────────────────────────────────────────────────────────────────────
"""
logging_setup.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Early logging setup for desktop notification system.
"""

import logging


def setup_desktop_notify_logging() -> None:
    """
    Setup logging for desktop-notify based on configuration.
    This is called early during module import.
    """
    try:
        # Import here to avoid circular imports during module init
        from .config import get_config
        
        config = get_config()
        log_level = config.log_level.upper()
        
        # Validate log level
        if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            log_level = 'INFO'
        
        # Set log level for desktop_notify loggers
        desktop_logger = logging.getLogger('desktop_notify')
        desktop_logger.setLevel(getattr(logging, log_level))
        
        config_logger = logging.getLogger('config_manager')
        config_logger.setLevel(getattr(logging, log_level))
        
        # Log that we've configured logging
        desktop_logger.debug(f"Desktop-notify logging configured: {log_level}")
        
    except Exception as e:
        # Fallback to INFO level if config loading fails
        logging.getLogger('desktop_notify').setLevel(logging.INFO)
        logging.getLogger('config_manager').setLevel(logging.INFO)
        logging.getLogger('desktop_notify').warning(f"Failed to configure logging from config: {e}")


# Setup logging when module is imported
setup_desktop_notify_logging()