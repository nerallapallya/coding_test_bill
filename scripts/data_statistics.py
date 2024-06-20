import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from api.weather_data_models.weather_data_model import weather_data_input, weather_data_stats, Base

DATABASE_URL = 'sqlite:///weather_data.db'


def calculate_yearly_stats():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Get distinct station ids
    stations = session.query(weather_data_input.station_id).distinct()

    for station in stations:
        station_id = station[0]

        # Get distinct years for each station
        years = session.query(func.strftime('%Y', weather_data_input.date)).filter(
            weather_data_input.station_id == station_id).distinct()

        for year in years:
            year = int(year[0])

            # Calculate average maximum temperature
            avg_max_temp = session.query(func.avg(weather_data_input.maximum_temp)).filter(
                weather_data_input.station_id == station_id,
                func.strftime('%Y', weather_data_input.date) == str(year),
                weather_data_input.maximum_temp != None
            ).scalar()

            # Calculate average minimum temperature
            avg_min_temp = session.query(func.avg(weather_data_input.minimum_temp)).filter(
                weather_data_input.station_id == station_id,
                func.strftime('%Y', weather_data_input.date) == str(year),
                weather_data_input.minimum_temp != None
            ).scalar()

            # Calculate total precipitation
            total_precipitation = session.query(func.sum(weather_data_input.precipitation)).filter(
                weather_data_input.station_id == station_id,
                func.strftime('%Y', weather_data_input.date) == str(year),
                weather_data_input.precipitation != None
            ).scalar()

            # Convert precipitation from millimeters to centimeters
            if total_precipitation is not None:
                total_precipitation /= 10.0

            # Store the calculated statistics in the WeatherStats table
            weather_stat = weather_data_stats(
                station_id=station_id,
                year=year,
                avg_maximum_temp=avg_max_temp,
                avg_minimum_temp=avg_min_temp,
                total_precipitation=total_precipitation
            )

            existing_stat = session.query(weather_data_stats).filter_by(station_id=station_id, year=year).first()
            if existing_stat is None:
                session.add(weather_stat)

        session.commit()

    session.close()


if __name__ == "__main__":
    calculate_yearly_stats()
    print("Yearly weather statistics calculation complete.")
