from flask import Blueprint


# Create the blueprint instance
analysis_bp = Blueprint('analysis_bp',
                        __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/analysis_bp/static')


# Import the routes module
from . import routes
