from flask import jsonify


def get_error(e, isTeacher=0):
    code = str(e)[:4]
    if code == '1062':
        return jsonify({
            "error": "Вчитель з такою поштою або табельним номером вже зареєстрований" if isTeacher
            else "Учень з такою поштою або учнівським номером вже зареєстрований"
        }), 400
    elif code == '1452':
        return jsonify({
            "error": "Школи з таким кодом не існує"
        }), 400
    else:
        return jsonify({
            "error": str(e)
        }), 400


def check_id(data):
    if 'id' not in data:
        return False
    if data['id'] == "":
        return False
    return True


def check_parameter(data, param):
    if param not in data:
        return False
    if data[param] == "":
        return False
    return True


def check_all_parameters(data: object, params):
    return all([check_parameter(data, x) for x in params])


def check_for_null(data, param):
    if not param in data:
        return 'NULL'
    else:
        return "'" + data[param] + "'"
