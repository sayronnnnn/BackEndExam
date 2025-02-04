from fastapi import APIRouter, Query, HTTPException
from pymongo import MongoClient
from math import ceil

router = APIRouter()

# MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client["olympics"]
collection = db["medalists"]

@router.get("/aggregated_stats/event")
async def get_event_aggregated_stats(page: int = Query(1, ge=1)):
    try:
        # Records per page
        records_per_page = 10

        # Aggregation query
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "discipline": "$discipline",
                        "event": "$event",
                        "event_date": "$event_date",  # Corrected field name
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
                            "medal_date": "$event_date",  # Corrected field name
                        }
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "discipline": "$_id.discipline",
                    "event": "$_id.event",
                    "event_date": "$_id.event_date",
                    "medalists": 1,
                }
            }
        ]

        # Total records for pagination
        total_records = collection.count_documents({})  # Synchronous call
        total_pages = ceil(total_records / records_per_page)

        # Pagination
        if page > total_pages:
            raise HTTPException(status_code=404, detail="Page not found")
        
        pipeline.extend([ 
            {"$skip": (page - 1) * records_per_page},
            {"$limit": records_per_page},
        ])

        results = list(collection.aggregate(pipeline))  # Synchronous call

        return {
            "data": results,
            "paginate": {
                "current_page": page,
                "total_pages": total_pages,
                "next_page": f"/aggregated_stats/event?page={page+1}" if page < total_pages else None,
                "previous_page": f"/aggregated_stats/event?page={page-1}" if page > 1 else None,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")