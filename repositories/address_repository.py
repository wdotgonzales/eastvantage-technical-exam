from typing import List, Optional
from db.database import get_db
from models.address_model import Address, CreateAddress, UpdateAddress
import math

def insert_address(data: CreateAddress) -> Address:
    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO address
            (name, street, city, state, zip, country, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.name,
                data.street,
                data.city,
                data.state,
                data.zip,
                data.country,
                data.latitude,
                data.longitude,
            ),
        )
        address_id = cursor.lastrowid

    return select_address_by_id(address_id)


def select_address_by_id(address_id: int) -> Optional[Address]:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM address WHERE id = ?", (address_id,)
        ).fetchone()
        
        return Address.map(dict(row)) if row else None