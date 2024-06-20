import os
import glob
import datetime
import logging
from api.weather_data_models.weather_data_model import weather_data_input, db
from api.api_setup import app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_line(line):
    parts = line.strip().split("\t")
    date = datetime.datetime.strptime(parts[0], '%Y%m%d').date()
    maximum_temp = int(parts[1]) / 10.0 if int(parts[1]) != -9999 else None
    minimum_temp = int(parts[2]) / 10.0 if int(parts[2]) != -9999 else None
    precipitation = int(parts[3]) / 10.0 if int(parts[3]) != -9999 else None
    return date, maximum_temp, minimum_temp, precipitation


def ingest_weather_inputs(dir):
    with app.app_context():
        files = glob.glob(os.path.join(dir, '*.txt'))
        total_records = 0
        start_time = datetime.datetime.now()

        for file in files:
            station_id = os.path.basename(file).split('.')[0]
            with open(file, 'r') as f:
                for line in f:
                    date, maximum_temp, minimum_temp, precipitation = parse_line(line)
                    if not db.session.query(weather_data_input).filter_by(station_id=station_id, date=date).first():
                        weather_record = weather_data_input(
                            station_id=station_id,
                            date=date,
                            maximum_temp=maximum_temp,
                            minimum_temp=minimum_temp,
                            precipitation=precipitation
                        )
                        db.session.add(weather_record)
                        total_records += 1
            db.session.commit()

        end_time = datetime.datetime.now()
        logger.info(f"Ingestion started at {start_time} and ended at {end_time}")
        logger.info(f"Total records ingested: {total_records}")


if __name__ == "__main__":
    ingest_weather_inputs('../input_data/wx_data')

