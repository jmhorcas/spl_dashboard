import flask

from . import analysis_bp

from flamapy_analysis.flamapy_spl import FlamapySPL
from flamapy_analysis.statistical_analysis import StatisticalAnalysis
from cache import cache


@analysis_bp.route('/analysis', methods=['GET'])
def analysis():
    if 'flamapy_spl_hash' in flask.session:
        flamapy_spl_hash = flask.session['flamapy_spl_hash']
    flamapy_spl: FlamapySPL = cache.get(flamapy_spl_hash)
    if flamapy_spl is None:
        print('Flamapy SPL expired.')
        return None
    stats_analysis = StatisticalAnalysis(flamapy_spl)
    results = [stats_analysis.features_number(),
               stats_analysis.constraints_number(),
               stats_analysis.configurations_number(),
               stats_analysis.total_variability(),
               stats_analysis.partial_variability(),
               stats_analysis.homogeneity(),
               stats_analysis.product_distribution(),
               stats_analysis.descriptive_statistics(),
               stats_analysis.feature_inclusion_probabilities(),
               stats_analysis.extra_constraint_representativeness()]
    data = {res['name']: res for res in results}
    return flask.render_template('analysis/statistical_analysis.html', data=data) 
