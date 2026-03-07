from flask import jsonify

# ======================================================
# RESPUESTAS ESTÁNDAR
# ======================================================

def success_response(data=None, message=None, status=200):
    response = {}
    if message:
        response["message"] = message
    if data is not None:
        response["data"] = data
    return jsonify(response), status


def error_response(message, status=400):
    return jsonify({"error": message}), status
