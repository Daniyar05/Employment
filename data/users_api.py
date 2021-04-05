from flask import jsonify, Blueprint, make_response, render_template, abort
from . import db_session
from .users import User
import requests
blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/users_show/<int:user_id>', methods=['GET', 'POST'])
def users_show(user_id):
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(User).filter(User.id == user_id).first()
        city = user.city_from
        name = user.name
    except:
        abort(404)
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={city}&format=json"
    response = requests.get(geocoder_request)
    if response:
        map_file = 'templates/map.png'
        json_response = response.json()
        params = {}
        api_server = "http://static-maps.yandex.ru/1.x/"
        pos = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
        params['ll'] = ','.join(pos)
        params['pt'] = ','.join(pos) + ',org'
        response = requests.get(api_server, params=params)
        with open(map_file, "wb") as file:
            file.write(response.content)
        return render_template("city.html", name=name, city=city)

