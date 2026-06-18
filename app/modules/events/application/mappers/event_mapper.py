from app.modules.events.api.dto.responses.event_responses import (
    ConcertRead,
    ConcertReadDetail,
    ConferenceRead,
    ConferenceReadDetail,
    TheatreRead,
    TheatreReadDetail,
)
from app.modules.events.domain.entities.event import Event, EventType


def _get_read_class(  # noqa: E501
    event_type: str,
) -> type[ConcertRead | TheatreRead | ConferenceRead]:
    if event_type == EventType.CONCERT:
        return ConcertRead
    if event_type == EventType.THEATRE:
        return TheatreRead
    return ConferenceRead


def _get_detail_class(
    event_type: str,
) -> type[ConcertReadDetail | TheatreReadDetail | ConferenceReadDetail]:
    if event_type == EventType.CONCERT:
        return ConcertReadDetail
    if event_type == EventType.THEATRE:
        return TheatreReadDetail
    return ConferenceReadDetail


class EventMapper:
    @staticmethod
    def to_read(event: Event) -> ConcertRead | TheatreRead | ConferenceRead:
        cls = _get_read_class(event.event_type)
        return cls.model_validate(event)

    @staticmethod
    def to_detail(
        event: Event,
    ) -> ConcertReadDetail | TheatreReadDetail | ConferenceReadDetail:
        cls = _get_detail_class(event.event_type)
        return cls.model_validate(event)