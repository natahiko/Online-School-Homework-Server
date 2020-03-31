import os
from flask import Flask, request
from utils import Database, ParserConfig
from resourses import *
import json

path = os.path.dirname(os.path.abspath(__file__))

# load config with all dispatchers
config = ParserConfig(os.path.join(path, 'config', 'conf.json'))
# create application
app = Flask(__name__)

# init configuration and db
with app.app_context():
    app.configuration = config
    app.database = Database(**config['database'])

# initialise all resourses
pupil = Pupil(app.database)
teacher = Teacher(app.database)
admin = Admin(app.database)
school = School(app.database)
city = City(app.database)

# Треба передати: id (code)
# Повертає:
# @app.route('/getteachersubjects', methods=['GET'])
# def get_teacher_subjects():
#     data = request.get_json()
#     if 'id' not in data:
#         return json.dumps({"error": "Недостатньо даних"}), 400
#     if data['id'] == "":
#         return json.dumps({"error": "Некоректні дані"}), 400
#     return school.get_info(data['id'])

# Треба передати: id (code)
# Повертає: name, city, region, street, house, phone, notes
@app.route('/getschoolinfo', methods=['GET'])
def get_school_info():
    data = request.get_json()
    if 'id' not in data:
        return json.dumps({"error": "Недостатньо даних"}), 400
    if data['id'] == "":
        return json.dumps({"error": "Некоректні дані"}), 400
    return school.get_info(data['id'])


# Треба передати: id (той, що в localstorage -> "authentication")
# Повертає: name, surname, patronymic, email, phone, education, phd, schoolid, notes, schoolname
@app.route('/getteacherinfo', methods=['GET'])
def get_teacher_info():
    data = request.get_json()
    if 'id' not in data:
        return json.dumps({"error": "Недостатньо даних"}), 400
    if data['id'] == "":
        return json.dumps({"error": "Некоректні дані"}), 400
    return teacher.get_info(data['id'])


# Треба передати: id (той, що в localstorage -> "authentication")
# Повертає: login, email, password, notes, name, surname
@app.route('/getadmininfo', methods=['GET'])
def get_admin_info():
    data = request.get_json()
    if 'id' not in data:
        return json.dumps({"error": "Недостатньо даних"}), 400
    if data['id'] == "":
        return json.dumps({"error": "Некоректні дані"}), 400
    return admin.get_info(data['id'])


# Треба передати: id (той, що в localstorage -> "authentication")
# Повертає: name, surname, patronymic, email, phone, class, birthdate, schoolid, notes, schoolname
@app.route('/getpupilinfo', methods=['GET'])
def get_pupil_info():
    data = request.get_json()
    if 'id' not in data:
        return json.dumps({"error": "Недостатньо даних"}), 400
    if data['id'] == "":
        return json.dumps({"error": "Некоректні дані"}), 400
    return pupil.get_info(data['id'])


@app.route('/getCities', methods=['GET'])
def get_cities():
    return city.get_cities()


@app.route('/addCity', methods=['POST'])
def add_city():
    return city.add_city(request.get_json())


@app.route('/addSchool', methods=['POST'])
def school_add():
    return school.add(request.get_json())


@app.route('/registerpupil', methods=['POST'])
def pupils_registrations():
    return pupil.register(request.get_json())


@app.route('/registerteacher', methods=['POST'])
def teacher_registrations():
    return teacher.register(request.get_json())


@app.route('/registeradmin', methods=['POST'])
def admin_registrations():
    print(request.get_json())
    return admin.register(request.get_json())


@app.route('/loginpupil', methods=['POST'])
def pupils_login():
    return pupil.login(request.get_json())


@app.route('/loginteacher', methods=['POST'])
def teacher_login():
    return teacher.login(request.get_json())


@app.route('/loginadmin', methods=['POST'])
def admin_login():
    return admin.login(request.get_json())


if __name__ == '__main__':
    app.run(port=2303, debug=True)
