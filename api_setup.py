from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_inputs.db'
db = SQLAlchemy(app)


class weather_data_input(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    station_id = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    maximum_temp = db.Column(db.Float, nullable=True)
    minimum_temp = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)


class weather_stats_output(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_max_temp = db.Column(db.Float, nullable=True)
    avg_min_temp = db.Column(db.Float, nullable=True)
    total_precipitation = db.Column(db.Float, nullable=True)


@app.route('/api/weather_inputs', methods=['GET'])
def get_weather():
    station_id = request.args.get('unique_id')
    date = request.args.get('date')
    query = weather_data_input.query
    if station_id:
        query = query.filter_by(station_id=station_id)
    if date:
        query = query.filter_by(date=date)
    weather_records = query.paginate(page=request.args.get('page', 1, type=int), per_page=10)
    return jsonify([record.__dict__ for record in weather_records.items])


@app.route('/api/weather_inputs/stats', methods=['GET'])
def get_weather_stats():
    station_id = request.args.get('station_id')
    year = request.args.get('year')
    query = weather_stats_output.query
    if station_id:
        query = query.filter_by(station_id=station_id)
    if year:
        query = query.filter_by(year=year)
    stats_records = query.paginate(page=request.args.get('page', 1, type=int), per_page=10)
    return jsonify([record.__dict__ for record in stats_records.items])


# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "weather information API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
