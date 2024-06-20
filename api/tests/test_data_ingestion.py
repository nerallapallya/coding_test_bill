import os
import tempfile
import pytest
import datetime
from scripts.data_ingestion import ingest_weather_inputs
from api.api_setup import db
from api.weather_data_models.weather_data_model import weather_data_input

@pytest.fixture(scope='module')
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture(scope='module')
def test_db():
    db.create_all()
    yield
    db.drop_all()

def test_ingest_weather_data(temp_dir, test_db):
    sample_data = "20230101\t-50\t-100\t0\n20230102\t100\t50\t10\n"
    file_path = os.path.join(temp_dir, "test_station.txt")
    with open(file_path, 'w') as f:
        f.write(sample_data)

    ingest_weather_inputs(temp_dir)

    data = weather_data_input.query.all()
    assert len(data) == 2
    assert data[0].station_id == 'USC0030'
    assert data[0].date == datetime.strptime('19850101', '%Y%m%d').date()
    assert data[0].max_temp == 150
    assert data[0].min_temp == 50
    assert data[0].precipitation == 100

    assert data[1].station_id == 'USC0030'
    assert data[1].date == datetime.strptime('19850102', '%Y%m%d').date()
    assert data[1].max_temp == 160
    assert data[1].min_temp == 60
    assert data[1].precipitation == 200