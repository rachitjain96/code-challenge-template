import pytest
import os
from database_manager import DataBase_Manager  # Import your class here

# Define a test database name
TEST_DB_NAME = ":memory:"


# Create a fixture to set up and tear down the test database
@pytest.fixture
def test_db():
    # Set up: Create a test database
    DataBase_Manager.db_name = TEST_DB_NAME

# Define test cases
class TestDataBaseManager:
    def test_connection(self):
        # Test if the connection method returns a valid connection
        
        assert DataBase_Manager.get_connection() is not None

    def test_database_creation(self):
        # Test if the database_creation method creates tables without errors
        DataBase_Manager.database_creation()
        # Check if the tables exist in the test database
        cursor = DataBase_Manager.get_cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        assert ("weather_data_records",) in tables
        assert ("weather_data_stats",) in tables

    def test_data_ingestion(self):
        # Test if data_ingestion method inserts data into the table
        record = ("Station1", "2023-01-01", 25, 10, 5)
        DataBase_Manager.data_ingestion(record)
        # Query the database to check if the data was inserted
        cursor = DataBase_Manager.get_cursor()
        cursor.execute(
            "SELECT * FROM weather_data_records WHERE Station_id = 'Station1';"
        )
        data = cursor.fetchone()
        assert data == record

    def test_data_analysis(self):
        # Test if data_analysis method populates the statistics table
        record = ("Station1", "2023-01-01", 25, 10, 5)
        DataBase_Manager.data_ingestion(record)
        DataBase_Manager.data_analysis()
        # Query the database to check if data analysis was performed
        cursor = DataBase_Manager.get_cursor()
        cursor.execute(
            "SELECT * FROM weather_data_stats WHERE Station_id = 'Station1';"
        )
        data = cursor.fetchone()
        assert data is not None
        # Check the values in the statistics table

        # Check if the calculated values are within some reasonable range
        assert 20 <= data[1] <= 30  # avg_max_temperature
        assert 5 <= data[2] <= 15  # avg_min_temperature
        assert 0 <= data[3] <= 10  # total_precipitation

    def test_data_redundancy(self):
        record = ("Station2", "2023-01-01", 25, 10, 5)
        DataBase_Manager.data_ingestion(record)
        DataBase_Manager.data_ingestion(record)
        cursor = DataBase_Manager.get_cursor()
        cursor.execute(
            "SELECT * FROM weather_data_stats WHERE Station_id = 'Station1';"
        )
        data = cursor.fetchall()
        assert len(data) == 1


# Run the tests
if __name__ == "__main__":
    pytest.main()
    os.remove(TEST_DB_NAME)
