import os.path
from translate_colors import TranslateColors
from roi_info import ROIInfo
from csv_parser import RoiCsvParser


class LevelConnectivity:
    """
    csv_parser: RoiCsvParser object
    df: 'rgb_index', 'hemisphere', 'atlas_only', 'overlap', 'area'
    df_grey_matter: rows of df which belong to grey matter
    """
    def __init__(self, csv_path):
        assert os.path.isfile(csv_path), "{} does not exist".format(csv_path)
        self.csv_parser = RoiCsvParser(csv_path)
        self.roi_info = ROIInfo(TranslateColors(custom_atlas=self.csv_parser.custom_atlas()))
        self.df = self.csv_parser.parse_data()
        self.df['area'] = self.df['atlas_only'] + self.df['overlap']
        self.df['rgb_index'] = self.df['region'].apply(lambda roi: self.roi_info.roi2index[roi])

    # returns the columns rgb_index, hemisphere, overlap, area
    def connectivity(self, grey_matter=True):
        if grey_matter:
            return self.df.loc[self.df['rgb_index'].isin(self.roi_info.gray_matter_indices),
                               ['rgb_index', 'hemisphere', 'overlap', 'area']]
        else:
            return self.df[['rgb_index', 'hemisphere', 'overlap', 'area']]

