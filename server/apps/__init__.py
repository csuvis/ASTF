from flask import Flask

import settings
from apps.api.view import api_bp

def create_app():
    app = Flask(__name__,template_folder='../web',static_folder='../web',static_url_path="")
    app.config.from_object(settings.Config)
    app.register_blueprint(api_bp)
    return app