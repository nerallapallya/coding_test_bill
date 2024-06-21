This project is for ingesting weather data, calculating data stats and exposing the data via a REST API. 
This implementation uses SQLite for the database, SQLAlchemy for ORM, and Flask for the REST API.

--language
- Python 3.9

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
--python api/weather_data_models/weather_data_model.py

6. data injestion
--python scripts/data_injestion.py

7. Data statistics
--python scripts/data_statistics.py

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


screeshots from the run 
![datbase_created](https://github.com/nerallapallya/coding_test_bill/assets/146959916/8c86fcfa-e2e1-4a8b-aa6f-132ba470f1cf)
![Screenshot 2024-06-20 at 4 47 07 PM](https://github.com/nerallapallya/coding_test_bill/assets/146959916/e6eb1949-58f0-459f-823b-c560ba2df755)
![Screenshot 2024-06-20 at 4 53 01 PM](https://github.com/nerallapallya/coding_test_bill/assets/146959916/e3ae91d4-a405-41eb-a6f5-882bc2c0694b)
![Screenshot 2024-06-20 at 8 06 46 PM](https://github.com/nerallapallya/coding_test_bill/assets/146959916/12a282f7-cd31-4ce9-b728-a564d3b6a923)

