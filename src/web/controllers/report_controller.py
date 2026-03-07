


# ======================================================
# REPOR CONTROLLER
# ======================================================

#@app.route("/reportes/inventario/excel", methods=["GET"])
@token_required # <- autenticación
#@roles_required("ADMIN", "OPERADOR")
def descargar_excel_inventario():

    archivo_excel = excel_service.generar_excel_en_memoria()

    return send_file(
        archivo_excel,
        as_attachment=True,
        download_name="reporte_inventario.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )