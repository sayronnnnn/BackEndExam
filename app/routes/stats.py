from fastapi import APIRouter, Query, HTTPException
from app.database import db
from app.models import EventStatsResponse, EventStatsData, Paginate
from typing import List
from math import ceil
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/aggregated_stats/event", response_model=EventStatsResponse)
async def get_event_stats(page: int = Query(1, alias="page", ge=1)):
    PAGE_SIZE = 10
    skip = (page - 1) * PAGE_SIZE

    collection = db["medalists"]

    pipeline = [
        {
            "$group": {
                "_id": {
                    "discipline": "$discipline",
                    "event": "$event",
                    "event_date": "$event_date"
                },
                "medalists": {
                    "$push": {
                        "name": "$name",
                        "medal_type": "$medal_type",
                        "gender": "$gender",
                        "country": "$country",
                        "country_code": "$country_code",
                        "nationality": "$nationality",
                        "medal_code": "$medal_code",
                        "medal_date": "$event_date"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "discipline": "$_id.discipline",
                "event": "$_id.event",
                "event_date": "$_id.event_date",
                "medalists": 1
            }
        },
        {"$skip": skip},
        {"$limit": PAGE_SIZE}
    ]

    try:
        total_records = await collection.count_documents({})
        total_pages = ceil(total_records / PAGE_SIZE)

        result = await collection.aggregate(pipeline).to_list(length=PAGE_SIZE)

        if not result:
            raise HTTPException(status_code=404, detail="No data found.")

        return EventStatsResponse(
            data=[EventStatsData(**d) for d in result],
            paginate=Paginate(
                current_page=page,
                total_pages=total_pages,
                next_page=f"/aggregated_stats/event?page={page+1}" if page < total_pages else None,
                previous_page=f"/aggregated_stats/event?page={page-1}" if page > 1 else None
            )
        )

    except Exception as e:
        logger.error(f"Error fetching event stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
