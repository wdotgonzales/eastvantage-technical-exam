'''address_repository.py'''
import logging
from typing import List, Optional
from db.database import get_db
from models.address_model import Address, CreateAddress, UpdateAddress
import math

logger = logging.getLogger(__name__)


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

    logger.info(f"Inserted address id={address_id}")
    return select_address_by_id(address_id)


def select_address_by_id(address_id: int) -> Optional[Address]:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM address WHERE id = ?", (address_id,)
        ).fetchone()

        if not row:
            logger.warning(f"Address id={address_id} not found")
            return None

        return Address.map(dict(row))


def modify_address_by_id(address_id: int, data: UpdateAddress) -> Optional[Address]:
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        logger.info(f"No fields to update for address id={address_id}, skipping write")
        return select_address_by_id(address_id)

    set_clause = ", ".join(f"{key} = ?" for key in update_data.keys())
    values = list(update_data.values()) + [address_id]

    with get_db() as conn:
        conn.execute(
            f"UPDATE address SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            values,
        )

    logger.info(f"Updated address id={address_id}, fields={list(update_data.keys())}")
    return select_address_by_id(address_id)


def remove_address_by_id(address_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM address WHERE id = ?", (address_id,)
        )
        deleted = cursor.rowcount > 0

    if deleted:
        logger.info(f"Deleted address id={address_id}")
    else:
        logger.warning(f"Attempted to delete non-existent address id={address_id}")

    return deleted


def find_addresses_near(latitude: float, longitude: float, distance_km: float) -> List[Address]:
    '''
    Uses a bounding-box pre-filter in SQL to cut down the candidate set,
    then applies the precise haversine formula only to rows inside that
    box.
    '''
    lat_delta = distance_km / 111.0  # ~111km per degree latitude, constant
    lon_delta = distance_km / (111.0 * math.cos(math.radians(latitude)) or 1e-9)

    min_lat, max_lat = latitude - lat_delta, latitude + lat_delta
    min_lon, max_lon = longitude - lon_delta, longitude + lon_delta

    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT * FROM address
            WHERE latitude BETWEEN ? AND ?
            AND longitude BETWEEN ? AND ?
            """,
            (min_lat, max_lat, min_lon, max_lon),
        ).fetchall()

    results = []
    for row in rows:
        row_dict = dict(row)
        d = _haversine_km(latitude, longitude, row_dict["latitude"], row_dict["longitude"])
        if d <= distance_km:
            row_dict["distance_km"] = round(d, 2)
            results.append(Address.map(row_dict))

    results.sort(key=lambda a: a.distance_km)
    logger.info(
        f"Search near ({latitude}, {longitude}) within {distance_km}km "
        f"found {len(results)} of {len(rows)} candidates in bounding box"
    )
    return results


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    '''
    Works out the distance in km between two points on Earth.
    We can't just use normal straight-line math because the Earth
    is round, not flat, so this formula bends the "ruler" to match
    the curve of the planet.
    '''
    R = 6371  # Earth's radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))