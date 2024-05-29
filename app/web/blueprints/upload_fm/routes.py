import os
import flask
from werkzeug.utils import secure_filename

from . import upload_fm_bp

from . import utils

from flamapy_analysis.flamapy_spl import FlamapySPL
from cache import cache


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
        flamapy_spl = FlamapySPL(filepath)
        os.remove(filepath)
        # Store in cache and cookies session
        flamapy_spl_hash = str(hash(flamapy_spl))
        cache.set(flamapy_spl_hash, flamapy_spl)
        flask.session['flamapy_spl_hash'] = flamapy_spl_hash
    return flask.redirect(flask.url_for('analysis_bp.analysis'))
    #     data = {}
    #     data['product_distribution'] = analysis.get_product_distribution(fm_model)
    #     data.update(analysis.get_configurations_number(fm_model))
    #     data['n_features'] = len(fm_model.get_features())
    #     data['n_constraints'] = len(fm_model.get_constraints())
    #     data['feature_inclusion_probabilities'] = analysis.get_feature_inclusion_probabilities(fm_model)
    #     data.update(analysis.get_variability(fm_model))
    #     data.update(analysis.get_homogeneity(fm_model))
    # return flask.render_template('analysis.html', data=data)
