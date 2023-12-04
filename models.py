# models.py

from pydantic import BaseModel, Field
from typing import Optional


class Disc(BaseModel):
    Manufacturer: str
    Name: str
    Speed: float
    Glide: float
    Turn: float
    Fade: float
    Diameter: float
    Height: float
    RimDepth: float
    RimWidth: float
    Distance: Optional[int] = None
