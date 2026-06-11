from math import ceil
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class PaginationParams:
    def __init__(
        self,
        page: Annotated[int, Query(ge=1, description="Numéro de page")] = 1,
        size: Annotated[int, Query(ge=1, le=100, description="Éléments par page")] = 20,
    ) -> None:
        self.page = page
        self.size = size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class PaginatedResponse[T](BaseModel):
    items: list[T]
    page: int
    size: int
    total: int
    pages: int

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int,
        size: int,
    ) -> "PaginatedResponse[T]":
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=ceil(total / size) if size > 0 else 0,
        )
