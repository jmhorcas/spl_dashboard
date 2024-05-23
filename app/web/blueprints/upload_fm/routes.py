import os
import flask
from werkzeug.utils import secure_filename
import tempfile

from . import upload_fm_bp

from . import utils


@upload_fm_bp.route('/', methods=['POST'])
def upload_fm():
    if 'file' not in flask.request.files:
        flask.flash('No file part')
        return flask.redirect(flask.request.url)
    file = flask.request.files['file']
    if file.filename == '':
        flask.flash('No selected file')
        return flask.redirect(flask.request.url)
    if file and utils.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(flask.current_app.config['UPLOAD_FOLDER'], filename)
        filepath = secure_filename(filepath)
        file.save(filepath)
        fm_model = utils.read_fm_file(filepath)
        os.remove(filepath)

        print(fm_model)
    return flask.render_template('index.html')
