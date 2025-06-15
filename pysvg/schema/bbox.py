from pydantic import BaseModel, Field, ConfigDict


class BBox(BaseModel):
    model_config = ConfigDict(extra="forbid")

    x: float = Field(ge=0.0, description="X coordinate of the top-left corner")
    y: float = Field(ge=0.0, description="Y coordinate of the top-left corner")
    width: float = Field(ge=0.0, description="Width of the bounding box")
    height: float = Field(ge=0.0, description="Height of the bounding box")
