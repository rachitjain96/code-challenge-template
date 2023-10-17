from fastapi import FastAPI, Query
import logging
from api_helper import Records_Manager

app = FastAPI()

# Initialize the logging configuration
logging.basicConfig(
    filename='logs.log',
    filemode='a',
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

@app.get("/api/weather")
def get_weather_data(
    date: str = Query(None, title="Date (YYYYMMDD format)"),
    station_id: str = Query(None, title="Station ID"),
    page: int = Query(1, description="Page number"),
    per_page: int = Query(10, description="Items per page"),
):
    """
    Get weather data based on query parameters.

    :param date: Date in YYYYMMDD format (optional).
    :param station_id: Station ID (optional).
    :param page: Page number (default is 1).
    :param per_page: Items per page (default is 10).
    :return: JSON response containing weather data.
    """
    logger.info("Fetching weather data with parameters: date=%s, station_id=%s, page=%s, per_page=%s", date, station_id, page, per_page)
    weather_data = Records_Manager.fetch_weather_data(
        date, station_id, page, per_page
    )
    return {"data": weather_data}

@app.get("/api/weather/stats")
def get_weather_stats(
    station_id: str = Query(None, title="Station ID"),
):
    """
    Get weather statistics based on query parameters.

    :param station_id: Station ID (optional).
    :return: JSON response containing weather statistics.
    """
    logger.info("Fetching weather statistics with station_id=%s", station_id)
    weather_stats = Records_Manager.fetch_weather_stats(station_id)
    return {"data": weather_stats}
