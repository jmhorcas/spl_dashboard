import math
import sys
import pathlib
import logging
import argparse
from typing import Optional

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import UVLReader, FeatureIDEReader
from flamapy.metamodels.bdd_metamodel.transformations import FmToBDD
from flamapy.metamodels.bdd_metamodel.operations import BDDFeatureInclusionProbability, BDDProductDistribution


PRECISION = 2


def read_fm_file(filename: str) -> Optional[FeatureModel]:
    try:
        if filename.endswith(".uvl"):
            return UVLReader(filename).transform()
        elif filename.endswith(".xml") or filename.endswith(".fide"):
            return FeatureIDEReader(filename).transform()
    except Exception as e:
        print(e)
        pass
    try:
        return UVLReader(filename).transform()
    except Exception as e:
        print(e)
        pass
    try:
        return FeatureIDEReader(filename).transform()
    except Exception as e:
        print(e)
        pass
    return None


def get_nof_configuration_as_str(nof_configurations: int, precision: int = 2, max_limit: int = 1e6, aproximation: bool = False) -> str:
    return f"{'≤ ' if aproximation else ''}{int_to_scientific_notation(nof_configurations, precision) if nof_configurations > max_limit else nof_configurations}"


def int_to_scientific_notation(n: int, precision: int = 2) -> str:
    """Convert a large int into scientific notation.
    
    It is required for large numbers that Python cannot convert to float,
    solving the error `OverflowError: int too large to convert to float`.
    """
    str_n = str(n)
    decimal = str_n[1:precision+1]
    exponent = str(len(str_n) - 1)
    return str_n[0] + '.' + decimal + 'e' + exponent


def write_pd(pd: list[int], filepath: str) -> None:
    x = list(range(len(pd)))
    y = [get_nof_configuration_as_str(v) for v in pd]
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write('Features,Configurations\n')
        for x, y in zip(x, y):
            file.write(f'{x},{y}\n')


def write_fip(fip: dict[str, float], filepath: str) -> None:
    x_axis = [x / 100.0 for x in range(0, 101, 1)]
    y_axis = [round(sum(math.isclose(x, round(p, PRECISION), abs_tol=1e-4) for p in fip.values()) / len(fip), PRECISION) * 100 for x in x_axis]
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write('Probability,Features\n')
        for x, y in zip(x_axis, y_axis):
            file.write(f'{x},{y}\n')


def main(fm_filepath: str) -> None:
    path = pathlib.Path(fm_filepath)
    filename = path.stem
    dir = path.parent

    # Read the feature model
    fm = read_fm_file(fm_filepath)
    if fm is None:
        raise Exception('Feature model format not supported.')
    
    try:
        bdd_model = FmToBDD(fm).transform()
    except Exception as e:
        raise Exception('Error transforming the feature model to BDD.') from e
    
    pd = BDDProductDistribution().execute(bdd_model).get_result()
    fip = BDDFeatureInclusionProbability().execute(bdd_model).get_result()

    pd_output_filepath = str(dir / f'{filename}_pd.csv')
    fip_output_filepath = str(dir / f'{filename}_fip.csv')
    write_pd(pd, pd_output_filepath)
    write_fip(fip, fip_output_filepath)
   

if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    logging.basicConfig(level=logging.ERROR)
    
    parser = argparse.ArgumentParser(description='FM Characterization.')
    parser.add_argument(metavar='path', dest='path', type=str, help='Input feature model.')
    args = parser.parse_args()

    main(args.path)
