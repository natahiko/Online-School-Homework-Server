from flask import jsonify


def get_error(e):
    code = str(e)[:4]
    if code == '1062':
        return jsonify({
            "error": "Користувач з такою поштою вже є в базі даних"
        }), 200
    elif code == '1452':
        return jsonify({
            "error": "Школи з таким кодом не існує"
        }), 200
    else:
        return jsonify({
            "error": str(e)
        }), 200
