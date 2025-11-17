"""Rollback manager for undoing FreeCAD operations."""

import logging
import tempfile
import os
import shutil
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Snapshot:
    """Represents a document snapshot for rollback."""
    timestamp: datetime
    description: str
    file_path: str
    operation_count: int
    metadata: Dict[str, Any]


class RollbackManager:
    """
    Manages rollback capability for FreeCAD operations.

    Creates snapshots before operations and enables restoration
    to previous states.
    """

    def __init__(self, file_parser, max_snapshots: int = 10):
        """
        Initialize the rollback manager.

        Args:
            file_parser: FreeCADFileParser instance
            max_snapshots: Maximum number of snapshots to keep
        """
        self.file_parser = file_parser
        self.max_snapshots = max_snapshots
        self.snapshots: List[Snapshot] = []
        self.temp_dir = tempfile.mkdtemp(prefix='freecad_rollback_')
        self.snapshot_counter = 0

        logger.info(f"Rollback manager initialized. Temp dir: {self.temp_dir}")

    def create_snapshot(self, description: str = "Auto snapshot") -> Optional[Snapshot]:
        """
        Create a snapshot of the current document state.

        Args:
            description: Description of the snapshot

        Returns:
            Snapshot object or None if failed
        """
        if not self.file_parser.is_loaded():
            logger.warning("No document loaded, cannot create snapshot")
            return None

        try:
            # Generate snapshot filename
            self.snapshot_counter += 1
            snapshot_filename = f"snapshot_{self.snapshot_counter:04d}.FCStd"
            snapshot_path = os.path.join(self.temp_dir, snapshot_filename)

            # Save current document to snapshot
            doc = self.file_parser.document
            doc.saveAs(snapshot_path)

            # Get document info
            doc_info = self.file_parser.get_document_info()

            # Create snapshot object
            snapshot = Snapshot(
                timestamp=datetime.now(),
                description=description,
                file_path=snapshot_path,
                operation_count=len(self.snapshots),
                metadata={
                    'object_count': doc_info.get('object_count', 0),
                    'object_types': doc_info.get('object_types', {}),
                    'original_file': self.file_parser.file_path
                }
            )

            self.snapshots.append(snapshot)

            # Cleanup old snapshots if necessary
            self._cleanup_old_snapshots()

            logger.info(f"Snapshot created: {description} ({snapshot.operation_count})")
            return snapshot

        except Exception as e:
            logger.error(f"Failed to create snapshot: {e}")
            return None

    def rollback_to_snapshot(self, snapshot_index: int = -1) -> bool:
        """
        Rollback to a specific snapshot.

        Args:
            snapshot_index: Index of snapshot to restore (-1 for most recent)

        Returns:
            True if rollback successful
        """
        if not self.snapshots:
            logger.error("No snapshots available for rollback")
            return False

        try:
            # Get the snapshot
            snapshot = self.snapshots[snapshot_index]

            logger.info(f"Rolling back to snapshot: {snapshot.description}")

            # Close current document
            if self.file_parser.is_loaded():
                self.file_parser.close_document()

            # Load the snapshot
            success = self.file_parser.load_file(snapshot.file_path)

            if success:
                logger.info("Rollback successful")
                # Remove snapshots after the restored one
                if snapshot_index >= 0:
                    self.snapshots = self.snapshots[:snapshot_index + 1]
                return True
            else:
                logger.error("Failed to load snapshot")
                return False

        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False

    def rollback_last_operation(self) -> bool:
        """
        Rollback the last operation.

        Returns:
            True if rollback successful
        """
        if len(self.snapshots) < 2:
            logger.error("Need at least 2 snapshots to rollback")
            return False

        # Rollback to the second-to-last snapshot
        return self.rollback_to_snapshot(-2)

    def get_snapshot_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of snapshots.

        Returns:
            List of snapshot information
        """
        return [
            {
                'index': i,
                'timestamp': snap.timestamp.isoformat(),
                'description': snap.description,
                'operation_count': snap.operation_count,
                'object_count': snap.metadata.get('object_count', 0)
            }
            for i, snap in enumerate(self.snapshots)
        ]

    def can_rollback(self) -> bool:
        """Check if rollback is possible."""
        return len(self.snapshots) >= 1

    def get_current_snapshot_index(self) -> int:
        """Get the index of the current state."""
        return len(self.snapshots) - 1

    def _cleanup_old_snapshots(self):
        """Remove old snapshots if we exceed the maximum."""
        while len(self.snapshots) > self.max_snapshots:
            old_snapshot = self.snapshots.pop(0)

            # Delete the snapshot file
            try:
                if os.path.exists(old_snapshot.file_path):
                    os.remove(old_snapshot.file_path)
                    logger.debug(f"Removed old snapshot: {old_snapshot.file_path}")
            except Exception as e:
                logger.warning(f"Failed to remove old snapshot file: {e}")

    def clear_snapshots(self):
        """Clear all snapshots and free disk space."""
        for snapshot in self.snapshots:
            try:
                if os.path.exists(snapshot.file_path):
                    os.remove(snapshot.file_path)
            except Exception as e:
                logger.warning(f"Failed to remove snapshot file: {e}")

        self.snapshots = []
        self.snapshot_counter = 0
        logger.info("All snapshots cleared")

    def get_snapshot_storage_size(self) -> int:
        """
        Get total storage used by snapshots.

        Returns:
            Size in bytes
        """
        total_size = 0
        for snapshot in self.snapshots:
            try:
                if os.path.exists(snapshot.file_path):
                    total_size += os.path.getsize(snapshot.file_path)
            except:
                pass

        return total_size

    def __del__(self):
        """Cleanup temporary directory on deletion."""
        try:
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                logger.debug(f"Cleaned up temp directory: {self.temp_dir}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temp directory: {e}")


class OperationLog:
    """
    Maintains a log of all operations for audit trail.

    Separate from snapshots - provides a record of what happened.
    """

    def __init__(self):
        """Initialize operation log."""
        self.operations: List[Dict[str, Any]] = []

    def log_operation(
        self,
        operation_type: str,
        description: str,
        code: str,
        success: bool,
        metadata: Optional[Dict] = None
    ):
        """
        Log an operation.

        Args:
            operation_type: Type of operation (create, modify, delete, query)
            description: Human-readable description
            code: Code that was executed
            success: Whether operation succeeded
            metadata: Additional metadata
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': operation_type,
            'description': description,
            'code': code,
            'success': success,
            'metadata': metadata or {}
        }

        self.operations.append(entry)
        logger.debug(f"Logged operation: {description}")

    def get_operations(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent operations.

        Args:
            limit: Maximum number of operations to return

        Returns:
            List of operations
        """
        return self.operations[-limit:]

    def get_failed_operations(self) -> List[Dict[str, Any]]:
        """Get all failed operations."""
        return [op for op in self.operations if not op['success']]

    def clear_log(self):
        """Clear the operation log."""
        self.operations = []
        logger.info("Operation log cleared")

    def export_log(self, file_path: str) -> bool:
        """
        Export log to a JSON file.

        Args:
            file_path: Path to export to

        Returns:
            True if successful
        """
        try:
            import json

            with open(file_path, 'w') as f:
                json.dump({
                    'operations': self.operations,
                    'export_time': datetime.now().isoformat()
                }, f, indent=2)

            logger.info(f"Log exported to: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export log: {e}")
            return False
