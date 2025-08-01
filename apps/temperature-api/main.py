from fastapi import FastAPI, Query, Path
from random import uniform
from time import time

app = FastAPI(title="Temperature API", version="1.0.0")

SENSOR_TO_LOCATION = {"1": "Living Room", "2": "Bedroom", "3": "Kitchen"}
LOCATION_TO_SENSOR = {v: k for k, v in SENSOR_TO_LOCATION.items()}

def build(sensor_id: str, location: str) -> dict:
    return {
        "sensorId": sensor_id,
        "location": location,
        "value": round(uniform(5, 30), 2),
        "ts": int(time()),
    }

@app.get("/temperature")
def by_query(
    sensorId: str | None = Query(None, alias="sensorId"),
    location: str | None = None,
):
    if sensorId is None and location is None:
        return {"detail": "Either sensorId or location must be provided"}
    if sensorId is None:
        sensorId = LOCATION_TO_SENSOR.get(location, "0")
    if location is None:
        location = SENSOR_TO_LOCATION.get(sensorId, "Unknown")
    return build(sensorId, location)

@app.get("/temperature/{identifier}")
def by_path(identifier: str = Path(..., description="sensorId *или* location")):
    if identifier.isdigit():
        sensor_id = identifier
        location = SENSOR_TO_LOCATION.get(sensor_id, "Unknown")
    else:
        location = identifier.replace("%20", " ")
        sensor_id = LOCATION_TO_SENSOR.get(location, "0")
    return build(sensor_id, location)
