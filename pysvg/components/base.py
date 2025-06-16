from abc import ABC, abstractmethod
from typing import Tuple

from pysvg.logger import get_logger
from pysvg.schema import AppearanceConfig, BBox, ComponentConfig, TransformConfig

_logger = get_logger(__name__)


class BaseSVGComponent(ABC):
    """
    Abstract base class for all SVG components.

    This class defines the common interface that all SVG components should implement,
    including common properties (appearance, transform) and abstract methods that
    must be implemented by each specific component type.
    """

    def __init__(
        self,
        config: ComponentConfig | None = None,
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
    def central_point_relative(self) -> Tuple[float, float]:
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
    def get_bounding_box(self) -> BBox:
        """
        Get the bounding box of the component using **absolute coordinates**.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def to_svg_element(self) -> str:
        """
        Generate the complete SVG element string.

        Returns:
            Complete SVG element as XML string
        """
        raise NotImplementedError("Subclasses must implement this method")

    @property
    def central_point(self) -> Tuple[float, float]:
        """
        Get the absolute central point of the component.

        If transform is not set, returns the relative central point with a warning.
        If transform is set, returns the central point with translation applied.

        Returns:
            Tuple[float, float]: The absolute (x, y) coordinates of the central point
        """
        relative_x, relative_y = self.central_point_relative

        if not self.has_transform():
            _logger.warning(
                f"{self.__class__.__name__} has no transform, returning relative central point"
            )
            return relative_x, relative_y

        translate = self.transform.translate or (0, 0)
        return relative_x + translate[0], relative_y + translate[1]

    def get_attr_dict(self) -> dict[str, str]:
        """
        Get the attributes of the component as a dictionary.
        """
        attr = {}
        if hasattr(self, "config") and isinstance(self.config, ComponentConfig):
            attr.update(self.config.to_svg_dict())
        if hasattr(self, "appearance") and isinstance(self.appearance, AppearanceConfig):
            attr.update(self.appearance.to_svg_dict())
        if hasattr(self, "transform") and isinstance(self.transform, TransformConfig):
            attr.update(self.transform.to_svg_dict())
        attr = {k: str(v) for k, v in attr.items()}
        return attr

    def restrict_size(self, max_width: float, max_height: float) -> "BaseSVGComponent":
        """
        Restrict the size of the component to a maximum width and height.
        Maintains the aspect ratio by using the smaller scaling factor.

        Args:
            max_width: Maximum width
            max_height: Maximum height

        Returns:
            Self for method chaining
        """
        bbox = self.get_bounding_box()
        current_width = bbox.width
        current_height = bbox.height

        # Calculate scale factors for both dimensions
        width_scale = max_width / current_width if current_width > 0 else 1.0
        height_scale = max_height / current_height if current_height > 0 else 1.0

        # Use the smaller scale factor to maintain aspect ratio
        scale_factor = min(width_scale, height_scale)

        # Only apply scaling if we need to reduce the size
        if scale_factor < 1.0:
            self.scale(scale_factor)
        else:
            _logger.info(
                f"Component {self.__class__.__name__} is already smaller than the maximum size"
            )

        return self

    def has_transform(self) -> bool:
        """Check if the component has any transforms."""
        return self.transform is not None and isinstance(self.transform, TransformConfig)

    def move(self, cx: float, cy: float) -> "BaseSVGComponent":
        """
        Move the component to a specified position.

        Note:
            Coordinates are based on the central point of the component.

        Args:
            cx: central point x coordinate to move to
            cy: central point y coordinate to move to

        Returns:
            Self for method chaining
        """
        self.set_cpoint_to_lefttop()
        self.move_by(cx, cy)
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

    def set_cpoint_to_lefttop(self) -> "BaseSVGComponent":
        """
        Set the central point of the component to the left top corner
        """
        # cp_x, cp_y = self.central_point_relative
        # self.move_by(-cp_x, -cp_y)
        cp_x, cp_y = self.central_point
        self.move_by(-cp_x, -cp_y)
        return self

    def rotate(
        self, angle: float | Tuple[float, float, float], around_center_relative: bool = True
    ) -> "BaseSVGComponent":
        """
        Rotate the component by a specified angle.

        Args:
            angle: Rotation angle in degrees
            around_center_relative: If True, rotate around component center (relative); if False, rotate around origin

        Returns:
            Self for method chaining
        """
        if around_center_relative:
            cx, cy = self.central_point_relative
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
