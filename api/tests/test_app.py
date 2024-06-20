import pytest
from api.api_setup import app, db
from api.weather_data_models.weather_data_model import weather_data_input, weather_data_stats

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Add sample data
            sample_data = weather_data_input(station_id='TEST1', date='2022-01-01', maximum_temp=25.0, minimum_temp=10.0, precipitation=5.0)
            db.session.add(sample_data)
            db.session.commit()
        yield client

def test_get_weather(client):
    response = client.get('/api/weather_inputs')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['results']) == 1
    assert data['results'][0]['station_id'] == 'TEST1'

def test_get_weather_stats(client):
    # Assuming weather stats data is precomputed and stored
    sample_stats = weather_data_stats(station_id='TEST1', year=2022, avg_maximum_temp=25.0, avg_minimum_temp=10.0, total_precipitation=5.0)
    db.session.add(sample_stats)
    db.session.commit()

    response = client.get('/api/weather_inputs/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['results']) == 1
    assert data['results'][0]['station_id'] == 'TEST1'

if __name__ == '__main__':
    pytest.main()