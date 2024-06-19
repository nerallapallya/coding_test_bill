from sqlalchemy import Column, Integer, String, Float, Date, create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class weather_data_input(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    station_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    maximum_temp = Column(Float, nullable=True)
    minimum_temp = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)

    __table_args__ = (UniqueConstraint('station_id', 'date', name='_station_date_uc'),)


class weather_stats_output(Base):
    __tablename__ = 'weather_stats'
    id = Column(Integer, primary_key=True)
    station_id = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    avg_maximum_temp = Column(Float, nullable=True)
    avg_minimum_temp = Column(Float, nullable=True)
    total_precipitation = Column(Float, nullable=True)

# Create SQLite database
engine = create_engine('sqlite:///weather_inputs.db')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)