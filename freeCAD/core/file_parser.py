"""FreeCAD file parser for loading and managing .FCStd files."""

import os
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class FreeCADFileParser:
    """
    Handles loading, parsing, and managing FreeCAD files (.FCStd).

    This class provides a safe interface for working with FreeCAD documents,
    including loading files, accessing objects, and managing document state.
    """

    def __init__(self, headless: bool = True):
        """
        Initialize the FreeCAD file parser.

        Args:
            headless: If True, run FreeCAD without GUI (default: True)
        """
        self.headless = headless
        self.document = None
        self.file_path: Optional[str] = None
        self._original_state: Optional[Dict] = None
        self._initialize_freecad()

    def _initialize_freecad(self):
        """Initialize FreeCAD environment."""
        try:
            import FreeCAD
            self.FreeCAD = FreeCAD
            logger.info("FreeCAD initialized successfully")
        except ImportError:
            logger.warning("FreeCAD not available. Running in mock mode.")
            self.FreeCAD = None

    def load_file(self, file_path: str) -> bool:
        """
        Load a FreeCAD file.

        Args:
            file_path: Path to the .FCStd file

        Returns:
            True if loaded successfully, False otherwise

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a valid FreeCAD file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not file_path.endswith('.FCStd'):
            raise ValueError(f"Invalid file type. Expected .FCStd, got: {file_path}")

        try:
            if self.FreeCAD:
                self.document = self.FreeCAD.openDocument(file_path)
                self.file_path = file_path
                self._capture_original_state()
                logger.info(f"Loaded file: {file_path}")
                return True
            else:
                logger.warning("FreeCAD not available. Cannot load file.")
                return False
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            return False

    def create_new_document(self, name: str = "Untitled") -> bool:
        """
        Create a new FreeCAD document.

        Args:
            name: Document name

        Returns:
            True if created successfully
        """
        try:
            if self.FreeCAD:
                self.document = self.FreeCAD.newDocument(name)
                self._capture_original_state()
                logger.info(f"Created new document: {name}")
                return True
            else:
                logger.warning("FreeCAD not available. Cannot create document.")
                return False
        except Exception as e:
            logger.error(f"Error creating document: {e}")
            return False

    def _capture_original_state(self):
        """Capture the original state of the document for rollback purposes."""
        if not self.document:
            return

        try:
            self._original_state = {
                'timestamp': datetime.now(),
                'object_count': len(self.document.Objects),
                'objects': [obj.Name for obj in self.document.Objects],
                'object_types': {obj.Name: obj.TypeId for obj in self.document.Objects}
            }
            logger.debug("Captured original document state")
        except Exception as e:
            logger.error(f"Error capturing state: {e}")

    def get_objects(self) -> List[Any]:
        """
        Get all objects in the current document.

        Returns:
            List of FreeCAD objects
        """
        if not self.document:
            return []

        try:
            return list(self.document.Objects)
        except Exception as e:
            logger.error(f"Error getting objects: {e}")
            return []

    def get_object_by_name(self, name: str) -> Optional[Any]:
        """
        Get an object by its name.

        Args:
            name: Object name

        Returns:
            FreeCAD object or None if not found
        """
        if not self.document:
            return None

        try:
            return self.document.getObject(name)
        except Exception as e:
            logger.error(f"Error getting object '{name}': {e}")
            return None

    def get_objects_by_type(self, type_id: str) -> List[Any]:
        """
        Get all objects of a specific type.

        Args:
            type_id: FreeCAD TypeId (e.g., 'Part::Box', 'Arch::Wall')

        Returns:
            List of matching objects
        """
        if not self.document:
            return []

        try:
            return [obj for obj in self.document.Objects if obj.TypeId == type_id]
        except Exception as e:
            logger.error(f"Error getting objects by type '{type_id}': {e}")
            return []

    def get_document_info(self) -> Dict[str, Any]:
        """
        Get information about the current document.

        Returns:
            Dictionary containing document information
        """
        if not self.document:
            return {'status': 'no_document_loaded'}

        try:
            objects = self.get_objects()
            object_types = {}
            for obj in objects:
                type_id = obj.TypeId
                object_types[type_id] = object_types.get(type_id, 0) + 1

            return {
                'name': self.document.Name,
                'file_path': self.file_path,
                'object_count': len(objects),
                'object_types': object_types,
                'objects': [{'name': obj.Name, 'type': obj.TypeId} for obj in objects]
            }
        except Exception as e:
            logger.error(f"Error getting document info: {e}")
            return {'status': 'error', 'message': str(e)}

    def save_file(self, file_path: Optional[str] = None) -> bool:
        """
        Save the current document.

        Args:
            file_path: Optional path to save to (if different from original)

        Returns:
            True if saved successfully
        """
        if not self.document:
            logger.error("No document to save")
            return False

        save_path = file_path or self.file_path
        if not save_path:
            logger.error("No file path specified")
            return False

        try:
            if self.FreeCAD:
                self.document.saveAs(save_path)
                self.file_path = save_path
                logger.info(f"Saved document to: {save_path}")
                return True
            else:
                logger.warning("FreeCAD not available. Cannot save file.")
                return False
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return False

    def recompute(self) -> bool:
        """
        Recompute the document to update all dependencies.

        Returns:
            True if recomputed successfully
        """
        if not self.document:
            return False

        try:
            self.document.recompute()
            logger.debug("Document recomputed")
            return True
        except Exception as e:
            logger.error(f"Error recomputing document: {e}")
            return False

    def close_document(self):
        """Close the current document."""
        if self.document and self.FreeCAD:
            try:
                self.FreeCAD.closeDocument(self.document.Name)
                logger.info("Document closed")
            except Exception as e:
                logger.error(f"Error closing document: {e}")

        self.document = None
        self.file_path = None
        self._original_state = None

    def is_loaded(self) -> bool:
        """Check if a document is currently loaded."""
        return self.document is not None

    def get_original_state(self) -> Optional[Dict]:
        """Get the original state of the document."""
        return self._original_state
