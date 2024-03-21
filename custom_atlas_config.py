from __future__ import print_function
import os
import warnings
import enum
import json
import numpy as np
import cv2
from translate_colors import TranslateColors
from translate_colors import UnknownCustomAtlasError
from roi_info import ROIInfo, INDEX2ROI
from path_spector import PathSpector


class AtlasAssetType(enum.Enum):
    RGBAtlas = 1
    Wireframe = 2
    AnnotatedBWAtlas = 3
    AnnotatedColorAtlas = 4

    def asset_dir(self, custom_atlas="ARA"):
        CustomAtlasConfig.assert_is_valid_atlas(custom_atlas)
        root = self.asset_root_dir()
        subdir = CustomAtlasConfig.atlas_subdir(custom_atlas)
        return os.path.join(root, subdir)

    def asset_root_dir(self):
        if self is AtlasAssetType.RGBAtlas:
            return CustomAtlasConfig.ATLAS_COMMON_DIR
        elif self is AtlasAssetType.Wireframe:
            return CustomAtlasConfig.ATLAS_WIRE_COMMON_DIR
        elif self is AtlasAssetType.AnnotatedBWAtlas:
            return CustomAtlasConfig.ATLAS_ANN_BW_COMMON_DIR
        elif self is AtlasAssetType.AnnotatedColorAtlas:
            return CustomAtlasConfig.ATLAS_ANN_RGB_COMMON_DIR

    def asset_name(self, custom_atlas, level):
        CustomAtlasConfig.assert_is_valid_atlas(custom_atlas)
        level = CustomAtlasConfig.clean_level_str(level=level)
        if self is AtlasAssetType.RGBAtlas:
            basename = CustomAtlasConfig.CUSTOM_ATLAS_POSTFIX[custom_atlas]
            use_fmt = False
        elif self is AtlasAssetType.Wireframe:
            basename = CustomAtlasConfig.CUSTOM_WIRE_FORMAT[custom_atlas]
            use_fmt = True
        elif self is AtlasAssetType.AnnotatedBWAtlas:
            basename = CustomAtlasConfig.CUSTOM_ANN_FORMAT[custom_atlas]
            use_fmt = True
        elif self is AtlasAssetType.AnnotatedColorAtlas:
            basename = CustomAtlasConfig.CUSTOM_ANN_FORMAT[custom_atlas]
            use_fmt = True
        if use_fmt:
            return basename.format(level)
        else:
            return level + basename

    def asset_path(self, custom_atlas, level, local=True):
        asset_dir = self.asset_dir(custom_atlas=custom_atlas)
        asset_name = self.asset_name(custom_atlas=custom_atlas, level=level)
        ret_path = os.path.join(asset_dir, asset_name)
        if local:
            return PathSpector.normalize_path_to_os(ret_path)
        else:
            return ret_path


