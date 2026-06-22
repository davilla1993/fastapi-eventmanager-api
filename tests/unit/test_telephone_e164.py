import pytest
from pydantic import BaseModel, ValidationError

from app.shared.types.telephone_e164 import TelephoneE164


class _Model(BaseModel):
    tel: TelephoneE164


# ── Cas valides ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value",
    [
        "+22890123456",  # Togo mobile
        "+33142345678",  # France fixe
        "+12025550123",  # USA
        "+447911123456",  # UK
        "+2250700000000",  # Côte d'Ivoire
    ],
)
def test_telephone_valide(value: str) -> None:
    assert _Model(tel=value).tel == value


# ── Cas invalides ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value",
    [
        "0612345678",  # sans indicatif
        "+336",  # trop court
        "+336123456789012345",  # trop long (> 15 chiffres)
        "+0612345678",  # indicatif commence par 0
        "336-12-34-56-78",  # tirets
        "",  # vide
    ],
)
def test_telephone_invalide(value: str) -> None:
    with pytest.raises(ValidationError):
        _Model(tel=value)


# ── Sérialisation ─────────────────────────────────────────────────────────────


def test_telephone_serialise_en_str() -> None:
    m = _Model(tel="+22890123456")
    assert m.model_dump()["tel"] == "+22890123456"
    assert isinstance(m.model_dump()["tel"], str)
