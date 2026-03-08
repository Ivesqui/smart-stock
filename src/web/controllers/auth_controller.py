from flask import request, g
from container.dependencies import auth_service, user_service
from utils.responses import success_response, error_response


def register():
    try:
        data = request.get_json()
        if not data:
            return error_response("Datos requeridos", 400)

        usuario = auth_service.registrar(
            nombre=data["nombre"],
            email=data["email"],
            password=data["password"],
            rol=data.get("rol", "OPERADOR")
        )

        return success_response(
            data=usuario.to_dict(),
            message="User registrado",
            status=201
        )

    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        print("ERROR REGISTER:", e)
        # raise test de errores
        return error_response("Error interno del servidor", 500)



def login():
    try:
        data = request.get_json()
        if not data:
            return error_response("Datos requeridos", 400)

        token = auth_service.login(
            email=data["email"],
            password=data["password"]
        )

        return success_response(data={"token": token})

    except ValueError as e:
        return error_response(str(e), 401)

    except Exception as e:
        print("ERROR LOGIN:", e)
        raise


# Información de usuario

def me():

    current_user = g.user
    usuario = user_service.obtener_por_id(current_user["user_id"])

    return success_response(data=usuario.to_dict())
