from typing import NamedTuple, Any
import json
from requests import Response
import requests
from config import USE_ROUNDED_COORDS, OPENWEATHER_API_KEY


class Coordinates(NamedTuple):
    """Apply typing based on NamedTuple"""
    longitude: float
    latitude: float


def result() -> Coordinates:
    """Returning the final result"""
    coordinates = get_gps_coordinates()
    return rounded(coordinates)


def get_info_by_ip() -> dict:
    """Find out your ip"""
    response = requests.get(url='http://ip-api.com/json/', timeout=5).json()
    return response


def get_latitude_and_longitude_by_ip() -> tuple[Any, Any]:
    """Getting the coordinates"""
    data = get_info_by_ip()
    latitude = data.get('lat')
    longitude = data.get('lon')
    lat_long_tuple = latitude, longitude
    return lat_long_tuple


def request_weather() -> str:
    """We substitute the received coordinates (length and width) by ip
    and get json with all the necessary weather data through the openweathermap api"""
    lat_and_long = get_latitude_and_longitude_by_ip()
    openweather_url = f"https://api.openweathermap.org/data/2.5/weather?" \
                      f"lat={lat_and_long[0]}" \
                      f"&lon={lat_and_long[1]}" \
                      f"&appid={OPENWEATHER_API_KEY}"
    return openweather_url


def json_request_weather() -> Response:
    """Returning connection status"""
    req_result = request_weather()
    response_for_create = requests.request(
        "POST",
        req_result,
        timeout=5,
    )
    return response_for_create


def result_json_request() -> str:
    """We translate the json request into a form convenient for us"""
    result_request = json_request_weather()
    output = (
        json.dumps(
            json.loads(result_request.text),
            ensure_ascii=False,
            sort_keys=True,
            indent=0,
            separators=("", ": ")))
    return output


def get_gps_coordinates():
    """Get coordinates via OPENWEATHERMAP API"""
    result_json = result_json_request()
    longitude = latitude = None
    for line in result_json.strip().lower().split('\n'):
        if line.startswith('"lat"'):
            latitude = float(line.split()[1])
        if line.startswith('"lon"'):
            longitude = float(line.split()[1])

    return Coordinates(longitude, latitude)


def rounded(coordinates: Coordinates) -> Coordinates:
    """Round the coordinates if necessary
       you can change the parameter in the config.USE_ROUNDED_COORDS file"""
    coordinate = get_gps_coordinates()
    if not USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(*map(
        lambda c: round(c, 1),
        [coordinate.longitude, coordinate.latitude]))


if __name__ == '__main__':
    print(result())
