from fastapi import APIRouter

from app.models.contact import (
    ContactRequest,
    ContactResponse
)

from app.services.contact_service import contact_service


router = APIRouter()


@router.post(
    "/contact",
    response_model=ContactResponse
)
async def contact(
    request: ContactRequest
):

    result = await contact_service.process_contact(
        request
    )

    return ContactResponse(**result)