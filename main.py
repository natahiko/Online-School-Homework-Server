import json
import os

from flask import Flask, request
from flask_cors import CORS

from resourses import *
from utils import Database, ParserConfig, get_hash, check_id

path = os.path.dirname(os.path.abspath(__file__))

# load config with all dispatchers
config = ParserConfig(os.path.join(path, 'config', 'conf.json'))
# create application
app = Flask(__name__)
CORS(app)

# init configuration and db
with app.app_context():
    app.configuration = config
    app.database = Database(**config['database'])

# initialise all resourses
pupil = Pupil(app.database)
teacher = Teacher(app.database)
admin = Admin(app.database)
school = School(app.database)
city_compete = CityCompete(app.database)
subject = Subject(app.database)
olimpiad = Olimpiad(app.database)


@app.route('/deleteolimpiatask', methods=['POST'])
def delete_olimp_task():
    data = request.get_json()
    if check_id(data):
        return olimpiad.delete_task(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400

@app.route("/getallcompetitions", methods=['GET'])
def get_all_competition():
    return city_compete.get_all_competition()


@app.route("/addcompetition", methods=['POST'])
def add_competition():
    data = request.get_json()
    return city_compete.add_competition(data)


@app.route("/getCompetitionNamesAndStages", methods=['GET'])
def get_competition_names_and_stages():
    return city_compete.get_competition_names_and_stages()


@app.route('/getpupilanswer', methods=['POST'])
def get_pupil_answer():
    data = request.get_json()
    return pupil.get_answer(data)


@app.route('/getolympiadtasksandsources', methods=['POST'])
def get_tasks_and_sources_teacher():
    data = request.get_json()
    if check_id(data):
        return olimpiad.get_tasks_and_sources(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/getpupilolympiads', methods=["POST"])
def get_pupil_olimpiads():
    data = request.get_json()
    if check_id(data):
        return olimpiad.get_pupil_olimpiad(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/getpass', methods=['GET'])
def get_pass():
    return get_hash(request.get_json()['pass']), 200


@app.route('/deletehometask', methods=['POST'])
def delete_hometask():
    data = request.get_json()
    if check_id(data):
        return subject.delete_hometask(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/getCompetitionNames', methods=['GET'])
def get_competition_names():
    return city_compete.get_competition_names()


@app.route('/editolympiad', methods=['POST'])
def edit_olimpiad():
    data = request.get_json()
    return olimpiad.edit_olimp(data)


@app.route('/addolympiad', methods=['POST'])
def add_olimpiad():
    data = request.get_json()
    return olimpiad.add_olimp(data)


@app.route('/deleteolympiad', methods=['POST'])
def delete_olimpiad():
    data = request.get_json()
    if check_id(data):
        return olimpiad.delete_olimp(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/addhometask', methods=['POST'])
def add_hometask():
    data = request.get_json()
    return subject.add_hometask(data)


@app.route('/edithometask', methods=['POST'])
def edit_hometask():
    data = request.get_json()
    return subject.edit_hometask(data)


@app.route('/gethometaskinfo', methods=['POST'])
def get_hometask_info():
    data = request.get_json()
    if check_id(data):
        return subject.get_hometask_info(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route("/getteacherolympiads", methods=['POST'])
def get_teacher_olympiads():
    data = request.get_json()
    if check_id(data):
        return olimpiad.get_teacher_olympiads(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/getsubjecthometasks', methods=['POST'])
def get_subjects_hometasks():
    data = request.get_json()
    if check_id(data):
        return subject.get_subjects_hometasks(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/getpupilsubjects', methods=['POST'])
def get_pupil_subjects():
    data = request.get_json()
    if check_id(data):
        return subject.get_pupil_subjects(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/getteachersubjects', methods=['POST'])
def get_teacher_subjects():
    data = request.get_json()
    if check_id(data):
        return subject.get_teacher_subjects(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/editsubject', methods=['POST'])
def edit_subject():
    data = request.get_json()
    return subject.edit(data)


@app.route('/addsubject', methods=['POST'])
def add_subject():
    data = request.get_json()
    return subject.add(data)


@app.route('/deletesubject', methods=['POST'])
def delete_subject():
    data = request.get_json()
    if check_id(data):
        return subject.delete_sub(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


@app.route('/getschoolinfo', methods=['POST'])
def get_school_info():
    data = request.get_json()
    if check_id(data):
        return school.get_info(data['id'])
    return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400


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
    return city_compete.get_cities()


@app.route('/addCity', methods=['POST'])
def add_city():
    return city_compete.add_city(request.get_json())


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
