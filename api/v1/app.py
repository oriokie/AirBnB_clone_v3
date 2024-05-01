#!/usr/bin/python3
"""Flask Application with API functionality"""
from flask import Flask, jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from os import environ as env


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Closes the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = env.get('HBNB_API_HOST')
    port = env.get('HBNB_API_PORT')
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = 5000
    app.run(host=host, port=port, threaded=True)
