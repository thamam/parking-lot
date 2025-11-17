"""Operations modules for common FreeCAD tasks."""

from .basic_shapes import BasicShapeOperations
from .bim_elements import BIMOperations
from .properties import PropertyOperations

__all__ = [
    'BasicShapeOperations',
    'BIMOperations',
    'PropertyOperations'
]
