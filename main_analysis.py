import sys
import argparse

from alive_progress import alive_bar, alive_it

from flamapy.metamodels.fm_metamodel.transformations import UVLReader, UVLWriter
from flamapy.metamodels.fm_metamodel.operations import FMMetrics
from flamapy.metamodels.bdd_metamodel.transformations import FmToBDD, DDDMPWriter

import app.utils as utils


def main(fm_filepath: str) -> None:
    fm_model = UVLReader(fm_filepath).transform()

    print(fm_model)
    for ctc in fm_model.get_constraints():
        print(f'{ctc.ast.pretty_str()} -> {ctc.ast.get_operators()} -> {ctc.ast.get_operands()}')

    UVLWriter('output.uvl', fm_model).transform()
    
    raise Exception
    metrics_result = FMMetrics().execute(fm_model).get_result()
    metrics_dict = {item["name"]: item for item in metrics_result}
    ordered_metrics = [
        metrics_dict[name] for name in utils.METRICS_ORDER if name in metrics_dict
    ]

    for metric in ordered_metrics:
        print(f"{metric['name']}: {metric['size']}")

    print(f'FM to BDD...')
    bdd_model = FmToBDD(fm_model).transform()
    DDDMPWriter('bdd_model.dddmp', bdd_model).transform()

    # print(f'#Features: {len(fm_model.get_features())}')
    # print(f'#Constraints: {len(fm_model.get_constraints())}')
    
    # sat_model = FmToPysat(fm_model).transform()
    # bdd_model = FmToBDD(fm_model).transform()

    # n_configs = BDDConfigurationsNumber().execute(bdd_model).get_result()
    # print(f'#Configs: {utils.int_to_scientific_notation(n_configs)}')

    # core_features = BDDCoreFeatures().execute(bdd_model).get_result()
    # print(f'Core features: ({len(core_features)}) {core_features}')

    # variation_points = FMVariationPoints().execute(fm).get_result()
    # print(f'Variations points:')
    # for vp, variant in variation_points.items():
    #     print(f'{vp} -> {variant}')

    # sampling_op = BDDSampling()
    # sampling_op.set_sample_size(5)
    # sample = sampling_op.execute(bdd_model).get_result()
    # configs_writer = ConfigurationsCSVWriter('configs.csv')
    # configs_writer.set_elements([f.name for f in fm.get_features()])
    # configs_writer.set_configurations(sample)
    # configs_writer.transform()

    # configs_reader = ConfigurationsCSVReader('configs.csv')
    # configs_reader.store_only_selected_elements(False)
    # sample2 = configs_reader.transform()
    # print(f'Equals: {set(sample) == set(sample2)}')

    # config_writer = ConfigurationsListWriter('configs.txt')
    # config_writer.set_configurations(sample)
    # config_writer.transform()

    # configs_reader.store_only_selected_elements(True)
    # sample3 = configs_reader.transform()
    # sample4 = ConfigurationsListReader('configs.txt').transform()
    # print(f'Equals: {set(sample3) == set(sample4)}')
    
    # configs_attributes = ConfigurationsAttributesReader('models/NamasteRincon_configs_simple.csv').transform()
    # print(f'#Products in portfolio: {len(configs_attributes)}')

    # pl_model = ProductLineModel()
    # pl_model.configurations = {config[0] for config in configs_attributes}
    # print(pl_model)
    # prod_dist_op = PLProductDistribution().execute(pl_model)
    # prod_dist = prod_dist_op.get_result()
    # desc_stats = prod_dist_op.descriptive_statistics()
    # print(f'Product distribution: {prod_dist}')
    # print(f'#Product dist: {sum(prod_dist)}')
    # print(desc_stats)
    
    # fif = PLFeatureInclusionFrequency().execute(pl_model).get_result()
    # fif = dict(sorted(fif.items(), key=lambda item: item[1]))
    # print(f'Feature Inclusion Frequency:\n')
    # for feature, freq in fif.items():
    #     print(f'{feature}: {freq}')
    # raise Exception
    
    # for config_attr in configs_attributes:
    #     satis_config_op = BDDSatisfiableConfiguration()
    #     satis_config_op.set_configuration(config_attr[0], is_full=False)
    #     satis = satis_config_op.execute(bdd_model).get_result()
    #     print(f'{config_attr[0]} -> {satis}')
    
    # print("full configurations:")
    # false_configs = []
    # full_configs = []
    # for config_attr in configs_attributes:
    #     full_config_op = FullConfigurations()
    #     full_config_op.set_configuration(config_attr[0])
    #     new_configs = full_config_op.execute(sat_model).get_result()
    #     print(new_configs)
    #     full_configs.extend(new_configs)
    #     for config in new_configs:
    #         satis_config_op = BDDSatisfiableConfiguration()
    #         satis_config_op.set_configuration(config, is_full=True)
    #         satis = satis_config_op.execute(bdd_model).get_result()
    #         print(f'{config} -> {satis}')
    #         if not satis:
    #             false_configs.append((config_attr, config))
    # config_writer = ConfigurationsListWriter('full_configs.txt')
    # config_writer.set_configurations(full_configs)
    # config_writer.transform()
    # print(f'Invalid configs: {false_configs}')



if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    parser = argparse.ArgumentParser(description='Product Line analysis.')
    parser.add_argument(metavar='fm', dest='fm_filepath', type=str, help='Input feature model (.uvl).')
    args = parser.parse_args()

    main(args.fm_filepath)
