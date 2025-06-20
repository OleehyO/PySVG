from abc import ABC, abstractmethod
from typing import Any, Tuple
from typing_extensions import override

from pysvg.schema import AppearanceConfig, TransformConfig, BaseSVGConfig


class BaseSVGComponent(ABC):
    """
    Abstract base class for all SVG components.

    This class defines the common interface that all SVG components should implement,
    including common properties (appearance, transform) and abstract methods that
    must be implemented by each specific component type.
    """

    def __init__(
        self,
        config: BaseSVGConfig | None = None,
        appearance: AppearanceConfig | None = None,
        transform: TransformConfig | None = None,
    ):
        """
        Initialize the base SVG component.

        Args:
            appearance: External appearance configuration
            transform: Transform configuration
        """
        self.config = config
        self.appearance = appearance
        self.transform = transform

    @property
    @abstractmethod
    def central_point(self) -> Tuple[float, float]:
        """
        Get the central point of the component.

        This property must be implemented by subclasses to return the central point
        of the specific component type. The return type may vary based on the
        component's coordinate system and representation.

        Returns:
            The central point of the component
        """
        raise NotImplementedError("Subclasses must implement this property")

    @abstractmethod
    def to_svg_element(self) -> str:
        """
        Generate the complete SVG element string.

        Returns:
            Complete SVG element as XML string
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def restrict_size(self, max_width: float, max_height: float) -> "BaseSVGComponent":
        """
        Restrict the size of the component to a maximum width and height.

        Args:
            max_width: Maximum width
            max_height: Maximum height

        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Subclasses must implement this method")

    def has_transform(self) -> bool:
        """Check if the component has any transforms."""
        return self.transform is not None

    # Transform methods
    def move(self, x: float, y: float) -> "BaseSVGComponent":
        """
        Move the component to a specified position.

        Args:
            x: X coordinate to move to
            y: Y coordinate to move to

        Returns:
            Self for method chaining
        """
        self.transform.translate = (x, y)
        return self

    def move_by(self, dx: float, dy: float) -> "BaseSVGComponent":
        """
        Move the component by a specified offset.

        Args:
            dx: X offset to move by
            dy: Y offset to move by

        Returns:
            Self for method chaining
        """
        current_translate = self.transform.translate or (0, 0)
        new_x = current_translate[0] + dx
        new_y = current_translate[1] + dy
        self.transform.translate = (new_x, new_y)
        return self

    def rotate(
        self, angle: float | Tuple[float, float, float], around_center: bool = True
    ) -> "BaseSVGComponent":
        """
        Rotate the component by a specified angle.

        Args:
            angle: Rotation angle in degrees
            around_center: If True, rotate around component center; if False, rotate around origin

        Returns:
            Self for method chaining
        """
        if around_center:
            cx, cy = self.central_point
            self.transform.rotate = (angle, cx, cy)
        else:
            self.transform.rotate = angle
        return self

    def scale(self, scale_factor: float | Tuple[float, float]) -> "BaseSVGComponent":
        """
        Scale the component by a specified factor.

        Args:
            scale_factor: Scale factor. Can be a single number (uniform scaling)
                         or tuple (sx, sy) for different scaling in x and y directions

        Returns:
            Self for method chaining
        """
        assert hasattr(self, "transform"), "Component must have transform attribute"
        assert isinstance(self.transform, TransformConfig), "Transform must be TransformConfig"
        self.transform.scale = scale_factor
        return self

    def skew(self, skew_x: float | None = None, skew_y: float | None = None) -> "BaseSVGComponent":
        """
        Apply skew transform to the component.

        Args:
            skew_x: X-axis skew angle in degrees (optional)
            skew_y: Y-axis skew angle in degrees (optional)

        Returns:
            Self for method chaining
        """
        if skew_x is not None:
            self.transform.skew_x = skew_x
        if skew_y is not None:
            self.transform.skew_y = skew_y
        return self

    def reset_transform(self) -> "BaseSVGComponent":
        """
        Reset all transforms to default values.

        Returns:
            Self for method chaining
        """
        self.transform.reset()
        return self

    def reset_appearance(self) -> "BaseSVGComponent":
        """
        Reset all appearance to default values.

        Returns:
            Self for method chaining
        """
        self.appearance.reset()
        return self
