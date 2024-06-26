import os
import sys
import flask

from web.blueprints.upload_fm import upload_fm_bp
from web.blueprints.analysis import analysis_bp

from cache import cache


# Create the App
flask_app = flask.Flask(__name__)

# Configure parameters
flask_app.secret_key = '5BLI6FmW48EuLlX0woUUgA'
flask_app.config['UPLOAD_FOLDER'] = 'tmp'

# Configure Flask app
flask_app.template_folder = 'web/templates'
flask_app.static_folder = 'web/static'
flask_app.static_url_path = '/static'

# Initialize the cache
cache.init_app(flask_app)


# Register blueprints
flask_app.register_blueprint(upload_fm_bp, url_prefix='/')
flask_app.register_blueprint(analysis_bp, url_prefix='/')


@flask_app.route('/')
def index():
    return flask.render_template('index.html')


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5555)

    flask_app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
