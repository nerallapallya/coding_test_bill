from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL
DATABASE_URL = 'sqlite:///weather_data.db'

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a base class for the ORM models
Base = declarative_base()


# Define the WeatherData model
class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    maximum_temp = Column(Float)
    minimum_temp = Column(Float)
    precipitation = Column(Float)


# Define the WeatherStats model
class WeatherStats(Base):
    __tablename__ = 'weather_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    avg_maximum_temp = Column(Float)
    avg_minimum_temp = Column(Float)
    total_precipitation = Column(Float)


# Create the tables in the database
Base.metadata.create_all(engine)

# Print a message indicating success
print("Database setup complete and tables created successfully.")
