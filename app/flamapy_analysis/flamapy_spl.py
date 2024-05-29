from typing import Any
from functools import cached_property

from flamapy.core.discover import DiscoverMetamodels

from flamapy.metamodels.fm_metamodel.models import FeatureModel, Feature, Constraint
from flamapy.metamodels.pysat_metamodel.models import PySATModel
from flamapy.metamodels.bdd_metamodel.models import BDDModel
from flamapy.metamodels.bdd_metamodel.operations.bdd_product_distribution import descriptive_statistics


class FlamapySPL():

    def __init__(self, fm_path: str) -> None:
        self._dm: DiscoverMetamodels = DiscoverMetamodels()
        self._fm_path: str = fm_path
        self._fm_model: FeatureModel = self._dm.use_transformation_t2m(self._fm_path, 'fm')

    @cached_property
    def fm_model(self) -> FeatureModel:
        return self._fm_model
    
    @cached_property
    def sat_model(self) -> PySATModel:
        return self._dm.use_transformation_m2m(self.fm_model, "pysat")

    @cached_property
    def bdd_model(self) -> BDDModel:
        return self._dm.use_transformation_m2m(self.fm_model, "bdd")

    def __getstate__(self):
        # Exclude non-serializable attributes
        state = self.__dict__.copy()
        del state['_dm']
        return state

    def __setstate__(self, state):
        # Restore the object's state
        self.__dict__.update(state)
        # Handle the non-serializable attribute if needed
        self._dm = DiscoverMetamodels()
    
    @cached_property
    def features(self) -> list[Feature]:
        """Features of the model."""
        return self.fm_model.get_features()
    
    @cached_property
    def constraints(self) -> list[Constraint]:
        """Constraints of the model."""
        return self.fm_model.get_constraints()
    
    @cached_property
    def configurations_number(self) -> int:
        """Number of valid configurations that can be derived."""
        return self._dm.use_operation(self.bdd_model, 'BDDConfigurationsNumber').get_result()

    @cached_property
    def total_variability(self) -> float:
        """The total variability measures the flexibility of the SPL considering all features."""
        return self.configurations_number / (2 ** len(self.features) - 1)
    
    @cached_property
    def partial_variability(self) -> float:
        """The partial variability measures the flexibility of the SPL considering only variant features."""
        return self.configurations_number / (2 ** len(self.features) - 1)
    
    @cached_property
    def homogeneity(self) -> float:
        """The homogeneity measures how similar are the configurations of the SPL."""
        return self._dm.use_operation(self.bdd_model, 'BDDHomogeneity').get_result()
    
    @cached_property
    def feature_inclusion_probabilities(self) -> dict[str, float]:
        """The Feature Inclusion Probability (FIP) determines the probability for a feature of being included in a valid configuration, that is, for each feature, the proportion of valid configurations that include it."""
        return self._dm.use_operation(self.bdd_model, 'BDDFeatureInclusionProbability').get_result()
    
    @cached_property
    def core_features(self) -> list[str]:
        """The core features are those features present in all configurations."""
        return [feat for feat, prob, in self.feature_inclusion_probabilities().items() if prob >= 1.0]

    @cached_property
    def dead_features(self) -> list[str]:
        """The dead features are those features that are not present in any configuration."""
        return [feat for feat, prob, in self.feature_inclusion_probabilities().items() if prob <= 0.0]

    @cached_property
    def variant_features(self) -> list[str]:
        """The variant features are those features that appear only in some configurations, that is, the features that are neither core features nor dead features."""
        return [feat for feat, prob, in self.feature_inclusion_probabilities().items() if 0.0 < prob < 1.0]

    @cached_property
    def pure_optional_features(self) -> list[str]:
        """The pure optional features are those feature with 0.5 (50%) probability of being selected in a valid configuration, that is, their selection is unconstrained."""
        return [feat for feat, prob, in self.feature_inclusion_probabilities().items() if prob == 0.5]

    @cached_property
    def product_distribution(self) -> list[int]:
        """The Product Distribution (PD) determines the number of configurations having a given number of features, that is, how many products have no features, one features, two features,..., all features."""
        return self._dm.use_operation(self.bdd_model, 'BDDProductDistribution').get_result()

    @cached_property
    def descriptive_statistics(self) -> dict[str, Any]:
        """Descriptive statistics summarizing the product distribution of the variability model, that is, its mean, standard deviation, median, median absolute deviation, mode, min, max, and range."""
        return descriptive_statistics(self.product_distribution)
    
    @cached_property
    def features_in_constraints(self) -> set[str]:
        """Features that are present in cross-tree constraints."""
        return {feat for ctc in self.constraints for feat in ctc.get_features()}
    
    @cached_property
    def extra_constraint_representativeness(self) -> float:
        """The degree of representativeness of the cross-tree constraints in the feature tree, as the ratio of the number of features involved in constraints to the number of features in the SPL."""
        return len(self.features_in_constraints) / len(self.features)