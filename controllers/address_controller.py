from fastapi import APIRouter, Query
from typing import Optional
from models.address_model import Address, CreateAddress, UpdateAddress
from repositories.address_repository import insert_address, select_address_by_id, modify_address_by_id, remove_address_by_id
from utilities.api_response_format import api_response_format

router = APIRouter(prefix="/address", tags=["Address"])

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
        return api_response_format(message=str(e), status_code=500)