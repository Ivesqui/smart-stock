from utils.responses import success_response

# ======================================================
# DASHBOARD
# ======================================================

#@app.route("/dashboard/resumen", methods=["GET"])
@token_required
#@roles_required("ADMIN")
def dashboard():

    resumen = inventario.obtener_resumen_dashboard()

    return success_response(data=resumen)