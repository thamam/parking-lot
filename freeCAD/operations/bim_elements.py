"""BIM (Building Information Modeling) operations for FreeCAD."""

import logging
from typing import Optional, Tuple, List, Any

logger = logging.getLogger(__name__)


class BIMOperations:
    """
    Provides high-level operations for creating and manipulating BIM elements.

    This class wraps FreeCAD Arch module functionality for building modeling.
    """

    def __init__(self, document):
        """
        Initialize BIM operations.

        Args:
            document: FreeCAD document
        """
        self.document = document

        # Import FreeCAD modules
        try:
            import FreeCAD
            import Arch
            import Part
            self.FreeCAD = FreeCAD
            self.Arch = Arch
            self.Part = Part
        except ImportError:
            logger.warning("FreeCAD modules not available")
            self.FreeCAD = None
            self.Arch = None
            self.Part = None

    def create_wall(
        self,
        length: float,
        width: float,
        height: float,
        position: Optional[Tuple[float, float, float]] = None,
        align: str = "Center",
        name: str = "Wall"
    ) -> Optional[Any]:
        """
        Create a wall.

        Args:
            length: Wall length in mm
            width: Wall thickness in mm
            height: Wall height in mm
            position: (x, y, z) position in mm
            align: Alignment ("Center", "Left", "Right")
            name: Wall name

        Returns:
            Wall object or None
        """
        if not self.Arch or not self.document:
            logger.error("FreeCAD Arch module not available")
            return None

        try:
            # Create the wall
            wall = self.Arch.makeWall(
                baseobj=None,
                length=length,
                width=width,
                height=height,
                align=align
            )

            wall.Label = name

            # Set position if provided
            if position:
                wall.Placement.Base = self.FreeCAD.Vector(*position)

            self.document.recompute()
            logger.info(f"Created wall: {name} ({length}x{width}x{height})")
            return wall

        except Exception as e:
            logger.error(f"Failed to create wall: {e}")
            return None

    def create_structure(
        self,
        length: float,
        width: float,
        height: float,
        position: Optional[Tuple[float, float, float]] = None,
        name: str = "Structure"
    ) -> Optional[Any]:
        """
        Create a structural element (column, beam, etc.).

        Args:
            length: Length in mm
            width: Width in mm
            height: Height in mm
            position: (x, y, z) position in mm
            name: Structure name

        Returns:
            Structure object or None
        """
        if not self.Arch or not self.document:
            logger.error("FreeCAD Arch module not available")
            return None

        try:
            # Create the structure
            structure = self.Arch.makeStructure(
                baseobj=None,
                length=length,
                width=width,
                height=height
            )

            structure.Label = name

            # Set position if provided
            if position:
                structure.Placement.Base = self.FreeCAD.Vector(*position)

            self.document.recompute()
            logger.info(f"Created structure: {name} ({length}x{width}x{height})")
            return structure

        except Exception as e:
            logger.error(f"Failed to create structure: {e}")
            return None

    def create_window(
        self,
        width: float,
        height: float,
        position: Optional[Tuple[float, float, float]] = None,
        name: str = "Window"
    ) -> Optional[Any]:
        """
        Create a window.

        Args:
            width: Window width in mm
            height: Window height in mm
            position: (x, y, z) position in mm
            name: Window name

        Returns:
            Window object or None
        """
        if not self.Arch or not self.document:
            logger.error("FreeCAD Arch module not available")
            return None

        try:
            # Create the window
            window = self.Arch.makeWindow(
                baseobj=None,
                width=width,
                height=height
            )

            window.Label = name

            # Set position if provided
            if position:
                window.Placement.Base = self.FreeCAD.Vector(*position)

            self.document.recompute()
            logger.info(f"Created window: {name} ({width}x{height})")
            return window

        except Exception as e:
            logger.error(f"Failed to create window: {e}")
            return None

    def create_door(
        self,
        width: float,
        height: float,
        position: Optional[Tuple[float, float, float]] = None,
        name: str = "Door"
    ) -> Optional[Any]:
        """
        Create a door.

        Args:
            width: Door width in mm
            height: Door height in mm
            position: (x, y, z) position in mm
            name: Door name

        Returns:
            Door object or None
        """
        if not self.Arch or not self.document:
            logger.error("FreeCAD Arch module not available")
            return None

        try:
            # In FreeCAD, doors are typically windows with specific properties
            # For simplicity, we'll use makeWindow
            door = self.Arch.makeWindow(
                baseobj=None,
                width=width,
                height=height
            )

            door.Label = name

            # Set position if provided
            if position:
                door.Placement.Base = self.FreeCAD.Vector(*position)

            self.document.recompute()
            logger.info(f"Created door: {name} ({width}x{height})")
            return door

        except Exception as e:
            logger.error(f"Failed to create door: {e}")
            return None

    def create_floor(
        self,
        objects: Optional[List[Any]] = None,
        name: str = "Floor"
    ) -> Optional[Any]:
        """
        Create a floor containing other objects.

        Args:
            objects: List of objects to include in the floor
            name: Floor name

        Returns:
            Floor object or None
        """
        if not self.Arch or not self.document:
            logger.error("FreeCAD Arch module not available")
            return None

        try:
            # Create the floor
            floor = self.Arch.makeFloor(objectslist=objects or [])
            floor.Label = name

            self.document.recompute()
            logger.info(f"Created floor: {name}")
            return floor

        except Exception as e:
            logger.error(f"Failed to create floor: {e}")
            return None

    def create_building(
        self,
        objects: Optional[List[Any]] = None,
        name: str = "Building"
    ) -> Optional[Any]:
        """
        Create a building containing floors and other objects.

        Args:
            objects: List of objects to include in the building
            name: Building name

        Returns:
            Building object or None
        """
        if not self.Arch or not self.document:
            logger.error("FreeCAD Arch module not available")
            return None

        try:
            # Create the building
            building = self.Arch.makeBuilding(objectslist=objects or [])
            building.Label = name

            self.document.recompute()
            logger.info(f"Created building: {name}")
            return building

        except Exception as e:
            logger.error(f"Failed to create building: {e}")
            return None

    def create_site(
        self,
        objects: Optional[List[Any]] = None,
        name: str = "Site"
    ) -> Optional[Any]:
        """
        Create a site containing buildings and other objects.

        Args:
            objects: List of objects to include in the site
            name: Site name

        Returns:
            Site object or None
        """
        if not self.Arch or not self.document:
            logger.error("FreeCAD Arch module not available")
            return None

        try:
            # Create the site
            site = self.Arch.makeSite(objectslist=objects or [])
            site.Label = name

            self.document.recompute()
            logger.info(f"Created site: {name}")
            return site

        except Exception as e:
            logger.error(f"Failed to create site: {e}")
            return None

    def add_window_to_wall(
        self,
        window,
        wall,
        position_along_wall: float = 0.5
    ) -> bool:
        """
        Add a window to a wall.

        Args:
            window: Window object
            wall: Wall object
            position_along_wall: Position along wall (0.0 to 1.0)

        Returns:
            True if successful
        """
        if not self.Arch or not window or not wall:
            logger.error("Missing required objects")
            return False

        try:
            # Set the window's host to the wall
            if hasattr(window, 'Host'):
                window.Host = wall

            # Calculate position along the wall
            if hasattr(wall, 'Width') and hasattr(wall, 'Placement'):
                wall_length = wall.Width.Value
                offset = wall_length * position_along_wall

                # Adjust window position
                base_pos = wall.Placement.Base
                window.Placement.Base = self.FreeCAD.Vector(
                    base_pos.x + offset,
                    base_pos.y,
                    base_pos.z + 1000  # 1m above floor by default
                )

            self.document.recompute()
            logger.info(f"Added window {window.Label} to wall {wall.Label}")
            return True

        except Exception as e:
            logger.error(f"Failed to add window to wall: {e}")
            return False

    def create_room(
        self,
        length: float,
        width: float,
        height: float,
        position: Optional[Tuple[float, float, float]] = None,
        name: str = "Room"
    ) -> Optional[Dict[str, Any]]:
        """
        Create a simple room with 4 walls.

        Args:
            length: Room length in mm
            width: Room width in mm
            height: Wall height in mm
            position: (x, y, z) position of the room corner
            name: Room name prefix

        Returns:
            Dictionary with wall objects or None
        """
        if not self.Arch or not self.document:
            logger.error("FreeCAD Arch module not available")
            return None

        try:
            pos = position or (0, 0, 0)
            wall_thickness = 200  # 200mm default wall thickness

            # Create 4 walls
            walls = {}

            # Wall 1 (bottom, along X axis)
            walls['wall1'] = self.create_wall(
                length=length,
                width=wall_thickness,
                height=height,
                position=pos,
                name=f"{name}_Wall1"
            )

            # Wall 2 (right, along Y axis)
            walls['wall2'] = self.create_wall(
                length=width,
                width=wall_thickness,
                height=height,
                position=(pos[0] + length, pos[1], pos[2]),
                name=f"{name}_Wall2"
            )
            if walls['wall2']:
                # Rotate 90 degrees
                walls['wall2'].Placement.Rotation = self.FreeCAD.Rotation(
                    self.FreeCAD.Vector(0, 0, 1), 90
                )

            # Wall 3 (top, along X axis)
            walls['wall3'] = self.create_wall(
                length=length,
                width=wall_thickness,
                height=height,
                position=(pos[0], pos[1] + width, pos[2]),
                name=f"{name}_Wall3"
            )

            # Wall 4 (left, along Y axis)
            walls['wall4'] = self.create_wall(
                length=width,
                width=wall_thickness,
                height=height,
                position=pos,
                name=f"{name}_Wall4"
            )
            if walls['wall4']:
                # Rotate 90 degrees
                walls['wall4'].Placement.Rotation = self.FreeCAD.Rotation(
                    self.FreeCAD.Vector(0, 0, 1), 90
                )

            self.document.recompute()
            logger.info(f"Created room: {name}")
            return walls

        except Exception as e:
            logger.error(f"Failed to create room: {e}")
            return None

    def set_ifc_type(self, obj, ifc_type: str) -> bool:
        """
        Set the IFC type of a BIM object.

        Args:
            obj: BIM object
            ifc_type: IFC type string (e.g., 'Wall', 'Column', 'Beam')

        Returns:
            True if successful
        """
        if not obj:
            return False

        try:
            if hasattr(obj, 'IfcType'):
                obj.IfcType = ifc_type
                self.document.recompute()
                logger.info(f"Set IFC type of {obj.Label} to {ifc_type}")
                return True
            else:
                logger.warning(f"Object {obj.Label} does not support IFC types")
                return False

        except Exception as e:
            logger.error(f"Failed to set IFC type: {e}")
            return False

    def export_to_ifc(self, file_path: str, objects: Optional[List[Any]] = None) -> bool:
        """
        Export objects to IFC format.

        Args:
            file_path: Path to save IFC file
            objects: List of objects to export (None for all)

        Returns:
            True if successful
        """
        try:
            import importIFC

            # If no objects specified, export all
            if objects is None:
                objects = self.document.Objects

            # Export to IFC
            importIFC.export(objects, file_path)

            logger.info(f"Exported to IFC: {file_path}")
            return True

        except ImportError:
            logger.error("IFC export module not available")
            return False
        except Exception as e:
            logger.error(f"Failed to export to IFC: {e}")
            return False
