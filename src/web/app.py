from flask import Flask
from flask_cors import CORS

from web.routes.auth_route import auth_bp
from web.routes.user_route import user_bp
from web.routes.product_route import product_bp
from web.routes.movement_route import movement_bp
from web.routes.report_route import report_bp
from web.routes.alert_route import alert_bp
from web.routes.dashboard_route import dashboard_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(movement_bp)
app.register_blueprint(report_bp)
app.register_blueprint(alert_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)