from fastapi import FastAPI, Query
from random import uniform
from time import time

app = FastAPI(title="Temperature API", version="1.0.0")

SENSOR_TO_LOCATION = {
    "1": "Living Room",
    "2": "Bedroom",
    "3": "Kitchen",
}
LOCATION_TO_SENSOR = {v: k for k, v in SENSOR_TO_LOCATION.items()}


@app.get("/temperature")
def read_temperature(
    sensorId: str | None = Query(None, alias="sensorId"),
    location: str | None = None,
):
    """Return random temperature for a given sensor or location."""
    if sensorId is None and location is None:
        return {"detail": "Either sensorId or location must be provided"}

    if sensorId is None:
        sensorId = LOCATION_TO_SENSOR.get(location, "0")
    if location is None:
        location = SENSOR_TO_LOCATION.get(sensorId, "Unknown")

    value = round(uniform(5, 30), 2)  # 5 … 30 °C
    return {
        "sensorId": sensorId,
        "location": location,
        "value": value,
        "ts": int(time()),
    }
