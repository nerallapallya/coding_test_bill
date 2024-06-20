from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class weather_data_input(db.Model):
    __tablename__ = 'weather_data'

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    maximum_temp = db.Column(db.Float)
    minimum_temp = db.Column(db.Float)
    precipitation = db.Column(db.Float)

    __table_args__ = (db.UniqueConstraint('station_id', 'date', name='_station_date_uc'),)


class weather_data_stats(db.Model):
    __tablename__ = 'weather_stats'

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_maximum_temp = db.Column(db.Float)
    avg_minimum_temp = db.Column(db.Float)
    total_precipitation = db.Column(db.Float)

    __table_args__ = (db.UniqueConstraint('station_id', 'year', name='_station_year_uc'),)
