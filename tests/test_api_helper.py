import pytest
from api_helper import Records_Manager  # Replace with the actual module name
from database_manager import DataBase_Manager

# Define a test database name
TEST_DB_NAME = "test_my_database.db"


# Create a fixture to set up and tear down the test database
@pytest.fixture
def test_db():
    # Set up: Create a test database
    DataBase_Manager.db_name = TEST_DB_NAME



# Test the Records_Manager class
class TestRecordsManager:
    def test_fetch_weather_data(self):
        # Set up: Create a test database manager and insert sample data
        DataBase_Manager.database_creation()
        record = ("Station1", "2023-01-01", 25, 10, 5)
        sample_data = {
            "Station_id": "Station1",
            "date": "2023-01-01",
            "max_temperature": 25,
            "min_temperature": 10,
            "precipitation": 5,
        }
        DataBase_Manager.data_ingestion(record)
        DataBase_Manager.get_connection().commit()

        # Initialize Records_Manager with the test database
        data = Records_Manager.fetch_weather_data(
            date="2023-01-01", station_id="Station1"
        )

        # Verify that the expected data is returned
        assert len(data) == 1
        assert data[0] == sample_data

    def test_fetch_weather_stats(self, test_db):
        # Set up: Create a test database manager and insert sample stats
        DataBase_Manager.database_creation()
        sample_stats = {
            "Station_id": "Station1",
            "avg_max_temperature": 25,
            "avg_min_temperature": 10,
            "total_precipitation": 5,
        }
        DataBase_Manager.data_analysis()
        DataBase_Manager.get_connection().commit()

        stats = Records_Manager.fetch_weather_stats(station_id="Station1")

        # Verify that the expected stats are returned
        assert len(stats) == 1
        assert stats[0] == sample_stats


# Run the tests
if __name__ == "__main__":
    pytest.main()
