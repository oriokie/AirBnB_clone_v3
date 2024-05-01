#!/usr/bin/python3
"""This is the index file for the API Blueprint"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    classes = {"Amenity": "amenities", "City": "cities", "Place": "places",
               "Review": "reviews", "State": "states", "User": "users"}
    num_objs = {}
    for key, value in classes.items():
        try:
            num_objs[value] = storage.count(key)
        except:
            num_objs[value] = 0
    return jsonify(num_objs)
