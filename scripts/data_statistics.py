import datetime
from sqlalchemy.sql import func
import logging
from api.weather_data_models.weather_data_model import db, weather_data_input, weather_data_stats
from api.api_setup import app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_aggregate_stats():
    with app.app_context():
        stats_data = db.session.query(
            weather_data_input.station_id,
            func.strftime('%Y', weather_data_input.date).label('year'),
            func.avg(weather_data_input.maximum_temp).label('avg_maximum_temp'),
            func.avg(weather_data_input.minimum_temp).label('avg_minimum_temp'),
            func.sum(weather_data_input.precipitation).label('total_precipitation')
        ).group_by(
            weather_data_input.station_id,
            func.strftime('%Y', weather_data_input.date)
        ).all()

    for data in stats_data:
        year = int(data.year)
        avg_maximum_temp = round(data.avg_maximum_temp, 2) if data.avg_maximum_temp is not None else None
        avg_minimum_temp = round(data.avg_minimum_temp, 2) if data.avg_minimum_temp is not None else None
        total_precipitation = round(data.total_precipitation / 10, 2) if data.total_precipitation is not None else None

        existing_stat = weather_data_stats.query.filter_by(station_id=data.station_id, year=year).first()

        if not existing_stat:
            weather_stat = weather_data_stats(
                station_id=data.station_id,
                year=year,
                avg_max_temp=avg_maximum_temp,
                avg_min_temp=avg_minimum_temp,
                total_precipitation=total_precipitation
            )
            db.session.add(weather_stat)
        else:
            existing_stat.avg_max_temp = avg_maximum_temp
            existing_stat.avg_min_temp = avg_minimum_temp
            existing_stat.total_precipitation = total_precipitation

    db.session.commit()
    print("Weather statistics calculated and stored.")


if __name__ == "__main__":
    calculate_aggregate_stats()
