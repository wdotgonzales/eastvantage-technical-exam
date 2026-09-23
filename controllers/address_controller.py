from fastapi import APIRouter, Query
from typing import Optional
from models.address_model import Address, CreateAddress, UpdateAddress
from repositories.address_repository import insert_address
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