import math
from typing import Any, Optional

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.bdd_metamodel.models import BDDModel
from flamapy.metamodels.bdd_metamodel.transformations import FmToBDD
from flamapy.metamodels.bdd_metamodel.operations import (
    BDDConfigurationsNumber,
    BDDProductDistribution,
    BDDFeatureInclusionProbability,
    BDDHomogeneity,
    BDDVariability
)


class FM():
    _fm: 'FM' = None

    def __init__(self, fm_model: FeatureModel) -> None:
        self._fm_model: FeatureModel = fm_model
        self._bdd_model: Optional[BDDModel] = None
    
    @staticmethod
    def get_instance(fm_model: FeatureModel) -> 'FM':
        if FM._fm is None:
            FM._fm = FM(fm_model)
        elif FM._fm._fm_model != fm_model:
            FM._fm = FM(fm_model)
        return FM._fm
        

    @property
    def fm_model(self) -> FeatureModel:
        return self._fm_model
    
    @property
    def bdd_model(self) -> BDDModel:
        if self._bdd_model is None:
            self._bdd_model = FmToBDD(self._fm_model).transform()
        return self._bdd_model


def get_product_distribution(fm_model: FeatureModel) -> dict[str, Any]:
    fm = FM.get_instance(fm_model)
    dist_op = BDDProductDistribution()
    dist = dist_op.execute(fm.bdd_model).get_result()
    dist_stats = {e: round(v, 2) for e, v in dist_op.descriptive_statistics().items()}
    return {'x': list(range(len(dist))), 'y': dist, 'descriptive_statistics': dist_stats}


def get_feature_inclusion_probabilities(fm_model: FeatureModel) -> dict[str, Any]:
    fm = FM.get_instance(fm_model)
    n_features = len(fm_model.get_features())
    prob = BDDFeatureInclusionProbability().execute(fm.bdd_model).get_result()
    x_axis = [x  / 100.0 for x in range(0, 101, 1)]
    y_axis = [round(sum(math.isclose(x, round(p, 2), abs_tol=1e-4) for p in prob.values())/n_features, 2)*100 for x in x_axis]
    colors = ['rgb(231, 74, 59)'] + ['rgb(126, 157, 188)'] * (len(x_axis) - 2) + ['rgb(28, 200, 138)']
    colors[50] = 'rgb(246, 194, 62)'
    return {'x': x_axis, 'y': y_axis, 'colors': colors}


def get_configurations_number(fm_model: FeatureModel) -> dict[str, Any]:
    fm = FM.get_instance(fm_model)
    n_configs = BDDConfigurationsNumber().execute(fm.bdd_model).get_result()
    return {'n_configurations': n_configs}


def get_variability(fm_model: FeatureModel) -> dict[str, Any]:
    fm = FM.get_instance(fm_model)
    total_variability, partial_variability = BDDVariability().execute(fm.bdd_model).get_result()
    total_variability_res = round(total_variability * 100, 2)
    total_variability_str = str(total_variability_res) if total_variability_res > 0 else '{:.2e}'.format(total_variability * 100)
    partial_variability_res = round(partial_variability * 100, 2)
    partial_variability_str = str(partial_variability_res) if partial_variability_res > 0 else '{:.2e}'.format(partial_variability * 100)
    return {'total_variability': total_variability_str, 
            'partial_variability': partial_variability_str}


def get_homogeneity(fm_model: FeatureModel) -> dict[str, Any]:
    fm = FM.get_instance(fm_model)
    homogeneity = BDDHomogeneity().execute(fm.bdd_model).get_result()
    return {'homogeneity': round(homogeneity * 100, 2)}
