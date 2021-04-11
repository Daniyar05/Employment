from flask import jsonify, Blueprint, make_response
from . import db_session
from .employment import Employment

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Employment).all()
    return jsonify(
        {
            'employment':
                [item.to_dict(only=('job', 'work_size', 'experience', 'email', 'user', 'start_time', 'end_time', 'id'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Employment).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('job', 'work_size', 'experience', 'email', 'user', 'start_time', 'end_time'))
        }
    )
