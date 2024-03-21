from __future__ import print_function, division
import os
import re
from collections import defaultdict
import pandas as pd
from level_connectivity import LevelConnectivity
from custom_atlas_config import CustomAtlasConfig


class TracerConnectivity:
    """
    TracerConnectivity class:
    connectivity of all sections from a single tracer in a single case
    all rois present in the atlas are included in the data frame
    dataframe:
       tracer_connectivity. index: hemisphere roi names
         [roi_index, hemisphere, overlap, area]
    overlap_dir: directory where csv files are located
    csv_names: list of csv files to include under overlap_dir. for each instance, all csv files are expected to have
    the same meta info. see self.get_meta_info
    injection_site: can be str or dict. if str, it overwrites injection site parsed from csv files. if dict, 2 types of
    keys are accepted: injection site roi string, (case_id, channel) tuple. roi string take precedence, channel is expected
    to be str type
    injection site parsed from csv file is a key of the dict, replace with dict value of the key
    """

    def __init__(self, overlap_dir, csv_names=None, injection_site=None, injection_site_level=None):
        if not os.path.isdir(overlap_dir):
            raise ValueError('{} does not exist'.format(overlap_dir))
        self.overlap_dir = overlap_dir

        if csv_names is None:
            self.csv_names = [name for name in os.listdir(self.overlap_dir) if name.endswith('.csv')]
        else:
            self.csv_names = csv_names

        # ara level int: LevelConnectivity object
        self.level_connectivities = {}
        self.construct_level_connectivities()
        if len(self.level_connectivities) == 0:
            raise ValueError('no LevelConnectivity objects constructed from {}'.format(overlap_dir))

        # by default include all ara levels
        self.ara_level_subset = set([ara_level for ara_level in self.level_connectivities])

        self.project_name = self.case_name = self.tracer = self.channel_number = \
            self.injection_site = self.anterograde = self.cell_count = self.custom_atlas = None
        self.get_meta_info()

        self.custom_atlas_config = CustomAtlasConfig(self.custom_atlas)

        if isinstance(injection_site, str):
            self.injection_site = injection_site
        elif isinstance(injection_site, dict):
            if self.injection_site in injection_site:
                self.injection_site = injection_site[self.injection_site]
            elif (self.case_name, self.channel_number) in injection_site:
                self.injection_site = injection_site[(self.case_name, self.channel_number)]
        # injection site level is None (unknown) by default
        self.injection_site_level = injection_site_level

        # contains all roi in the custom atlas, even if the particular roi does
        # not appear in the levels present for the channel
        self.tracer_connectivity = None
        self.build_tracer_connectivity()

    def set_injection_site(self, injection_site, injection_site_level=None):
        self.injection_site, self.injection_site_level = injection_site, injection_site_level

    # if subset is None, all ara levels are added to the subset. for levels not within the subset, they are treated
    # as if the data from these levels were not observed. self.tracer_connectivity is rebuilt based on subset
    def set_ara_level_subset(self, ara_level_subset=None):
        if self.ara_level_subset != ara_level_subset:
            self.ara_level_subset = ara_level_subset
        if self.ara_level_subset is None:
            self.ara_level_subset = set([ara_level for ara_level in self.level_connectivities])
        self.build_tracer_connectivity()

    def construct_level_connectivities(self):
        for csv_name in self.csv_names:
            level_connectivity = LevelConnectivity(os.path.join(self.overlap_dir, csv_name))
            ara_level = level_connectivity.csv_parser.ara_level()
            self.level_connectivities[ara_level] = level_connectivity

    def get_meta_info(self):
        ara_levels = [k for k in self.level_connectivities.keys()]
        csv_parser0 = self.level_connectivities[ara_levels[0]].csv_parser
        self.project_name = csv_parser0.project_name()
        self.case_name = csv_parser0.case_name()
        self.tracer = csv_parser0.tracer()
        self.channel_number = csv_parser0.channel_number()
        self.injection_site = csv_parser0.injection_site()
        print(self.case_name, ara_levels[0], self.channel_number, self.tracer, self.injection_site)
        self.anterograde = csv_parser0.is_anterograde()
        self.cell_count = csv_parser0.is_cell_count()
        self.custom_atlas = csv_parser0.custom_atlas()

        for ara_level in ara_levels[1:]:
            try:
                csv_parser = self.level_connectivities[ara_level].csv_parser
                assert self.project_name == csv_parser.project_name()
                assert self.case_name == csv_parser.case_name()
                assert self.tracer == csv_parser.tracer()
                assert self.channel_number == csv_parser.channel_number()
                assert self.injection_site == csv_parser.injection_site()
                assert self.anterograde == csv_parser.is_anterograde()
                assert self.cell_count == csv_parser.is_cell_count()
                assert self.custom_atlas == csv_parser.custom_atlas()
            except AssertionError:
                raise AssertionError('meta data info conflict in case {} channel {} at ara {} and ara {}'
                                     .format(self.case_name, self.channel_number, ara_levels[0], ara_level))

    # for ara levels not in the subset, during tracer connectivity construction,
    # replace overlap and area values from these levels with 0
    def build_tracer_connectivity(self):
        # level connectivity data
        connectivity = pd.concat([level_connectivity.connectivity()
                                  .assign(overlap=lambda df: df.overlap * int(ara_level in self.ara_level_subset),
                                          area=lambda df: df.area * int(ara_level in self.ara_level_subset))
                                  for ara_level, level_connectivity in self.level_connectivities.items()])
        # group by roi_index and hemisphere, sum overlap and area
        connectivity = connectivity.groupby(['rgb_index', 'hemisphere']).sum().reset_index()
        # roi indices in atlas but did not appear in csv files
        remainder_indices = list(set(self.custom_atlas_config.roi_info.gray_matter_indices) -
                                 set(connectivity['rgb_index']))
        remainder = pd.DataFrame({
            'rgb_index': remainder_indices * 2,
            'hemisphere': ['l'] * len(remainder_indices) + ['r'] * len(remainder_indices),
            'overlap': 0,
            'area': 0
        })
        # sort rgb_index and hemisphere ascending
        self.tracer_connectivity = pd.concat([connectivity, remainder])
        self.tracer_connectivity = self.tracer_connectivity.sort_values(by=['rgb_index', 'hemisphere'])
        # roi_name column
        roi_name = self.tracer_connectivity['rgb_index'].apply(self.custom_atlas_config.rgb_codec.index_to_region)
        roi_name_hemi = roi_name.str.cat(others=self.tracer_connectivity['hemisphere']
                                                    .apply(lambda x: 'c' if x == 'l' else 'i'),
                                         sep='_')
        self.tracer_connectivity = self.tracer_connectivity.set_index(roi_name_hemi)
        self.tracer_connectivity.index.name = 'roi_name'

    # columns rgb_index, hemisphere, overlap, area, ara_level
    def tracer_connectivity_by_ara_levels(self):
        df_ara_levels = []
        for ara_level, level_connectivity in self.level_connectivities.items():
            df_ara_level = level_connectivity.connectivity()\
                           .assign(overlap=lambda df: df.overlap * int(ara_level in self.ara_level_subset),
                                   area=lambda df: df.area * int(ara_level in self.ara_level_subset))
            df_ara_level['ara_level'] = ara_level
            df_ara_levels.append(df_ara_level)
        return pd.concat(df_ara_levels)

    def case_tracer(self, series_insensitive=False):
        if not series_insensitive:
            return '{}_{}'.format(self.case_name, self.tracer)
        else:
            return '{}_{}'.format(re.match('[A-Z]{2}[0-9]{6}-[0-9]{2}', self.case_name).group(), self.tracer)

    # only return levels within ara_level_subset
    def ara_levels(self):
        return sorted([ara_level for ara_level in self.ara_level_subset])

    def top_overlap_rois(self, n):
        return self.tracer_connectivity.nlargest(n, 'overlap').index.values


