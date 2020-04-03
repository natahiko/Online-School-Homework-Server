import os
from flask import Flask, request
from utils import Database, ParserConfig, get_hash, check_id
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
subject = Subject(app.database)


# Треба передати: id (code)
# Повертає:
@app.route('/getpass', methods=['GET'])
def get_pass():
    return get_hash(request.get_json()['pass']), 200


@app.route('/getteachersubjects', methods=['POST'])
def get_teacher_subjects():
    data = request.get_json()
    if check_id(data):
        return subject.get_teacher_subjects(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/addsubject', methods=['POST'])
def add_subject():
    data = request.get_json()
    return subject.add(data)


# Треба передати: id (code)
# Повертає: name, city, region, street, house, phone, notes
@app.route('/getschoolinfo', methods=['POST'])
def get_school_info():
    data = request.get_json()
    if check_id(data):
        return school.get_info(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


# Треба передати: id
# Повертає: name, surname, patronymic, email, phone, education, phd, schoolid, notes, schoolname
@app.route('/getteacherinfo', methods=['POST'])
def get_teacher_info():
    data = request.get_json()
    if check_id(data):
        return teacher.get_info(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/editteacherinfo', methods=['POST'])
def edit_teacher_info():
    data = request.get_json()
    return teacher.edit_info(data)


# Треба передати: id
# Повертає: login, email, notes, name, surname
@app.route('/getadmininfo', methods=['POST'])
def get_admin_info():
    data = request.get_json()
    if check_id(data):
        return admin.get_info(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/editadmininfo', methods=['POST'])
def edit_admin_info():
    data = request.get_json()
    return admin.edit_info(data)


# Треба передати: id
# Повертає: name, surname, patronymic, email, phone, class, birthdate, schoolid, notes, schoolname
@app.route('/getpupilinfo', methods=['POST'])
def get_pupil_info():
    data = request.get_json()
    if check_id(data):
        return pupil.get_info(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/editpupilinfo', methods=['POST'])
def edit_pupil_info():
    data = request.get_json()
    return pupil.edit_info(data)


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
