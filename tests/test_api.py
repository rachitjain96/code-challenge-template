from fastapi.testclient import TestClient
from api import app
from unittest.mock import patch
import pytest


client = TestClient(app) 

# Mock the Records_Manager class and its methods
@patch("api.Records_Manager")
def test_get_weather_data(mock_records_manager):

    # Mock the fetch_weather_data method of Records_Manager to return a sample response
    sample_data = [
        {"date": "20230101", "station_id": "Station1", "max_temperature": 25}
    ]
    mock_records_manager.fetch_weather_data.return_value = sample_data

    response = client.get(
        "/api/weather?date=20230101&station_id=Station1&page=1&per_page=10"
    )
    assert response.status_code == 200
    data = response.json()["data"]

    # Verify that the expected data is returned
    assert len(data) == 1
    assert data[0] == sample_data[0]


@patch("api.Records_Manager")
def test_get_weather_stats(mock_records_manager):
    # Mock the fetch_weather_stats method of Records_Manager to return a sample response
    sample_stats = [{"station_id": "Station1", "avg_max_temperature": 25}]
    mock_records_manager.fetch_weather_stats.return_value = sample_stats

    response = client.get("/api/weather/stats?station_id=Station1")
    assert response.status_code == 200
    stats = response.json()["data"]

    # Verify that the expected stats are returned
    assert len(stats) == 1
    assert stats[0] == sample_stats[0]


if __name__ == "__main__":
    pytest.main()
