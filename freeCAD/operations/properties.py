"""Property modification operations for FreeCAD objects."""

import logging
from typing import Tuple, Optional, Any, Dict

logger = logging.getLogger(__name__)


class PropertyOperations:
    """
    Provides high-level operations for modifying object properties.

    Handles colors, materials, visibility, labels, and other properties.
    """

    def __init__(self, document):
        """
        Initialize property operations.

        Args:
            document: FreeCAD document
        """
        self.document = document

        # Import FreeCAD modules
        try:
            import FreeCAD
            self.FreeCAD = FreeCAD
        except ImportError:
            logger.warning("FreeCAD not available")
            self.FreeCAD = None

    def set_color(
        self,
        obj,
        color: Tuple[float, float, float],
        transparency: int = 0
    ) -> bool:
        """
        Set the color of an object.

        Args:
            obj: FreeCAD object
            color: (R, G, B) tuple with values 0.0-1.0
            transparency: Transparency value 0-100

        Returns:
            True if successful
        """
        if not obj or not hasattr(obj, 'ViewObject'):
            logger.error("Object has no ViewObject")
            return False

        try:
            obj.ViewObject.ShapeColor = color
            if transparency > 0:
                obj.ViewObject.Transparency = min(100, max(0, transparency))

            logger.info(f"Set color of {obj.Label} to {color}")
            return True

        except Exception as e:
            logger.error(f"Failed to set color: {e}")
            return False

    def set_color_rgb(
        self,
        obj,
        r: int,
        g: int,
        b: int,
        transparency: int = 0
    ) -> bool:
        """
        Set the color using RGB values (0-255).

        Args:
            obj: FreeCAD object
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
            transparency: Transparency value 0-100

        Returns:
            True if successful
        """
        # Convert RGB to 0.0-1.0 range
        color = (r / 255.0, g / 255.0, b / 255.0)
        return self.set_color(obj, color, transparency)

    def set_transparency(self, obj, transparency: int) -> bool:
        """
        Set the transparency of an object.

        Args:
            obj: FreeCAD object
            transparency: Transparency value 0-100 (0=opaque, 100=transparent)

        Returns:
            True if successful
        """
        if not obj or not hasattr(obj, 'ViewObject'):
            logger.error("Object has no ViewObject")
            return False

        try:
            obj.ViewObject.Transparency = min(100, max(0, transparency))
            logger.info(f"Set transparency of {obj.Label} to {transparency}")
            return True

        except Exception as e:
            logger.error(f"Failed to set transparency: {e}")
            return False

    def set_visibility(self, obj, visible: bool) -> bool:
        """
        Set the visibility of an object.

        Args:
            obj: FreeCAD object
            visible: True to show, False to hide

        Returns:
            True if successful
        """
        if not obj or not hasattr(obj, 'ViewObject'):
            logger.error("Object has no ViewObject")
            return False

        try:
            obj.ViewObject.Visibility = visible
            logger.info(f"Set visibility of {obj.Label} to {visible}")
            return True

        except Exception as e:
            logger.error(f"Failed to set visibility: {e}")
            return False

    def set_label(self, obj, label: str) -> bool:
        """
        Set the label (display name) of an object.

        Args:
            obj: FreeCAD object
            label: New label

        Returns:
            True if successful
        """
        if not obj:
            logger.error("No object provided")
            return False

        try:
            obj.Label = label
            logger.info(f"Set label to {label}")
            return True

        except Exception as e:
            logger.error(f"Failed to set label: {e}")
            return False

    def set_material(self, obj, material_name: str) -> bool:
        """
        Set the material of an object.

        Args:
            obj: FreeCAD object
            material_name: Material name (e.g., 'Concrete', 'Steel', 'Wood')

        Returns:
            True if successful
        """
        if not obj:
            logger.error("No object provided")
            return False

        try:
            # Check if object has Material property
            if hasattr(obj, 'Material'):
                # Simple material assignment
                # In a full implementation, we'd use material library
                obj.Material = material_name
                logger.info(f"Set material of {obj.Label} to {material_name}")
                return True
            else:
                logger.warning(f"Object {obj.Label} does not support materials")
                return False

        except Exception as e:
            logger.error(f"Failed to set material: {e}")
            return False

    def set_line_width(self, obj, width: float) -> bool:
        """
        Set the line width for object edges.

        Args:
            obj: FreeCAD object
            width: Line width in pixels

        Returns:
            True if successful
        """
        if not obj or not hasattr(obj, 'ViewObject'):
            logger.error("Object has no ViewObject")
            return False

        try:
            obj.ViewObject.LineWidth = width
            logger.info(f"Set line width of {obj.Label} to {width}")
            return True

        except Exception as e:
            logger.error(f"Failed to set line width: {e}")
            return False

    def set_display_mode(self, obj, mode: str) -> bool:
        """
        Set the display mode of an object.

        Args:
            obj: FreeCAD object
            mode: Display mode ('Flat Lines', 'Shaded', 'Wireframe', etc.)

        Returns:
            True if successful
        """
        if not obj or not hasattr(obj, 'ViewObject'):
            logger.error("Object has no ViewObject")
            return False

        try:
            obj.ViewObject.DisplayMode = mode
            logger.info(f"Set display mode of {obj.Label} to {mode}")
            return True

        except Exception as e:
            logger.error(f"Failed to set display mode: {e}")
            return False

    def get_properties(self, obj) -> Dict[str, Any]:
        """
        Get all properties of an object.

        Args:
            obj: FreeCAD object

        Returns:
            Dictionary of properties
        """
        if not obj:
            return {}

        try:
            properties = {
                'Name': obj.Name,
                'Label': obj.Label,
                'TypeId': obj.TypeId,
            }

            # Add geometric properties if available
            if hasattr(obj, 'Shape'):
                properties['Shape'] = {
                    'Volume': getattr(obj.Shape, 'Volume', None),
                    'Area': getattr(obj.Shape, 'Area', None),
                }

            # Add placement
            if hasattr(obj, 'Placement'):
                placement = obj.Placement
                properties['Placement'] = {
                    'Base': (placement.Base.x, placement.Base.y, placement.Base.z),
                    'Rotation': placement.Rotation.Axis,
                }

            # Add visual properties
            if hasattr(obj, 'ViewObject'):
                vo = obj.ViewObject
                properties['Visual'] = {
                    'ShapeColor': getattr(vo, 'ShapeColor', None),
                    'Transparency': getattr(vo, 'Transparency', None),
                    'Visibility': getattr(vo, 'Visibility', None),
                    'DisplayMode': getattr(vo, 'DisplayMode', None),
                }

            return properties

        except Exception as e:
            logger.error(f"Failed to get properties: {e}")
            return {}

    def copy_properties(self, source_obj, target_obj, property_types: Optional[list] = None) -> bool:
        """
        Copy properties from source object to target object.

        Args:
            source_obj: Source object
            target_obj: Target object
            property_types: List of property types to copy (None for all)

        Returns:
            True if successful
        """
        if not source_obj or not target_obj:
            logger.error("Source or target object missing")
            return False

        try:
            # Default to copying visual properties
            if property_types is None:
                property_types = ['color', 'transparency', 'visibility', 'display_mode']

            if 'color' in property_types and hasattr(source_obj, 'ViewObject'):
                self.set_color(target_obj, source_obj.ViewObject.ShapeColor)

            if 'transparency' in property_types and hasattr(source_obj, 'ViewObject'):
                self.set_transparency(target_obj, source_obj.ViewObject.Transparency)

            if 'visibility' in property_types and hasattr(source_obj, 'ViewObject'):
                self.set_visibility(target_obj, source_obj.ViewObject.Visibility)

            if 'display_mode' in property_types and hasattr(source_obj, 'ViewObject'):
                self.set_display_mode(target_obj, source_obj.ViewObject.DisplayMode)

            logger.info(f"Copied properties from {source_obj.Label} to {target_obj.Label}")
            return True

        except Exception as e:
            logger.error(f"Failed to copy properties: {e}")
            return False

    def set_dimension_property(self, obj, property_name: str, value: float) -> bool:
        """
        Set a dimensional property (Length, Width, Height, Radius, etc.).

        Args:
            obj: FreeCAD object
            property_name: Property name
            value: New value in mm

        Returns:
            True if successful
        """
        if not obj:
            logger.error("No object provided")
            return False

        try:
            if hasattr(obj, property_name):
                setattr(obj, property_name, value)
                if self.document:
                    self.document.recompute()
                logger.info(f"Set {property_name} of {obj.Label} to {value}")
                return True
            else:
                logger.warning(f"Object {obj.Label} does not have property {property_name}")
                return False

        except Exception as e:
            logger.error(f"Failed to set dimension property: {e}")
            return False

    def batch_set_color(self, objects: list, color: Tuple[float, float, float]) -> int:
        """
        Set the same color for multiple objects.

        Args:
            objects: List of objects
            color: (R, G, B) tuple

        Returns:
            Number of objects successfully updated
        """
        count = 0
        for obj in objects:
            if self.set_color(obj, color):
                count += 1

        logger.info(f"Set color for {count}/{len(objects)} objects")
        return count

    def batch_set_visibility(self, objects: list, visible: bool) -> int:
        """
        Set visibility for multiple objects.

        Args:
            objects: List of objects
            visible: True to show, False to hide

        Returns:
            Number of objects successfully updated
        """
        count = 0
        for obj in objects:
            if self.set_visibility(obj, visible):
                count += 1

        logger.info(f"Set visibility for {count}/{len(objects)} objects")
        return count
