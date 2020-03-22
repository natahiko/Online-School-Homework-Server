from flask import jsonify


def get_error(e, isTeacher=0):
    code = str(e)[:4]
    if code == '1062':
        return jsonify({
            "error": "Вчитель з такою поштою або табельним номером вже зареєстрований" if isTeacher
            else "Учень з такою поштою або учнівським номером вже зареєстрований"
        }), 200
    elif code == '1452':
        return jsonify({
            "error": "Школи з таким кодом не існує"
        }), 200
    else:
        return jsonify({
            "error": str(e)
        }), 200