class CustomAtlasConfig:
    """
    CustomAtlasConfig class
    holds TranslateColors and ROIInfo class instantiated from custom_atlas
    can also act as a filter to select desired roi to include in analysis.
    maybe interface with ui. placeholder for now
    """
    ATLAS_COMMON_DIR = "/ifs/loni/faculty/dong/mcp/atlas_roigb"
    ATLAS_WIRE_COMMON_DIR = ATLAS_COMMON_DIR + '/full_black_borders/'
    ATLAS_ANN_BW_COMMON_DIR = ATLAS_COMMON_DIR + '/annotated_bw_atlas/'
    ATLAS_ANN_RGB_COMMON_DIR = ATLAS_COMMON_DIR + '/annotated_color_atlas/'

    DEFAULT_ATLAS = 'ARA'

    CUSTOM_ATLAS_STABLE_VER = {
        "ARA": "v1",
        "CP_VORONOI": "v1",
        "CPR_VORONOI": "v2",
        "CPI_VORONOI": "v1",
        "CPC_VORONOI": "v1",
        "BLAA_DIVISIONS": "v2",
        "DP": "v1",
        "SC_DIVISIONS": "v3"
    }

    CUSTOM_ATLAS_POSTFIX = {
        "ARA": "_2013_rgb-01_append.tif",
        "CP_VORONOI": "_cp_voronoi.tif",
        "CPC_VORONOI": "_cp_voronoi.tif",
        "CPI_VORONOI": "_cp_voronoi.tif",
        "CPR_VORONOI": "_cp_voronoi.tif",
        "BLAA_DIVISIONS": "_ARA-Coronal-BLAA_Divisions.tif",
        "DP": "_dp.tif",
        "SC_DIVISIONS": "_SC_rgb_atlas.tif"
    }
    CUSTOM_WIRE_FORMAT = {
        "ARA": "{}_ARA_borders.tif",
        # TODO generate associated assets, decide on name
        "BLAA_DIVISIONS": "{}_borders.tif",
        "CP_VORONOI": '{}_borders.tif',
        "CPC_VORONOI": "{}_cp_voronoi.tif",
        "CPI_VORONOI": "{}_cp_voronoi.tif",
        "CPR_VORONOI": "{}_cp_voronoi.tif",
        "DP": "todo_{}.tif",
        "SC_DIVISIONS": "todo_{}.tif"
    }
    # TODO decide if use comon name for BW and COLOR Annotated
    CUSTOM_ANN_FORMAT = {
        "ARA": "ARA-Coronal-{}_full_labels.tif",
        # TODO generate associated assets, decide on name
        "BLAA_DIVISIONS": "todo_{}.tif",
        "CP_VORONOI": "todo_{}.tif",
        "CPC_VORONOI": "{}_cp_voronoi.tif",
        "CPI_VORONOI": "{}_cp_voronoi.tif",
        "CPR_VORONOI": "{}_cp_voronoi.tif",
        "DP": "todo_{}.tif",
        "SC_DIVISIONS": "todo_{}.tif"
    }

    CUSTOM_ATLAS_SUBDIR_NAME = {
        "ARA": "",
        "CP_VORONOI": "cp_voronoi",
        "CPR_VORONOI": "cpr_voronoi",
        "CPI_VORONOI": "cpi_voronoi",
        "CPC_VORONOI": "cpc_voronoi",
        "BLAA_DIVISIONS": 'blaa_divisions',
        "DP": 'dp',
        "SC_DIVISIONS": "sc"
    }

    def __init__(self, custom_atlas=DEFAULT_ATLAS):
        self.assert_is_valid_atlas(custom_atlas)
        self._associated_atlas = custom_atlas
        self.rgb_codec = TranslateColors(self._associated_atlas)
        self.roi_info = ROIInfo(self.rgb_codec)
        self.version = CustomAtlasConfig.CUSTOM_ATLAS_STABLE_VER[self._associated_atlas]
        self.filtered = False

    def __eq__(self, other):
        err_msg = "operator == between CustomAtlasConfig and another type is not defined"
        assert isinstance(other, CustomAtlasConfig), err_msg
        return self._associated_atlas == other._associated_atlas

    def __ne__(self, other):
        err_msg = "operator != between CustomAtlasConfig and another type is not defined"
        assert isinstance(other, CustomAtlasConfig), err_msg
        return self._associated_atlas != other._associated_atlas

    def same_version(self, other):
        if not isinstance(other, CustomAtlasConfig):
            warnings.warn("different associated atlases provided. "
                          "version comparision not meaningful. returning false")
            return False
        return self.version == other.version

    def level_rgb_atlas_path(self, level):
        '''
        see CustomAtlasConfig.gen_atlas_path
        '''
        return CustomAtlasConfig.gen_atlas_path(
            level, custom_atlas=self._associated_atlas)

    def level_wire_atlas_path(self, level):
        '''
        see CustomAtlasConfig.gen_wire_path
        '''
        return CustomAtlasConfig.gen_wire_path(
            level, custom_atlas=self._associated_atlas)

    def level_ann_bw_atlas_path(self, level):
        '''
        see CustomAtlasConfig.gen_ann_bw_path
        '''
        return CustomAtlasConfig.gen_ann_bw_path(
            level, custom_atlas=self._associated_atlas)

    def level_ann_color_atlas_path(self, level):
        '''
        see CustomAtlasConfig.gen_ann_color_path
        '''
        return CustomAtlasConfig.gen_ann_color_path(
            level, custom_atlas=self._associated_atlas)

    '''
    # probably don't need this
    def level_asset_path(self, level, asset_type):
        if asset_type is AtlasAssetType.RGBAtlas:
            return self.level_rgb_atlas_path(level)
        elif asset_type is AtlasAssetType.Wireframe:
            return self.level_rgb_atlas_path(level)
        elif asset_type is AtlasAssetType.AnnotatedBWAtlas:
            return self.level_rgb_atlas_path(level)
        elif asset_type is AtlasAssetType.AnnotatedColorAtlas:
            return self.level_rgb_atlas_path(level)
    '''

    @staticmethod
    def gen_wire_path(level, custom_atlas='ARA'):
        '''
        generate path to full size wireframe for selected atlas rgb image
        if not found for custom atlas returns ARA instead
        '''
        asset_type = AtlasAssetType.Wireframe
        return CustomAtlasConfig.gen_level_asset_atlas_path(
            level, asset_type, custom_atlas)

    @staticmethod
    def gen_atlas_path(level, custom_atlas="ARA"):
        """
        generate atlas path for level and specified custom atlas
        if no atlas defined for given level and custom atlas combination,
        return custom_atlas, path to ara atlas
        otherwise, return ARA, path to custom atlas
        """
        asset_type = AtlasAssetType.RGBAtlas
        return CustomAtlasConfig.gen_level_asset_atlas_path(
            level, asset_type, custom_atlas)

    @staticmethod
    def gen_ann_bw_path(level, custom_atlas="ARA"):
        """
        generate annotated bw atlas path for level and specified custom atlas
        if no atlas defined for given level and custom atlas combination,
        return custom_atlas, path to ara atlas
        otherwise, return ARA, path to custom atlas
        """
        asset_type = AtlasAssetType.AnnotatedBWAtlas
        return CustomAtlasConfig.gen_level_asset_atlas_path(
            level, asset_type, custom_atlas)

    @staticmethod
    def gen_ann_color_path(level, custom_atlas='ARA'):
        """
        generate annotated color atlas path for level and specified custom atlas
        if no atlas defined for given level and custom atlas combination,
        return custom_atlas, path to ara atlas
        otherwise, return ARA, path to custom atlas
        """
        asset_type = AtlasAssetType.AnnotatedColorAtlas
        return CustomAtlasConfig.gen_level_asset_atlas_path(
            level, asset_type, custom_atlas)

    @staticmethod
    def gen_level_asset_atlas_path(level, asset_type, custom_atlas):
        CustomAtlasConfig.assert_is_valid_atlas(custom_atlas)
        level = CustomAtlasConfig.clean_level_str(level)
        atlas_path = asset_type.asset_path(custom_atlas, level)
        if os.path.isfile(atlas_path):
            return custom_atlas, atlas_path
        else:
            atlas_path = asset_type.asset_path('ARA', level)
            assert os.path.isfile(atlas_path), "Cannot Generate Asset"
            return "ARA", atlas_path

    @staticmethod
    def clean_level_str(level):
        if isinstance(level, int):
            if level < 10:
                level = "00" + str(level)
            elif level < 100:
                level = '0' + str(level)
            else:
                level = str(level)
        if isinstance(level, str) and len(level) != 3:
            raise ValueError("incorrect ara level format")
        return level

    @classmethod
    def atlas_version(cls, custom_atlas):
        cls.assert_is_valid_atlas(custom_atlas)
        return cls.CUSTOM_ATLAS_STABLE_VER[custom_atlas]

    @classmethod
    def atlas_subdir(cls, custom_atlas):
        cls.assert_is_valid_atlas(custom_atlas)
        if custom_atlas == "ARA":
            return ""
        version = cls.atlas_version(custom_atlas)
        subdir = cls.CUSTOM_ATLAS_SUBDIR_NAME[custom_atlas]
        return os.path.join(subdir, version)

    @staticmethod
    def is_valid_atlas(custom_atlas):
        return custom_atlas in TranslateColors.CUSTOM_ATLAS_LOOKUP

    @classmethod
    def assert_is_valid_atlas(cls, custom_atlas):
        if not cls.is_valid_atlas(custom_atlas):
            raise UnknownCustomAtlasError(custom_atlas)

    @staticmethod
    def get_level_rois(level, custom_atlas='ARA', bilateral=True):
        if not 1 <= level <= 132:
            raise ValueError('atlas level out of range')
        level_str = '0' * (3 - len(str(level))) + str(level)
        atlas_dir = os.path.join(CustomAtlasConfig.ATLAS_COMMON_DIR,
                                 CustomAtlasConfig
                                 .CUSTOM_ATLAS_SUBDIR[custom_atlas])
        atlas_level_rois_json_path = os.path.join(
            atlas_dir, '{}_level_rois.json'.format(custom_atlas))
        with open(atlas_level_rois_json_path, 'r') as f:
            m = json.load(f)
        level_rois = set()
        if bilateral:
            for roi in m[level_str]:
                level_rois.add('{}_ipsi'.format(roi))
                level_rois.add('{}_contra'.format(roi))
        else:
            level_rois = set(m[level_str])
        return level_rois

    @staticmethod
    def _get_rgb_code_levels(rgb_indices, custom_atlas='ARA'):
        rgb_indices_level_mappings = {}
        for rgb_index in rgb_indices:
            rgb_indices_level_mappings[rgb_index] = []
        for level in range(1, 133):
            print(level)
            _, atlas_path = CustomAtlasConfig.gen_atlas_path(level, custom_atlas)
            rgb_atlas = cv2.imread(atlas_path, -1)
            index_atlas = TranslateColors.rgbatlas_to_indexatlas(rgb_atlas)
            unique_indices = set(np.unique(index_atlas))
            for rgb_index in rgb_indices:
                if rgb_index in unique_indices:
                    rgb_indices_level_mappings[rgb_index].append(level)
                    print('found {}: {} at custom atlas {} level {}'
                          .format(rgb_index, INDEX2ROI[rgb_index],
                                  custom_atlas, level))
        return rgb_indices_level_mappings

    @staticmethod
    def _build_custom_atlas_level_roi(custom_atlas='ARA'):
        if custom_atlas not in TranslateColors.CUSTOM_ATLAS_LOOKUP:
            raise UnknownCustomAtlasError(custom_atlas)
        out_dir = os.path.join(CustomAtlasConfig.ATLAS_COMMON_DIR,
                               CustomAtlasConfig
                               .CUSTOM_ATLAS_SUBDIR[custom_atlas])
        out_path = os.path.join(out_dir,
                                '{}_level_rois.json'.format(custom_atlas))
        level_rois = {}
        for level in range(1, 133):
            _, atlas_path = CustomAtlasConfig.gen_atlas_path(level,
                                                             custom_atlas)
            level_str = '0' * (3 - len(str(level))) + str(level)
            print('custom atlas {} level {}: {}'
                  .format(custom_atlas, level_str, atlas_path))
            rgb_atlas = cv2.imread(atlas_path, -1)
            index_atlas = TranslateColors.rgbatlas_to_indexatlas(rgb_atlas)
            unique_indices = np.unique(index_atlas)
            unique_rois = [INDEX2ROI[unique_index]
                           for unique_index in unique_indices]
            print(unique_rois)
            level_rois[level_str] = unique_rois
        with open(out_path, 'w') as f:
            json.dump(level_rois, f, indent=1, sort_keys=True)
