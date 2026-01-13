from flask import Blueprint, jsonify, request
import requests
import os

bp = Blueprint("map", __name__)


@bp.get("/geocode_address")
def geocode_address():
    address = request.json.get("state")

    resp = requests.get(
        'https://api.openrouteservice.org/geocode/search',
        headers={
            'Authorization': os.environ["MAP_API_KEY"]
        },
        params={
            'text': address,
            'size': 1  # Get the top result
        }
    )
    resp = resp.json()

    if resp['features']:
        print(resp)
        lon, lat = resp['features'][0]['geometry']['coordinates']

        return jsonify({
            'status': 200,
            'lon': lon,
            'lat': lat
        })
    else:
        raise ValueError(f"Could not geocode address: {address}")


@bp.get("/calculate_distance")
def calculate_distance(_from, _to):
    resp = requests.get(
        'https://api.openrouteservice.org/v2/directions/driving-car',
        headers={
            # 'Accept': 'application/json,
            'Authorization': os.environ["MAP_API_KEY"]
        },
        params={
            'start': [8.681495, 49.41461],
            'end': [8.687872, 49.420318]
        }
    )
    resp = resp.json()

    if resp['features']:
        print(resp)

        distance_km = resp['routes'][0]['summary']['distance'] / 1000.0
        distance_km = round(distance_km, 2)

        return jsonify({
            'origin': _from,
            'destination': _to,
            'distance_km': distance_km
        })

    else:
        raise ValueError(f"Could not geocode address: {_from}")
