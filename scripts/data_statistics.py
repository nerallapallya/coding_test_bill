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


def calculate_aggregate_stats():
    weather_data = session.query(
        weather_data_model.weather_data_input.unique_id,
        func.strftime('%Y', weather_data_model.weather_data_input.date).label('year'),
        func.avg(weather_data_model.weather_data_input.maximum_temp).label('avg_maximum_temp'),
        func.avg(weather_data_model.weather_data_input.minimum_temp).label('avg_minimum_temp'),
        func.sum(weather_data_model.weather_data_input.precipitation).label('total_precipitation')).group_by(
        func.strftime('%Y', weather_data_model.weather_data_input.date)).all()

    for data in weather_data:
        weather_stat = weather_data_model.weather_stats_output(
            station_id=data.station_id,
            year=int(data.year),
            avg_maximum_temp=data.avg_maximum_temp,
            avg_minimum_temp=data.avg_minimum_temp,
            total_precipitation=data.total_precipitation
        )
        session.add(weather_stat)

    session.commit()
    session.close()


if __name__ == '__main__':
    logger.info("Begin data ingestion")
    start_time = datetime.now()

    calculate_aggregate_stats()
    logger.info(f"aggregation finished")
    logger.info(f"start time: {start_time}")
    end_time = datetime.now()
    logger.info(f"end time: {end_time}")