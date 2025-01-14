from flask import jsonify
from functools import wraps
from http import HTTPStatus as Status
from ..models import Video, VideoType, Attention, Emotion, Person
from .. import db


def require_video_exists(route_function):
    """
    Decorator to check if video exists in database, if not return 404

    Note:
        It requires that the `route_function` has a parameter called `video_id`
    """

    @wraps(route_function)
    def decorator(*args, **kwargs):
        # Creates dict with args along with their variable names, then merge with kwargs
        kwargs.update(zip(route_function.__code__.co_varnames, args))

        video_id = kwargs['video_id']
        video = db.session.query(Video).filter_by(id=video_id).first()

        if video is None:
            return jsonify({"status": "error", "message": "Video not found"}), Status.NOT_FOUND

        return route_function(**kwargs)

    return decorator


def require_reaction_video_exists(require_trailer=False):
    """
    Decorator to check if video exists in database, and its type is reaction, if not return 404
    And optionally check if this reaction video has a trailer

    Note:
        It requires that the `route_function` has a parameter called `video_id`
    """

    def decorator(route_function):
        @wraps(route_function)
        def wrapper(*args, **kwargs):
            # Creates dict with args along with their variable names, then merge with kwargs
            kwargs.update(zip(route_function.__code__.co_varnames, args))

            video_id = kwargs['video_id']
            video = db.session.query(Video).filter_by(id=video_id, type=VideoType.Reaction).first()

            if video is None:
                return jsonify({"status": "error", "message": "Reaction Video not found"}), Status.NOT_FOUND

            if video.trailer is None and require_trailer:
                return jsonify({"status": "error", "message": "Reaction Video has no trailer"}), Status.NOT_FOUND

            return route_function(**kwargs)

        return wrapper
    return decorator


def require_video_processed(route_function):
    """
    Decorator to check if video exists in database, and if it has finished processing
    If didn't exist return 404
    If didn't finish processing return 400

    Note:
        It requires that the `route_function` has a parameter called `video_id`
    """

    @wraps(route_function)
    def decorator(*args, **kwargs):
        # Creates dict with args along with their variable names, then merge with kwargs
        kwargs.update(zip(route_function.__code__.co_varnames, args))

        video_id = kwargs['video_id']
        video = db.session.query(Video).filter_by(id=video_id, type=VideoType.Reaction).first()

        if video is None:
            return jsonify({"status": "error", "message": "Video not found"}), Status.NOT_FOUND

        if not video.finished_processing:
            return jsonify({"status": "error", "message": "Video not finished processing"}), Status.BAD_REQUEST

        return route_function(**kwargs)

    return decorator


def require_person_exists(route_function):
    """
    Decorator to check if person exists in database, if not return 404

    Note:
        It requires that the `route_function` has a parameter called `person_id`
    """

    @wraps(route_function)
    def decorator(*args, **kwargs):
        # Creates dict with args along with their variable names, then merge with kwargs
        kwargs.update(zip(route_function.__code__.co_varnames, args))

        video_id = kwargs['video_id']
        person_id = kwargs['person_id']

        person = db.session.query(Person).filter_by(id=person_id, video_id=video_id).first()
        if person is None:
            return jsonify({"status": "person not found"}), Status.NOT_FOUND

        return route_function(**kwargs)

    return decorator
