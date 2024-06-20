from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from api.weather_data_models.weather_data_model import weather_data_input, weather_data_stats

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Weather API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/api/weather_inputs', methods=['GET'])
def get_weather_data():
    station_id = request.args.get('station_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = weather_data_input.query

    if station_id:
        query = query.filter_by(station_id=station_id)
    if start_date:
        query = query.filter(weather_data_input.date >= start_date)
    if end_date:
        query = query.filter(weather_data_input.date <= end_date)

    weather_data = query.paginate(page, per_page, False)

    return jsonify({
        'total': weather_data.total,
        'pages': weather_data.pages,
        'results': [
            {
                'id': data.id,
                'station_id': data.station_id,
                'date': data.date.isoformat(),
                'maximum_temp': data.maximum_temp,
                'minimum_temp': data.minimum_temp,
                'precipitation': data.precipitation
            } for data in weather_data.items
        ]
    })


@app.route('/api/weather_inputs/stats', methods=['GET'])
def get_weather_stats():
    station_id = request.args.get('station_id')
    year = request.args.get('year', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = weather_data_stats.query

    if station_id:
        query = query.filter_by(station_id=station_id)
    if year:
        query = query.filter_by(year=year)

    stats_data = query.paginate(page, per_page, False)

    return jsonify({
        'total': stats_data.total,
        'pages': stats_data.pages,
        'results': [
            {
                'id': stats.id,
                'station_id': stats.station_id,
                'year': stats.year,
                'avg_maximum_temp': stats.avg_max_temp,
                'avg_minimum_temp': stats.avg_min_temp,
                'total_precipitation': stats.total_precipitation
            } for stats in stats_data.items
        ]
    })


if __name__ == '__main__':
    app.run(debug=True)
