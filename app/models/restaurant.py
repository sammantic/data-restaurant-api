from typing import List, Optional
from pydantic import BaseModel, field_validator

class Coord(BaseModel):
    latitude: float
    longitude: float

class Address(BaseModel):
    building: str
    street: str
    zipcode: int
    coord: Optional[Coord] = None

    @field_validator('coord', mode="before")
    def validate_coord(cls, v):
        if isinstance(v, list) and len(v) == 2:
            return Coord(latitude=v[1], longitude=v[0])
        raise ValueError("Coord should be a list with two elements representing longitude and latitude")

class RestaurantData(BaseModel):
    name: str
    address: Address
    borough: str
    class Config:
        allow_population_by_field_name = True