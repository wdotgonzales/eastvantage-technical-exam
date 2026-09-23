from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Address:
    def __init__(self):
        self.id: Optional[int] = None
        self.name: Optional[str] = None
        self.street: Optional[str] = None
        self.city: Optional[str] = None
        self.state: Optional[str] = None
        self.zip: Optional[str] = None
        self.country: Optional[str] = None
        self.latitude: Optional[float] = None
        self.longitude: Optional[float] = None
        self.created_at: Optional[datetime] = None
        self.updated_at: Optional[datetime] = None
        self.distance_km: Optional[float] = None

    @staticmethod
    def map(row: dict) -> "Address | None":
        if not row:
            return None

        a = Address()
        a.id = row.get("id")
        a.name = row.get("name")
        a.street = row.get("street")
        a.city = row.get("city")
        a.state = row.get("state")
        a.zip = row.get("zip")
        a.country = row.get("country")
        a.latitude = row.get("latitude")
        a.longitude = row.get("longitude")
        a.created_at = row.get("created_at")
        a.updated_at = row.get("updated_at")
        a.distance_km = row.get("distance_km")
        return a

    def serialize(self) -> dict:
        return AddressSchema.model_validate(self).model_dump(by_alias=True)


class AddressSchema(BaseModel):
    id: int
    name: str
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    latitude: float
    longitude: float
    distance_km: Optional[float] = None

    class Config:
        from_attributes = True


class CreateAddress(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class UpdateAddress(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)