import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# import outspector modules
from roi_groups import GLOBAL_COARSE_MAPPING, HY_COARSE_MAPPING, ROI_GROUPS, ROI_MAPPINGS, GLOBAL_HIERARCHY_MAPPING
from roi_info import INDEX2ROI
from tracer_connectivity import TracerConnectivityBuilder
from tracer_analysis import TracerAnalysis


case_sheet = pd.read_csv('case_sheet.csv', dtype={'channel': str}).set_index(['case_id', 'channel'])


def get_connectivities():
    overlap_dirs = []
    for case_id, channel in case_sheet.index:
        print(case_id, channel)
        overlap_dir = os.path.join(case_id, 'overlap', channel)
        assert os.path.isdir(overlap_dir)
        overlap_dirs.append(overlap_dir)
    builder = TracerConnectivityBuilder(overlap_dirs, injection_site_roi_mapper=case_sheet['injection_site_coarse'].to_dict())
    connectivities = [tracer_connectivity for tracer_connectivity in builder.tracer_connectivities if tracer_connectivity.anterograde]
    return connectivities


def plot_data(data_type='fraction'):
    # Global 2d cluster heatmap
    analysis.select_data()
    analysis.cluster_2d(data_type, threshold_quantile=0.975, vis_ceil_val=0.1, title='all')

    # ROI group scatter plot
    for roi_group, roi_mapping in [('GLOBAL_HIERARCHY', 'GLOBAL_HIERARCHY'), ('CTX_DS', 'CTX_DS'),
                                   ('TH', None), ('HY', 'HY_COARSE'), ('AMY', 'AMY_COARSE'),
                                   ('HPF', 'HPF_COARSE'), ('MB', 'MB_COARSE'), ('HB', None),
                                   ('STR', 'STR_COARSE')]:

        analysis.select_data(roi_group_names=roi_group, roi_aggregate_rule=roi_mapping)
        analysis.append_total_columns()
        analysis.plot_data_scatter(data_type)

    # ROI group 2d cluster heatmap
    for roi_group, roi_mapping in [('GLOBAL_HIERARCHY', 'GLOBAL_HIERARCHY'), ('CTX_DS', 'CTX_DS'),
                                   ('SENSORY_CTX_DS', 'SENSORY_CTX_DS')]:
        analysis.select_data(roi_group_names=roi_group, roi_aggregate_rule=roi_mapping, case_aggregate_rule='combine_series')
        analysis.cluster_2d('fraction', threshold_quantile=0.85, vis_ceil_val=0.1, title=roi_group)


def main()


if __name__ == '__main__':
    cs = get_connectivities(os.getcwd())
    analysis = TracerAnalysis(cs)
    analysis.set_analysis_name('mpfc-analysis')
    analysis.set_output_dir(os.path.join(os.getcwd(), 'plots'))

    analysis.select_data(roi_group_names='CTX_COARSE', roi_aggregate_rule='CTX_COARSE')
    communities = analysis.community_detection('density')
    print(communities)
    from collections import defaultdict
    d = defaultdict(list)
    for name, cid in communities.iteritems():
        d[cid].append(name)
    for cid in d:
        print(cid, d[cid])
