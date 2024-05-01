#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Places"""
from flask import abort, jsonify, make_response, request
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(HTTP_NOT_FOUND)
    places = [place.tp_dict() for place in city.places]
    return (jsonify(places))


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(HTTP_NOT_FOUND)
    return (jsonify(place.to_dict()))


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(HTTP_NOT_FOUND)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), HTTP_OK)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(HTTP_NOT_FOUND)
    data = request.get_json()
    if not data:
        abort(HTTP_BAD_REQUEST, 'Not a JSON')
    if 'user_id' not in data:
        abort(HTTP_BAD_REQUEST, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(HTTP_NOT_FOUND)
    if 'name' not in data:
        abort(HTTP_BAD_REQUEST, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), HTTP_CREATED)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(HTTP_NOT_FOUND)
    data = request.get_json()
    if not data:
        abort(HTTP_BAD_REQUEST, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), HTTP_OK)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """Searches for Place objects"""
    data = request.get_json()
    if not data:
        abort(HTTP_BAD_REQUEST, 'Not a JSON')
    places = storage.all(Place).values()
    if 'states' in data:
        places = [place for place in places
                  if place.city.state_id in data['states']]
    if 'cities' in data:
        places = [place for place in places
                  if place.city_id in data['cities']]
    if 'amenities' in data:
        places = [place for place in places
                  if all(amenity.id in place.amenities
                         for amenity in data['amenities'])]
    places = [place.to_dict() for place in places]
    return jsonify(places)
