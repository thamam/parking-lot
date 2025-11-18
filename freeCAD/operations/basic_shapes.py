"""Basic shape operations for FreeCAD."""

import logging
from typing import Optional, Tuple, Dict, Any

logger = logging.getLogger(__name__)


class BasicShapeOperations:
    """
    Provides high-level operations for creating and manipulating basic shapes.

    This class wraps FreeCAD Part module functionality with a simpler interface.
    """

    def __init__(self, document):
        """
        Initialize basic shape operations.

        Args:
            document: FreeCAD document
        """
        self.document = document

        # Import FreeCAD modules
        try:
            import FreeCAD
            import Part
            self.FreeCAD = FreeCAD
            self.Part = Part
        except ImportError:
            logger.warning("FreeCAD modules not available")
            self.FreeCAD = None
            self.Part = None

    def create_box(
        self,
        length: float,
        width: float,
        height: float,
        position: Optional[Tuple[float, float, float]] = None,
        name: str = "Box"
    ) -> Optional[Any]:
        """
        Create a box (rectangular cuboid).

        Args:
            length: Length in mm
            width: Width in mm
            height: Height in mm
            position: (x, y, z) position in mm
            name: Object name

        Returns:
            FreeCAD object or None
        """
        if not self.Part or not self.document:
            logger.error("FreeCAD not available")
            return None

        try:
            # Create the box
            if position:
                base_point = self.FreeCAD.Vector(*position)
                box = self.Part.makeBox(length, width, height, base_point)
            else:
                box = self.Part.makeBox(length, width, height)

            # Add to document
            obj = self.document.addObject("Part::Feature", name)
            obj.Shape = box

            self.document.recompute()
            logger.info(f"Created box: {name} ({length}x{width}x{height})")
            return obj

        except Exception as e:
            logger.error(f"Failed to create box: {e}")
            return None

    def create_cylinder(
        self,
        radius: float,
        height: float,
        position: Optional[Tuple[float, float, float]] = None,
        name: str = "Cylinder"
    ) -> Optional[Any]:
        """
        Create a cylinder.

        Args:
            radius: Radius in mm
            height: Height in mm
            position: (x, y, z) position in mm
            name: Object name

        Returns:
            FreeCAD object or None
        """
        if not self.Part or not self.document:
            logger.error("FreeCAD not available")
            return None

        try:
            # Create the cylinder
            if position:
                base_point = self.FreeCAD.Vector(*position)
                cylinder = self.Part.makeCylinder(radius, height, base_point)
            else:
                cylinder = self.Part.makeCylinder(radius, height)

            # Add to document
            obj = self.document.addObject("Part::Feature", name)
            obj.Shape = cylinder

            self.document.recompute()
            logger.info(f"Created cylinder: {name} (r={radius}, h={height})")
            return obj

        except Exception as e:
            logger.error(f"Failed to create cylinder: {e}")
            return None

    def create_sphere(
        self,
        radius: float,
        position: Optional[Tuple[float, float, float]] = None,
        name: str = "Sphere"
    ) -> Optional[Any]:
        """
        Create a sphere.

        Args:
            radius: Radius in mm
            position: (x, y, z) center position in mm
            name: Object name

        Returns:
            FreeCAD object or None
        """
        if not self.Part or not self.document:
            logger.error("FreeCAD not available")
            return None

        try:
            # Create the sphere
            if position:
                center = self.FreeCAD.Vector(*position)
                sphere = self.Part.makeSphere(radius, center)
            else:
                sphere = self.Part.makeSphere(radius)

            # Add to document
            obj = self.document.addObject("Part::Feature", name)
            obj.Shape = sphere

            self.document.recompute()
            logger.info(f"Created sphere: {name} (r={radius})")
            return obj

        except Exception as e:
            logger.error(f"Failed to create sphere: {e}")
            return None

    def create_cone(
        self,
        radius1: float,
        radius2: float,
        height: float,
        position: Optional[Tuple[float, float, float]] = None,
        name: str = "Cone"
    ) -> Optional[Any]:
        """
        Create a cone or truncated cone.

        Args:
            radius1: Bottom radius in mm
            radius2: Top radius in mm (0 for a point)
            height: Height in mm
            position: (x, y, z) position in mm
            name: Object name

        Returns:
            FreeCAD object or None
        """
        if not self.Part or not self.document:
            logger.error("FreeCAD not available")
            return None

        try:
            # Create the cone
            if position:
                base_point = self.FreeCAD.Vector(*position)
                cone = self.Part.makeCone(radius1, radius2, height, base_point)
            else:
                cone = self.Part.makeCone(radius1, radius2, height)

            # Add to document
            obj = self.document.addObject("Part::Feature", name)
            obj.Shape = cone

            self.document.recompute()
            logger.info(f"Created cone: {name} (r1={radius1}, r2={radius2}, h={height})")
            return obj

        except Exception as e:
            logger.error(f"Failed to create cone: {e}")
            return None

    def boolean_union(self, obj1, obj2, name: str = "Union") -> Optional[Any]:
        """
        Perform boolean union of two objects.

        Args:
            obj1: First object
            obj2: Second object
            name: Result object name

        Returns:
            Union object or None
        """
        if not self.Part or not self.document:
            logger.error("FreeCAD not available")
            return None

        try:
            union = self.document.addObject("Part::MultiFuse", name)
            union.Shapes = [obj1, obj2]

            self.document.recompute()
            logger.info(f"Created union: {name}")
            return union

        except Exception as e:
            logger.error(f"Failed to create union: {e}")
            return None

    def boolean_difference(self, base_obj, tool_obj, name: str = "Difference") -> Optional[Any]:
        """
        Perform boolean difference (subtract tool from base).

        Args:
            base_obj: Base object
            tool_obj: Tool object to subtract
            name: Result object name

        Returns:
            Difference object or None
        """
        if not self.Part or not self.document:
            logger.error("FreeCAD not available")
            return None

        try:
            diff = self.document.addObject("Part::Cut", name)
            diff.Base = base_obj
            diff.Tool = tool_obj

            self.document.recompute()
            logger.info(f"Created difference: {name}")
            return diff

        except Exception as e:
            logger.error(f"Failed to create difference: {e}")
            return None

    def boolean_intersection(self, obj1, obj2, name: str = "Intersection") -> Optional[Any]:
        """
        Perform boolean intersection of two objects.

        Args:
            obj1: First object
            obj2: Second object
            name: Result object name

        Returns:
            Intersection object or None
        """
        if not self.Part or not self.document:
            logger.error("FreeCAD not available")
            return None

        try:
            intersection = self.document.addObject("Part::MultiCommon", name)
            intersection.Shapes = [obj1, obj2]

            self.document.recompute()
            logger.info(f"Created intersection: {name}")
            return intersection

        except Exception as e:
            logger.error(f"Failed to create intersection: {e}")
            return None

    def move_object(
        self,
        obj,
        x: float = 0,
        y: float = 0,
        z: float = 0
    ) -> bool:
        """
        Move an object by a delta.

        Args:
            obj: Object to move
            x: X offset in mm
            y: Y offset in mm
            z: Z offset in mm

        Returns:
            True if successful
        """
        if not self.FreeCAD or not obj:
            logger.error("FreeCAD or object not available")
            return False

        try:
            current_pos = obj.Placement.Base
            new_pos = self.FreeCAD.Vector(
                current_pos.x + x,
                current_pos.y + y,
                current_pos.z + z
            )
            obj.Placement.Base = new_pos

            self.document.recompute()
            logger.info(f"Moved object {obj.Name} by ({x}, {y}, {z})")
            return True

        except Exception as e:
            logger.error(f"Failed to move object: {e}")
            return False

    def rotate_object(
        self,
        obj,
        axis: Tuple[float, float, float],
        angle_degrees: float
    ) -> bool:
        """
        Rotate an object around an axis.

        Args:
            obj: Object to rotate
            axis: (x, y, z) rotation axis
            angle_degrees: Rotation angle in degrees

        Returns:
            True if successful
        """
        if not self.FreeCAD or not obj:
            logger.error("FreeCAD or object not available")
            return False

        try:
            axis_vector = self.FreeCAD.Vector(*axis)
            rotation = self.FreeCAD.Rotation(axis_vector, angle_degrees)

            obj.Placement.Rotation = rotation

            self.document.recompute()
            logger.info(f"Rotated object {obj.Name} by {angle_degrees}° around {axis}")
            return True

        except Exception as e:
            logger.error(f"Failed to rotate object: {e}")
            return False

    def scale_object(
        self,
        obj,
        scale_x: float = 1.0,
        scale_y: float = 1.0,
        scale_z: float = 1.0
    ) -> bool:
        """
        Scale an object (non-uniform scaling).

        Note: This requires Draft module.

        Args:
            obj: Object to scale
            scale_x: X scale factor
            scale_y: Y scale factor
            scale_z: Z scale factor

        Returns:
            True if successful
        """
        try:
            import Draft

            scale_vector = self.FreeCAD.Vector(scale_x, scale_y, scale_z)
            Draft.scale(obj, scale_vector, copy=False)

            self.document.recompute()
            logger.info(f"Scaled object {obj.Name} by ({scale_x}, {scale_y}, {scale_z})")
            return True

        except ImportError:
            logger.error("Draft module not available for scaling")
            return False
        except Exception as e:
            logger.error(f"Failed to scale object: {e}")
            return False
