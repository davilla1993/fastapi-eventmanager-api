import re
from typing import Annotated

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

# E.164 : + suivi de 7 à 15 chiffres
_E164_RE = re.compile(r"^\+[1-9]\d{6,14}$")


class TelephoneE164(str):
    """Numéro de téléphone au format E.164 international. Ex: +22890123456"""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: object, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def _validate(cls, value: str) -> "TelephoneE164":
        if not _E164_RE.match(value):
            raise ValueError(
                f"Numéro de téléphone invalide : '{value}'. "
                "Format E.164 : '+' suivi de 7 à 15 chiffres (ex: +22890123456)."
            )
        return cls(value)


TelephoneE164Type = Annotated[TelephoneE164, ...]
