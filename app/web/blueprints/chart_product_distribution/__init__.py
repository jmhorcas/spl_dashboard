from flask import Blueprint


# Create the blueprint instance
chart_product_distribution_bp = Blueprint('chart_product_distribution',
                                          __name__,
                                          template_folder='templates',
                                          static_folder='static',
                                          static_url_path='/product_distribution/static')


# Import the routes module
from . import routes
