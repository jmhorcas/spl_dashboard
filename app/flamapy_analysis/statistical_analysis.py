import math
from typing import Any

from flamapy_analysis.flamapy_spl import FlamapySPL

import utils


DEFAULT_PRECISION: int = 2
CORE_FEATURES_COLOR = 'rgb(28, 200, 138)'  # Green
DEAD_FEATURES_COLOR = 'rgb(231, 74, 59)'  # Red
PUREOPTIONAL_FEATURES_COLOR = 'rgb(246, 194, 62)'  # Yellow
VARIANT_FEATURES_COLOR = 'rgb(126, 157, 188)'  # Blue-grey




class StatisticalAnalysis():

    def __init__(self, flamapy_spl: FlamapySPL, precision: int = DEFAULT_PRECISION) -> None:
        self.flamapy_spl = flamapy_spl
        self.precision = precision

    def construct_result(self, name: str, description: str, value: Any) -> dict[str, Any]:
        return {"name": name, "description": description, "value": value}

    def get_percentage_str(self, value: int | float) -> str:
        if value == 0:
            return str(value)
        percentage = value * 100
        format_percentage = '{:.pe}'
        format_percentage = format_percentage.replace('p', str(self.precision))
        percentage_value = round(percentage, self.precision)
        return str(percentage_value) if percentage_value > 0 else format_percentage.format(percentage)

    def features_number(self) -> dict[str, Any]:
        return self.construct_result(name='Features',
                                     description=FlamapySPL.features.__doc__,
                                     value=len(self.flamapy_spl.features))
    
    def constraints_number(self) -> dict[str, Any]:
        return self.construct_result(name='Constraints',
                                     description=FlamapySPL.constraints.__doc__,
                                     value=len(self.flamapy_spl.constraints))

    def satisfiable(self) -> dict[str, Any]:
        return self.construct_result(name='Satisfiable',
                                     description=FlamapySPL.satisfiable.__doc__,
                                     value=self.flamapy_spl.satisfiable)

    def configurations_number(self) -> dict[str, Any]:
        value = utils.get_nof_configuration_as_str(self.flamapy_spl.configurations_number, 
                                                   precision=self.precision,
                                                   max_limit=1e6)
        return self.construct_result(name='Configurations',
                                     description=FlamapySPL.configurations_number.__doc__,
                                     value=value)

    def total_variability(self) -> dict[str, Any]:
        value = self.get_percentage_str(self.flamapy_spl.total_variability)
        return self.construct_result(name='Total variability',
                                     description=FlamapySPL.total_variability.__doc__,
                                     value=value)

    def partial_variability(self) -> dict[str, Any]:
        value = self.get_percentage_str(self.flamapy_spl.partial_variability)
        return self.construct_result(name='Partial variability',
                                     description=FlamapySPL.partial_variability.__doc__,
                                     value=value)
    
    def homogeneity(self) -> dict[str, Any]:
        value = self.get_percentage_str(self.flamapy_spl.homogeneity)
        return self.construct_result(name='Homogeneity',
                                     description=FlamapySPL.homogeneity.__doc__,
                                     value=value)
    
    def feature_inclusion_probabilities(self) -> dict[str, Any]:
        fip = self.flamapy_spl.feature_inclusion_probabilities
        x_axis = [x / 100.0 for x in range(0, 101, 1)]
        y_axis = [round(sum(math.isclose(x, round(p, self.precision), abs_tol=1e-4) 
                            for p in fip.values()) / len(self.flamapy_spl.features), 
                            self.precision) * 100 for x in x_axis]
        colors = [DEAD_FEATURES_COLOR] + [VARIANT_FEATURES_COLOR] * (len(x_axis) - 2) + [CORE_FEATURES_COLOR]
        colors[50] = PUREOPTIONAL_FEATURES_COLOR
        value = {'x': x_axis, 'y': y_axis, 'colors': colors}
        return self.construct_result(name='Feature Inclusion Probabilities',
                                     description=FlamapySPL.feature_inclusion_probabilities.__doc__,
                                     value=value)

    def product_distribution(self) -> dict[str, Any]:
        dist = self.flamapy_spl.product_distribution
        y = [utils.get_nof_configuration_as_str(v) for v in dist]
        value = {'x': list(range(len(dist))), 'y': y}
        return self.construct_result(name='Product Distribution',
                                     description=FlamapySPL.product_distribution.__doc__,
                                     value=value)

    def descriptive_statistics(self) -> dict[str, Any]:
        value = {e: round(v, self.precision) for e, v in self.flamapy_spl.descriptive_statistics.items()}
        return self.construct_result(name='Descriptive statistics',
                                     description=FlamapySPL.descriptive_statistics.__doc__,
                                     value=value)
    
    def extra_constraint_representativeness(self) -> dict[str, Any]:
        value = self.get_percentage_str(self.flamapy_spl.extra_constraint_representativeness)
        return self.construct_result(name='Extra constraint representativeness',
                                     description=FlamapySPL.extra_constraint_representativeness.__doc__,
                                     value=value)
