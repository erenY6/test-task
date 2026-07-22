from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ContactRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User name"
    )

    email: EmailStr

    phone: str = Field(
        ...,
        min_length=6,
        max_length=30
    )

    comment: str = Field(
        ...,
        min_length=10,
        max_length=2000
    )


class ContactResponse(BaseModel):
    success: bool
    message: str
    ai_analysis: Optional[dict] = None