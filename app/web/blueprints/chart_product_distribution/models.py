from typing import Any

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.bdd_metamodel.models import BDDModel
from flamapy.metamodels.bdd_metamodel.operations import BDDProductDistribution

from analysis.models import FM


def get_product_distribution(fm_model: FeatureModel) -> dict[str, Any]:
    fm = FM(fm_model)
    dist = BDDProductDistribution().execute(fm.bdd_model).get_result()
    return {'x': list(range(len(dist))), 'y': dist}
