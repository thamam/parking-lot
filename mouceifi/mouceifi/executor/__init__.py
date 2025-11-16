"""Executor module for platform-specific mouse control."""
import platform
from typing import Optional
from .base import MouseExecutor


def get_executor(dry_run: bool = False, platform_name: Optional[str] = None) -> MouseExecutor:
    """
    Factory function to get the appropriate executor for the current platform.

    Uses lazy imports to avoid importing platform-specific dependencies
    until they're actually needed.

    Args:
        dry_run: If True, create executor in dry-run mode
        platform_name: Optional platform override for testing

    Returns:
        MouseExecutor instance for the current platform

    Raises:
        NotImplementedError: If platform is not supported
    """
    if platform_name is None:
        platform_name = platform.system().lower()

    if platform_name == 'linux':
        from .linux import LinuxMouseExecutor
        return LinuxMouseExecutor(dry_run=dry_run)
    elif platform_name == 'windows':
        from .windows import WindowsMouseExecutor
        return WindowsMouseExecutor(dry_run=dry_run)
    elif platform_name == 'darwin':  # macOS
        from .macos import MacOSMouseExecutor
        return MacOSMouseExecutor(dry_run=dry_run)
    else:
        raise NotImplementedError(f"Platform '{platform_name}' is not supported")


__all__ = [
    'MouseExecutor',
    'get_executor'
]
