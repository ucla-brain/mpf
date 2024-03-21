from __future__ import print_function
import os
from abc import ABCMeta, abstractmethod
import warnings
import pandas as pd
from translate_colors import TranslateColors
from roi_info import LEGACY_MISSPELLED_ROIS, ROIInfo
from tracers_and_regions import TracersAndRegions


class CsvParser(object):
    __metaclass__ = ABCMeta

    def __init__(self, csv_path):
        if not os.path.isfile(csv_path):
            raise ValueError('{} is not a file'.format(csv_path))
        self._csv_path = csv_path
        self._meta_info = CsvParser.init_meta_info()
        # search maximum of 20 lines for metalines
        self._max_metalines = 20
        self.parse_metalines()
        self.assert_supported()

    @staticmethod
    def init_meta_info():
        meta_info = {
            'Project Name': None,
            'Case Name': None,
            'Slide Number': None,
            'Channel Number': None,
            'ARA Level': None,
            'Tracer': None,
            'Injection Site': None,
            'Secondary Injection Site': None,
            'Atlas Name': None,
            'Atlas Version': None,
            'Overlap Format': None,
            # only applicable for grid overlap output
            'Grid Size': None,
            'Threshold Adjusted': None,
            'Connection Lens Version': None
        }
        return meta_info

    @abstractmethod
    def _metaline_end_token(self):
        pass

    def equal_metalines(self, other):
        assert isinstance(other, CsvParser)
        return self._meta_info == other._meta_info

    def project_name(self):
        return self._meta_info['Project Name']

    def case_name(self):
        return self._meta_info['Case Name']

    def slide_number(self):
        return self._meta_info['Slide Number']

    def is_roi_mode(self):
        return os.path.basename(self._csv_path).find('grid') < 0

    def tracer(self):
        tracer_tokens = self._meta_info['Tracer'].split()
        return tracer_tokens[0]

    def injection_site(self):
        return self._meta_info['Injection Site']

    def channel_number(self):
        return self._meta_info['Channel Number']

    def is_cell_count(self):
        return not self.is_anterograde() and self._csv_path.endswith('cellcount.csv')

    def is_anterograde(self):
        if self.tracer() not in TracersAndRegions.TRACERTOTYPE:
            raise ValueError('unknown tracer <{}>'.format(self.tracer()))
        return TracersAndRegions.TRACERTOTYPE[self.tracer()] in {TracersAndRegions.TRACER_ANT, TracersAndRegions.TRACER_EITHER}   # bda is classified as either

    def custom_atlas(self):
        return self._meta_info['Atlas Name']

    def ara_level_str(self):
        return self._meta_info['ARA Level']

    def ara_level(self):
        return int(self.ara_level_str())

    @abstractmethod
    def assert_supported(self):
        pass

    def parse_metalines(self):
        n = 0
        with open(self._csv_path, 'r') as f:
            for l in f:
                if n == self._max_metalines:
                    break
                kv = l.strip().split(':')
                if len(kv) != 2:
                    continue
                key, value = kv
                if key in self._meta_info:
                    self._meta_info[key] = value.strip()
                n += 1


class RoiCsvParser(CsvParser):
    def __init__(self, csv_path):
        super(RoiCsvParser, self).__init__(csv_path)
        self.rgb_codec = TranslateColors(custom_atlas=self.custom_atlas())
        self.roi_info = ROIInfo(self.rgb_codec)

    # if (HEMISPHERE:R:G:B) not found, the file's version is old and unsupported
    def _metaline_end_token(self):
        return '(HEMISPHERE:R:G:B)'

    # search maximum of 20 lines for metaline end token
    def assert_supported(self):
        assert self.is_roi_mode(), '{} is not roi based'.format(self._csv_path)
        n = 0
        with open(self._csv_path, 'r') as f:
            for l in f:
                if l.startswith(self._metaline_end_token()):
                    return
                n += 1
                if n == self._max_metalines:
                    raise ValueError('the roi overlap is from an older unsupported '
                                     'version of connection lens. please re-run overlap')

    def known_roi(self, roi):
        roi = roi.strip()
        return roi in self.roi_info.roi2index or roi in LEGACY_MISSPELLED_ROIS

    def parse_data(self):
        """
        return a dataframe with following columns parsed from csv file
        hemisphere, atlas_only, overlap, region
        :return:
        """
        data = {
            'hemisphere': [],
            'atlas_only': [],
            'overlap': [],
            'region': []
        }
        is_dataline = False
        with open(self._csv_path, 'r') as f:
            for l in f:
                if l.startswith(self._metaline_end_token()):
                    is_dataline = True
                    continue
                if not is_dataline:
                    continue
                hemi_rgb, atlas_only, overlap, region = l.strip().split(',')
                region = region.strip()
                hemi, r, g, b = hemi_rgb.strip()[1:-1].split(':')
                atlas_only = float(atlas_only)
                overlap = float(overlap)
                area = atlas_only + overlap
                if not self.known_roi(region):
                    warnings.warn("unknown roi {} encountered, discarding line".format(region),
                                  RuntimeWarning)
                    continue
                if region in LEGACY_MISSPELLED_ROIS:
                    region = LEGACY_MISSPELLED_ROIS[region]
                if area == 0:
                    warnings.warn("area of {} at {} level {} is zero. forcing overlap to zero. "
                                  .format(region, self.custom_atlas(), self.ara_level_str()),
                                  RuntimeWarning)
                    overlap = 0
                data['hemisphere'].append(hemi)
                data['atlas_only'].append(atlas_only)
                data['overlap'].append(overlap)
                data['region'].append(region)
        return pd.DataFrame(data=data)


class GridCsvParser(CsvParser):
    def __init__(self, csv_path):
        super(GridCsvParser, self).__init__(csv_path)
        self._meta_info['Grid Size'] = None
        # supported criteria TBD

    def _metaline_end_token(self):
        pass

    def assert_supported(self):
        pass

