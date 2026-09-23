'''address_controller.py'''
import logging
from fastapi import APIRouter, Query
from models.address_model import CreateAddress, UpdateAddress
from repositories.address_repository import (
    insert_address,
    select_address_by_id,
    modify_address_by_id,
    remove_address_by_id,
    find_addresses_near,
)
from utilities.api_response_format import api_response_format

router = APIRouter(prefix="/address", tags=["Address"])
logger = logging.getLogger(__name__)


@router.post("/", status_code=201)
def create_address(address: CreateAddress):
    try:
        result = insert_address(address)
        return api_response_format(
            message="Address created successfully",
            data={"address": result.serialize()},
            status_code=201,
        )
    except Exception as e:
        logger.error(f"Failed to create address: {e}", exc_info=True)
        return api_response_format(message=str(e), status_code=500)


@router.get("/{address_id}")
def get_address_by_id(address_id: int):
    try:
        address = select_address_by_id(address_id)
        if not address:
            return api_response_format(message="Address not found", status_code=404)

        return api_response_format(
            message="Address retrieved successfully",
            data={"address": address.serialize()},
            status_code=200,
        )
    except Exception as e:
        logger.error(f"Failed to retrieve address id={address_id}: {e}", exc_info=True)
        return api_response_format(message=str(e), status_code=500)


@router.put("/{address_id}")
def update_address_by_id(address_id: int, address: UpdateAddress):
    try:
        result = modify_address_by_id(address_id, address)
        if not result:
            return api_response_format(message="Address not found", status_code=404)

        return api_response_format(
            message="Address updated successfully",
            data={"address": result.serialize()},
            status_code=200,
        )
    except Exception as e:
        logger.error(f"Failed to update address id={address_id}: {e}", exc_info=True)
        return api_response_format(message=str(e), status_code=500)


@router.delete("/{address_id}")
def delete_address_by_id(address_id: int):
    try:
        success = remove_address_by_id(address_id)
        if not success:
            return api_response_format(message="Address not found", status_code=404)

        return api_response_format(
            message="Address deleted successfully",
            status_code=200,
        )
    except Exception as e:
        logger.error(f"Failed to delete address id={address_id}: {e}", exc_info=True)
        return api_response_format(message=str(e), status_code=500)


@router.get("/")
def get_addresses_near(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    distance: float = Query(..., gt=0, description="Search radius in kilometers"),
):
    try:
        addresses = find_addresses_near(latitude, longitude, distance)
        return api_response_format(
            message="Addresses retrieved successfully",
            data={"addresses": [a.serialize() for a in addresses]},
            status_code=200,
        )
    except Exception as e:
        logger.error(f"Failed to search addresses: {e}", exc_info=True)
        return api_response_format(message=str(e), status_code=500)