# take an overlap directory with potentially a mix of cases and series,
# split them into distinct groups identified by case and series, and return
# one TracerConnectivity object for each
class TracerConnectivityBuilder:
    def __init__(self, overlap_dirs, injection_site_roi_mapper=None):
        self.overlap_dirs = overlap_dirs
        self.injection_site_roi_mapper = injection_site_roi_mapper
        self.tracer_connectivities = []
        self.build_tracer_connectivities()

    def build_tracer_connectivities(self):
        for overlap_dir in self.overlap_dirs:
            if not os.path.isdir(overlap_dir):
                raise ValueError('{} is not a directory'.format(overlap_dir))
            self._build_tracer_connectivities_in_dir(overlap_dir)

    def _build_tracer_connectivities_in_dir(self, overlap_dir):
        # do not add files repetitively
        overlap_files = defaultdict(set)
        for name in os.listdir(overlap_dir):
            if not name.endswith('.csv'):
                continue
            # series sensitive case format matching
            m = re.match(re.compile('[a-zA-Z]{2}[0-9]{6}-[0-9]{2}[A-Z]'), name)
            if not m:
                continue
            overlap_files[m.group()].add(name)
        for csv_names in overlap_files.values():
            self.tracer_connectivities.append(TracerConnectivity(overlap_dir, csv_names, injection_site=self.injection_site_roi_mapper))


