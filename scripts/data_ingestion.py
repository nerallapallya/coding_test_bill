import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import logging
from api.weather_data_models import weather_data_model

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to the database
engine = create_engine('sqlite:///weather_inputs.db')
Session = sessionmaker(bind=engine)
session = Session()


def ingest_weather_inputs(file_path, station_id):
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            date_input, maximum_temp, minimum_temp, precip = parts
            date = datetime.strptime(date_input, '%Y%m%d').date()
            maximum_temp = None if int(maximum_temp) == -9999 else int(maximum_temp) / 10.0
            minimum_temp = None if int(minimum_temp) == -9999 else int(minimum_temp) / 10.0
            precipitation = None if int(precip) == -9999 else int(precip) / 10.0

            existing_record = session.query(weather_data_model.weather_data_input).filter_by(station_id=station_id,
                                                                                             date=date).first()

            if existing_record:
                # Update existing record
                existing_record.maximum_temp = maximum_temp
                existing_record.minimum_temp = minimum_temp
                existing_record.precipitation = precipitation
            else:
                # Insert new record
                new_record = weather_data_model.weather_data_input(
                    station_id=station_id, date=date, maximum_temp=maximum_temp, minimum_temp=minimum_temp, precipitation=precipitation)
                session.add(new_record)

    session.commit()
    session.close()

if __name__ == '__main__':
    logger.info("Begin data ingestion")
    start_time = datetime.now()

    wx_data_dir = '../code-challenge-template/wx_data'
    for file_name in os.listdir(wx_data_dir):
        station_id = file_name.split('.')[0]
        file_path = os.path.join(wx_data_dir, file_name)
        ingest_weather_inputs(file_path, station_id)

    end_time = datetime.now()
    logger.info(f"Data ingestion finished")
    logger.info(f"start time: {start_time}")
    logger.info(f"end time: {end_time}")

