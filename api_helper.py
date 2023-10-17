from database_manager import DataBase_Manager

class Records_Manager:

    @staticmethod
    def fetch_weather_data(date=None, station_id=None, page=1, per_page=10):
        # SQL query for filtering and pagination
        query = "SELECT * FROM weather_data_records Where 1=1"

        if date:
            query += f" AND date = '{date}'"
        if station_id:
            query += f" AND Station_id = '{station_id}'"

        # Calculate the start and end indices for pagination
        start_index = (page - 1) * per_page

        # Execute the SQL query with pagination
        query += f" LIMIT {per_page} OFFSET {start_index}"
        cursor = DataBase_Manager.get_cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        result_data = []
        for row in data:
            row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
            result_data.append(row_dict)

        return result_data
    
    @staticmethod
    def fetch_weather_stats(station_id=None):
        # SQL query for retrieving weather statistics
        query = "SELECT * FROM weather_data_stats WHERE 1=1"

        if station_id:
            query += f" AND Station_id = '{station_id}'"

        cursor = DataBase_Manager.get_cursor()
        cursor.execute(query)
        stats = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        result_data = []
        for row in stats:
            row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
            result_data.append(row_dict)

        return result_data
