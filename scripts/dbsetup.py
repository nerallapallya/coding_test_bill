from api.weather_data_models.weather_data_model import db
from app import app

with app.app_context():
    db.create_all()
    print("Database tables created.")