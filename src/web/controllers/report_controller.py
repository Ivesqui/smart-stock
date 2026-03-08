from flask import send_file

from container.dependencies import excel_service


# REPORT CONTROLLER


def convertir_inventario_a_excel():

    archivo_excel = excel_service.generar_excel_en_memoria()

    return send_file(
        archivo_excel,
        as_attachment=True,
        download_name="reporte_inventario.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def convertir_movimientos_a_excel():
    return

def convertir_logs_a_json():
    return
