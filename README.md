This project is for ingesting weather data, calculating data stats and exposing the data via a REST API. 
This implementation uses SQLite for the database, SQLAlchemy for ORM, and Flask for the REST API.

--language
- Python 3.8+
- pip package manager

--Setup instruction

1. repository cloning 
--bash
--git clone https://github.com/nerallapallya/coding_test_bill
--cd code-challenge-template


2.Virtual env creation
--python -m venv venv
--source venv/bin/activate


3. Python packages
--pip install -r requirements.txt

5. setup SQLlite DB
--python weather_data_model.py

6. data injestion
--python data_injestion.py

7. Data statistics
--python data_statistics.py

9. Run Flask API
--flask run

Below is the Table Schema for SQLlite DB
--weather_data_input

- `id`: Integer, Primary Key
- `station_id`: String
- `date`: Date
- `maximum_temp`: Float
- `minimum_temp`: Float
- `precipitation`: Float

--weather_stats_output

- `id`: Integer, Primary Key
- `station_id`: String
- `year`: Integer
- `avg_maximum_temp`: Float
- `avg_minimum_temp`: Float
- `total_precipitation`: Float

Endpoints for Rest API

--/api/weather_inputs

- GET: Retrieve WX_data weather data that has been injested into DB
  - Query Parameters:
    - `station_id`: Filter by station ID
    - `start_date`: Filter by start date (YYYY-MM-DD)
    - `end_date`: Filter by end date (YYYY-MM-DD)
    - `page`: Page number for pagination
    - `per_page`: Number of records per page

--/api/weather_inputs/stats

- GET: Retrieve aggregated weather data.
  - Query Parameters:
    - `station_id`: Filter by station ID
    - `year`: Filter by year
    - `page`: Page number for pagination
    - `per_page`: Number of records per page

Swagger documentation can be accessed under `/api/static/swagger`.

--How to run test cases

1.Pytest installation and run 
--bash
--pip install pytest
--pytest


AWS deployement

For deploying the application on AWS, we can use below services
- AWS RDS For the database.
- AWS Lambda For the data injestion and calcul;ating aggregate stats. We can schedule these lambdas using AWS CloudWatch Events.
- AWS Elastic Beanstalk or AWS ECS for Rest API

