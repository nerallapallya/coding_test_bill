import os
import glob
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.weather_data_models.weather_data_model import weather_data_input, Base

DATABASE_URL = 'sqlite:///weather_data.db'


def parse_weather_data_file(file_path, station_id):
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 4:
                continue

            date_str, max_temp, min_temp, precipitation = parts
            date = datetime.datetime.strptime(date_str, "%Y%m%d").date()

            max_temp = float(max_temp) / 10.0 if max_temp != "-9999" else None
            min_temp = float(min_temp) / 10.0 if min_temp != "-9999" else None
            precipitation = float(precipitation) / 10.0 if precipitation != "-9999" else None

            yield weather_data_input(
                station_id=station_id,
                date=date,
                maximum_temp=max_temp,
                minimum_temp=min_temp,
                precipitation=precipitation
            )


def ingest_weather_data(data_dir):
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    for file_path in glob.glob(os.path.join(data_dir, "*.txt")):
        station_id = os.path.basename(file_path).replace('.txt', '')
        weather_data = list(parse_weather_data_file(file_path, station_id))

        for data in weather_data:
            existing_record = session.query(weather_data_input).filter_by(station_id=data.station_id, date=data.date).first()
            if existing_record is None:
                session.add(data)

        session.commit()

    session.close()


if __name__ == "__main__":
    data_directory = '../input_data/wx_data' 
    ingest_weather_data(data_directory)
    print("Data ingestion complete.")
