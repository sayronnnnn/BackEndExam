from pydantic import BaseModel
from typing import List, Optional

class Medalist(BaseModel):
    name: str
    medal_type: str
    gender: str
    country: str
    country_code: str
    nationality: str
    medal_code: str
    medal_date: str

class EventStatsData(BaseModel):
    discipline: str
    event: str
    event_date: str
    medalists: List[Medalist]

class Paginate(BaseModel):
    current_page: int
    total_pages: int
    next_page: Optional[str]
    previous_page: Optional[str]

class EventStatsResponse(BaseModel):
    data: List[EventStatsData]
    paginate: Paginate
