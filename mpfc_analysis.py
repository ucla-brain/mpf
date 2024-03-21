import os
from src.path_spector import PathSpector
from src.tracer_connectivity import TracerConnectivity
from src.tracer_analysis import TracerAnalysis

mpfc_case_dir = os.path.join(PathSpector.MCP,
                             "muye/manuscripts/dp_ila_ttd/cases")
mpfc_analysis_dir = os.path.join(PathSpector.MCP,
                                 "muye/manuscripts/dp_ila_ttd/cases/analysis")
mpfc_antereo_cases = ["SW151027-02B/overlap/2",  # cv-DP
                      "SW160120-01B/overlap/2",  # cv-DP
                      "SW160120-03A/overlap/4",  # cv-DP
                      "SW160120-03A/overlap/2",  # DP + cv-DP
                      "SW170420-03A/overlap/2",  # deep DP, not cv
                      "SW170420-03A/overlap/4",  # ACAd + PL + MOs
                      "SW120404-01A/overlap/2",  # ILA
                      "SW120404-02A/overlap/2",   # ILA
                      ]
mpfc_retro_cases = ["SW151027-02B/overlap/4",  # DP
                    "SW160120-01B/overlap/5",  # DP
                    "SW160120-03A/overlap/5",  # DP
                    "SW160120-03A/overlap/3",  # TTd
                    "SW120404-02A/overlap/5",  # ILA
                    "SW120404-02A/overlap/3",  # PL
                    "SW120404-01A/overlap/3",  # PL
                    ]


def write_mpfc_connections():
    antereo_analysis.write_connections(mpfc_analysis_dir,
                                       sortby_field='overlap',
                                       analysis_name='mpfc_anterograde')

    retro_analysis.write_connections(mpfc_analysis_dir,
                                     sortby_field='overlap',
                                     analysis_name='mpfc_retrograde')


def write_eigen_fractions():
    pass


if __name__ == '__main__':
    mpfc_antereo_injections = [TracerConnectivity(os.path.join(mpfc_case_dir,
                                                               case))
                               for case in mpfc_antereo_cases]
    antereo_analysis = TracerAnalysis(mpfc_antereo_injections,
                                      mpfc_analysis_dir,
                                      analysis_name='mpfc_anterograde')
    #antereo_analysis.principal_dimensions()
    antereo_analysis.cluster_2d(use_matrix='rank_k', k=5)
    mpfc_retro_injections = [
        TracerConnectivity(os.path.join(mpfc_case_dir, case))
        for case in mpfc_retro_cases]
    retro_analysis = TracerAnalysis(mpfc_retro_injections,
                                    mpfc_analysis_dir,
                                    analysis_name='mpfc_retrograde')
    retro_analysis.principal_dimensions()
    retro_analysis.cluster_2d(use_matrix='rank_k', k=5)
    #retro_analysis.generate_dendrogram()