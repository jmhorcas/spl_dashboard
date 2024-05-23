from flask import Blueprint


# Create the blueprint instance
upload_fm_bp = Blueprint('upload_fm',
                         __name__,
                         template_folder='templates',
                         static_folder='static',
                         static_url_path='/upload_fm/static')


# Import the routes module
from . import routes
