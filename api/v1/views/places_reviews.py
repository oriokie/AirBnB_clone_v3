#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Reviews"""
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.user import User


HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrive the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(HTTP_NOT_FOUND)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object"""

    review = storage.get(Review, review_id)
    if not review:
        abort(HTTP_NOT_FOUND)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object"""

    review = storage.get(Review, review_id)
    if not review:
        abort(HTTP_NOT_FOUND)
    storage.delete(review)
    storage.save()
    return (jsonify({}), HTTP_OK)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a review"""

    place = storage.get(Place, place_id)
    if not place:
        abort(HTTP_NOT_FOUND)
    data = request.get_json()
    if not data:
        abort(HTTP_BAD_REQUEST, 'Not a JSON')
    if 'user_id' not in data:
        abort(HTTP_BAD_REQUEST, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(HTTP_NOT_FOUND)
    if 'text' not in data:
        abort(HTTP_BAD_REQUEST, 'Missing text')
    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return (jsonify(new_review.to_dict()), HTTP_CREATED)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Updates a review"""

    review = storage.get(Review, review_id)
    if not review:
        abort(HTTP_NOT_FOUND)
    data = request.get_json()
    if not data:
        abort(HTTP_BAD_REQUEST, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    storage.save()
    return (jsonify(review.to_dict()), HTTP_OK)
