#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Places - Amenity"""
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ as env


HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(HTTP_NOT_FOUND)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Amenity object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(HTTP_NOT_FOUND)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(HTTP_NOT_FOUND)
    if amenity not in place.amenities:
        abort(HTTP_NOT_FOUND)
    place.amenities.remove(amenity)
    storage.save()
    return make_response(jsonify({}), HTTP_OK)
