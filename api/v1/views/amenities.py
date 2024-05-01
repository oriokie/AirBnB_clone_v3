#!/usr/bin/python3
"""This is the amenities file for the API Blueprint"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    all_amenities = []
    for amenity in amenities:
        all_amenities.append(amenity.to_dict())
    return (jsonify(all_amenities))


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_amenity(amenity_id):
    """A function that retrieves a specific Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return (jsonify(amenity.to_dict()))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_amenity(amenity_id):
    """A function that deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({}), 200)
