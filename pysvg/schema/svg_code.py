from pydantic import BaseModel, Field, ConfigDict


class SVGCode(BaseModel):
    """SVG or SVG content component code"""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(description="SVG code")

    def __init__(self, code: str | None = None, **data):
        if code is not None:
            super().__init__(code=code, **data)
        else:
            super().__init__(**data)

    def __hash__(self):
        """Make SVGCode hashable so it can be used as a dictionary key"""
        return hash(self.code)

    def __eq__(self, other):
        """Define equality comparison"""
        if isinstance(other, SVGCode):
            return self.code == other.code
        return False
