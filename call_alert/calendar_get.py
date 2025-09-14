from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build as build_calendar_service
from pydantic import AliasPath, BaseModel, Field, TypeAdapter, computed_field

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


__all__ = 'get_calendar_events', 'TimeRangeCalEvent'


def get_calendar_events(allow_auth_flow: bool) -> list[TimeRangeCalEvent]:
    """Fetch calendar events which are not all-day and have a video link."""
    service = authenticate_google_calendar(allow_auth_flow)
    min_datetime = datetime.now(tz=timezone.utc) - timedelta(minutes=5)
    raw_events = get_upcoming_appointments(service, min_datetime)
    events = events_schema.validate_python(raw_events)
    return [
        event
        for event in events
        if isinstance(event, TimeRangeCalEvent) and event.video_link and event.start > min_datetime
    ]


class CalEvent(BaseModel):
    # unused and I'm not sure what other values `status` can take, hence disabled
    # status: Literal['confirmed']
    summary: str
    creator: str = Field(validation_alias=AliasPath('creator', 'email'))
    organizer: str = Field(validation_alias=AliasPath('organizer', 'email'))
    html_link: str = Field(validation_alias='htmlLink')
    hangout_link: str | None = Field(None, validation_alias='hangoutLink')
    # location can be a link, e.g. zoom link
    location: str | None = None
    description: str | None = None
    attendees: list[dict[str, Any]] | None = None

    @computed_field
    @property
    def video_link(self) -> str | None:
        if self.hangout_link:
            return self.hangout_link
        elif self.location and self.location.startswith('http'):
            return self.location
        return None


class AllDayCalEvent(CalEvent):
    start_date: date = Field(validation_alias=AliasPath('start', 'date'))
    end_date: date = Field(validation_alias=AliasPath('end', 'date'))


class TimeRangeCalEvent(CalEvent):
    start: datetime = Field(validation_alias=AliasPath('start', 'dateTime'))
    start_timezone: str = Field(validation_alias=AliasPath('start', 'timeZone'))
    end: datetime = Field(validation_alias=AliasPath('end', 'dateTime'))
    end_timezone: str = Field(validation_alias=AliasPath('end', 'timeZone'))


events_schema = TypeAdapter(list[AllDayCalEvent | TimeRangeCalEvent])
Service = Any


def authenticate_google_calendar(allow_auth_flow: bool) -> Service:
    """Authenticate and return Google Calendar service object."""
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    token_file = Path('calendar-temporary-auth-token.json')
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        elif allow_auth_flow:
            flow = InstalledAppFlow.from_client_secrets_file('calendar-auth-credentials.json', SCOPES)
            creds = flow.run_local_server(
                port=9000,
                authorization_prompt_message='Please visit this URL to authorize Google Calendar:\n\n{url}',
            )
        else:
            raise RuntimeError('No valid credentials found, and auth flow disabled')

        token_file.write_text(creds.to_json())

    return build_calendar_service('calendar', 'v3', credentials=creds)


def get_upcoming_appointments(
    service: Service, min_datetime: datetime, *, max_results: int = 100, calendar_id: str = 'primary'
) -> list[dict[str, Any]]:
    """Fetch upcoming appointments from Google Calendar."""

    # Call the Calendar API
    return (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=rfc3339(min_datetime),
            timeMax=rfc3339(min_datetime + timedelta(days=2)),
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime',
        )
        .execute()
        .get('items', [])
    )


def rfc3339(dt: datetime) -> str:
    assert dt.tzinfo is not None, 'Datetime object must have a timezone'
    return dt.isoformat().replace('+00:00', 'Z')
