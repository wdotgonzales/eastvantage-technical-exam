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


def modify_address_by_id(address_id: int, data: UpdateAddress) -> Optional[Address]:
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return select_address_by_id(address_id)

    set_clause = ", ".join(f"{key} = ?" for key in update_data.keys())
    values = list(update_data.values()) + [address_id]

    with get_db() as conn:
        conn.execute(
            f"UPDATE address SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            values,
        )

    return select_address_by_id(address_id)


def remove_address_by_id(address_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM address WHERE id = ?", (address_id,)
        )
        return cursor.rowcount > 0