from pydantic import BaseModel, EmailStr, Field

from app.shared.types.telephone_e164 import TelephoneE164


class OrganizerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255, examples=["Les Productions du Sud"])
    email: EmailStr = Field(examples=["contact@productions-du-sud.fr"])
    telephone: TelephoneE164 | None = Field(default=None, examples=["+22890123456"])
    website: str | None = Field(default=None, max_length=500, examples=["https://productions-du-sud.fr"])  # noqa: E501
    description: str | None = Field(
        default=None,
        max_length=2000,
        examples=["Producteur d'événements culturels basé à Marseille depuis 2010."],
    )


class OrganizerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255, examples=["Les Productions du Sud"])  # noqa: E501
    email: EmailStr | None = Field(default=None, examples=["contact@productions-du-sud.fr"])  # noqa: E501
    telephone: TelephoneE164 | None = Field(default=None, examples=["+22890123456"])
    website: str | None = Field(default=None, max_length=500, examples=["https://productions-du-sud.fr"])  # noqa: E501
    description: str | None = Field(default=None, max_length=2000)