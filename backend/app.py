from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.auth import bp as auth_bp
from routes.vehicles import bp as vehicles_bp
from routes.bookings import bp as bookings_bp
from routes.admin import bp as admin_bp
from routes.payments import bp as payments_bp

def create_app():
    app=Flask(__name__);app.config.from_object(Config)
    CORS(app,resources={r"/api/*":{"origins":app.config["FRONTEND_ORIGIN"]}},supports_credentials=False)
    for bp in (auth_bp,vehicles_bp,bookings_bp,admin_bp,payments_bp):app.register_blueprint(bp)
    @app.get("/api/health")
    def health():return jsonify(status="ok")
    @app.errorhandler(404)
    def not_found(_):return jsonify(error="Resource not found"),404
    @app.errorhandler(500)
    def server_error(_):return jsonify(error="An unexpected server error occurred"),500
    @app.errorhandler(Exception)
    def handle_error(error):
        app.logger.exception("Unhandled request error",exc_info=error)
        return jsonify(error="An unexpected server error occurred"),500
    return app

app=create_app()
if __name__=="__main__":app.run(debug=True,port=5000)

