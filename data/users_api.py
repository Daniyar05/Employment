from flask import jsonify, Blueprint, make_response, render_template, abort
from . import db_session
from .users import User
import requests

blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def users_api():
    db_sess = db_session.create_session()
    jobs = db_sess.query(User).all()
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': jobs.to_dict(only=('id', 'name', 'email', 'modified_date', 'about'))
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def user_api(user_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(User).get(user_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': jobs.to_dict(only=('name', 'email', 'modified_date', 'about'))
        }
    )

