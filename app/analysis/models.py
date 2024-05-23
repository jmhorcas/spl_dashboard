import threading
from typing import Optional

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.bdd_metamodel.models import BDDModel
from flamapy.metamodels.bdd_metamodel.transformations import FmToBDD


class SingletonMeta(type):
    """This is a thread-safe implementation of Singleton."""

    _instances = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
    

class FM(metaclass=SingletonMeta):

    def __init__(self, fm_model: FeatureModel) -> None:
        self._fm_model: FeatureModel = fm_model
        self._bdd_model: Optional[BDDModel] = None
    
    @property
    def fm_model(self) -> FeatureModel:
        return self._fm_model
    
    @property
    def bdd_model(self) -> BDDModel:
        if self._bdd_model is None:
            self._bdd_model = FmToBDD(self._fm_model).transform()
        return self._bdd_model
