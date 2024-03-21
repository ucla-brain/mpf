from copy import deepcopy
from translate_colors import TranslateColors, UnknownCustomAtlasError


NON_GRAYMATTER_ROIS = {
    "border_11", "BORDER10", "isl", "islm", "border9", "VL", "rc/sez", "V3", "SFO/V3", "AQ", "V4", "V4r",
    "central_canal", "BORDER1", "BORDER0", "amc", "BORDER3", "BORDER4", "BORDER5", "BORDER2", "border7",
    "border8", "BORDER6", "mtg", "mlf/ml", "sctv/sptV/rust/icp", "ts ", "sctv/sptV/rust", "arb/cbc",
    "icp", "tb/sctv/sptV/rust/vVlln/icp/arb", "py", "gVLLn", "tb/sctv/sptV/rust/vVllln", "VIIIn",
    "arbc/icp", "tb/sctv/sptV/rust/vlln", "ml/py", "Vlln", "py/tb/sctv/sptV/rust/Vlln", "arb",
    "py/tb/ml/sctv/sptV/vn/grf", "sctv", "sctv/ii", "mtv", "cic", "py/tb/ml/sctv/sptV/rust/vn",
    "mcp/sptV/tb/vn/rust", "sctv/mcp/sptV/tb/vn/rust", "sctv/ml/tb/py", "scp", "sctv/rust/ii", "moV",
    "sptV/tb/vn/mcp", "rust/ii", "py/tb/ml", "rust/ii/tb/ml/py", "mcp/vn", "ll", "dhc",
    "mcp/tb/ml/py/vn/rust/ii", "dscp/scp", "dhc/ec", "mcp/vn/rust/ii/py/ml", "mcp/ii", "mcp/cst/ml/ii",
    "dhc/ec/alv", "dscp", "cst/ml", "mcp/cpd/rust/ii", "scp/dtd/mlf", "tsp", "mcp/cst/ml/cpd/rust/bic",
    "scp/tsp/dtd", "rust", "mcp/cst/ml/cpd", "rust/scp/vtd/dtd/tsp", "bic", "vtd/rust", "alv",
    "fp/dhc/ec", "vtd", "mcp", "dhc/alv", "fp/ec", "mlf", "fr/mp", "rust/ml", "bsc/opt/cpd",
    "bsc/opt/cpd/mp", "csc", "fp/dhc/alv/ec", "mp", "cpd", "bsc/opt", "ccs/cing/alv/dhc/ec/alv/st", "pm",
    "smd", "bsc/opt/cpt", "ccg/cing/fi/alv/dhc/int/ec", "hsc", "pc", "ccg/cing/fi/alv/df/dhc/int/ec/amc",
    "bsc", "ccg/cing/fi/alv/df/int/ec/amc", "cpd/opt/st", "ml/em", "hbc",
    "ccg/cing/fi/alv/df/int/st/cpd/opt/ec/amc", "ml", "im", "cpd/opt", "fr", "em",
    "ccg/cing/fi/alv/df/ec/amc", "ccg/cing/fi/vhc/df/ec/amc", "mtt", "ccg/cing/fi/vhc/df/ec",
    "ccg/cing/df", "fi/vhc", "onl", "aco/lotd", "lot", "aco", "von", "fa", "fa/cing", "ccg/cing", "och",
    "int", "fx", "act", "aco/act", "st", "ect", "fi", "vhc", "ccg/cing/fi/vhc/df", "sm", "ccg/fi/cing",
    "df", "opt"
    }

LEGACY_MISSPELLED_ROIS = {
    'II': 'll', 'AON_': 'AON', 'COApI_1': 'COApl_1', 'COApI_2': 'COApl_2',
    'Ald_6b': 'AId_6b',
}

"""
ROI2INDEX and INDEX2ROI map rgb index (computed from (r, g, b) tuples) to and 
from roi name strings
"""

ROI2INDEX = {
    'MOs_6b': 2071637, 'MOs_6a': 2071638, 'PVR_pd': 15879739, 'AOB_gl': 10350801, 'FL_mo': 16775825,
    'mcp/cst/ml/cpd': 13421726, 'PRNr': 16759942, 'ccg/fi/cing': 13421791, 'SCm_dw': 16680441, 'AOB_gr': 10350799,
    'AON_1': 5554069, 'alv': 13421730, 'scp': 13421701, 'PRNc': 16759943, 'ANcr1_mo': 16774545, 'DCO': 16748754,
    'ZI_A13': 15884092, 'PYR_mo': 16772497, 'ANcr2_gr': 16774290, 'ts': 13421677, 'MEA_pd_c': 8437978,
    'MEA_pd_b': 8437977, 'MEA_pd_a': 8437976, 'ILA_6b': 5878621, 'TEa_6a': 1421487, 'SPA': 16744863,
    'POST_3': 4769852, 'POST_2': 4769853, 'fp/ec': 13421735, 'PERI_6a': 956033, 'PERI_6b': 956032,
    'sctv/mcp/sptV/tb/vn/rust': 13421699, 'AON_d': 5554066, 'AON_e': 5554064, 'PV_po': 15881533, 'GR': 16745938,
    'VAL': 16749727, 'AON_l': 5554065, 'AON_m': 5554068, 'PAR_2': 7525736, 'mlf': 13421736, 'dhc/alv': 13421734,
    'smd': 13421749, 'ml/em': 13421758, 'AUDv_6b': 103316, 'AUDv_6a': 103317, 'NPC': 16684287,
    'SSp_tr_2/3': 1601891, 'LAV': 16750290, 'PSTN': 15886395, 'ccg/cing/fi/vhc/df': 13421789, 'DTN': 16756102,
    'SSp_m_2/3': 1602659, 'PBl_ls': 16756874, 'AUDp_2/3': 103064, 'PBl_lv': 16756870, 'ml/py': 13421688,
    'SCs_op': 16680191, 'PTLp_6b': 40871, 'BST_rh': 11780055, 'SSs_2/3': 1605475, 'PBl_lc': 16756873,
    'ORBl_2/3': 2394717, 'PCG': 16755590, 'PBl_le': 16756871, 'PBl_ld': 16756872, 'VMH_dm': 15880765,
    'BORDER1': 11599800, 'BORDER0': 12573411, 'MOp_2/3': 2071897, 'BORDER2': 16740480, 'AIp_6a': 2201187,
    'BORDER4': 15790208, 'BORDER6': 16777215, 'CUL4/5_gr': 16775058, 'ZI': 15884091, 'AMB_v': 16754642,
    'VISl_4': 557450, 'RSPv_5': 1746325, 'RSPv_1': 1746328, 'RSPv_2': 1746327, 'sptV/tb/vn/mcp': 13421704,
    'aco/act': 13421784, 'VISC_4': 1158529, 'VISC_5': 1158528, 'AMB_d': 16754643, 'MOB_mi': 8570797,
    'sctv/rust/ii': 13421702, 'NLOT_3': 9823432, 'GRN': 16752338, 'CNspg': 16750035, 'IGL': 16744353,
    'py/tb/ml/sctv/sptV/vn/grf': 13421692, 'ME': 15879995, 'NTB': 16754130, 'MA': 10662360, 'MB': 16676607,
    'MM': 15887163, 'OT_1': 8441336, 'OT_2': 8441335, 'OT_3': 8441334, 'sAMY': 8437975, 'hbc': 13421759,
    'fa/cing': 13421778, 'SUBv_m': 4961863, 'MV': 16751314, 'MS': 9873619, 'csc': 13421742, 'NOT': 16677119,
    'PIR_2': 6998969, 'MY': 16745682, 'INC': 16680959, 'FS': 8441592, 'NTS_m': 16754386, 'NTS_l': 16754387,
    'SMT': 16747167, 'SCs_zo': 16680189, 'FC': 8312139, 'SCM_ig-a': 16680445, 'SCM_ig-c': 16680443,
    'SCM_ig-b': 16680444, 'SOC_m': 16757895, 'TRS': 9873106, 'RSPv_2/3': 1746326, 'VISpm_2/3': 557707,
    'ccg/cing/df': 13421770, 'PL_5': 3123277, 'PL_6': 3123274, 'PL_1': 3123281, 'PL_3': 3123278, 'PL_2': 3123280,
    'von': 13421776, 'CA2_sr': 8311629, 'CA2_sp': 8311628, 'SUBv_sp': 4961865, 'SUBv_sr': 4961864,
    'POST_1': 4769854, 'Ep_v': 10546844, 'V': 16758150, 'VMH_vl': 15880763, 'CA2_so': 8311627, 'ILA_2/3': 5878625,
    'PAR_1': 7525737, 'PAR_3': 7525735, 'TEa_6b': 1421486, 'scp/dtd/mlf': 13421721, 'ml': 13421761,
    'MARN': 16752850, 'SI': 9489389, 'SH': 9489388, 'SO': 15883067, 'mp': 13421744, 'DP_2/3': 10803875,
    'im': 13421762, 'VISpl_5': 557193, 'SG': 16754822, 'SF': 9489390, 'AUDd_1': 102809, 'AUDd_5': 102806,
    'AUDd_4': 102807, 'aco': 13421775, 'AIp_1': 2201190, 'VPL_pc': 16746912, 'bsc/opt': 13421746, 'AIp_5': 2201188,
    'CNlam': 16750034, 'COPY_gr': 16773266, 'aco/lotd': 13421773, 'BORDER10': 8437986, 'BST_BAC': 11780323,
    'LD': 16747679, 'LC': 16755078, 'LA': 10348700, 'LM': 15886907, 'LH': 16747935, 'SSp_tr_5': 1601889,
    'LT': 16679679, 'LP': 16745375, 'IAD': 16749983, 'VPM': 16745887, 'BST_if': 11780060, 'III': 16681983,
    'fr': 13421764, 'AId_6a': 2201698, 'MOs_6': 2071639, 'MM_me': 15887164, 'PVH_lp': 15881284, 'LING_mo': 16774033,
    'MOs_1': 2071642, 'fa': 13421777, 'rust/scp/vtd/dtd/tsp': 13421727, 'PRE_3': 5880135, 'PRE_2': 5880136,
    'PRE_1': 5880137, 'fi': 13421787, 'SSp_tr_1': 1601892, 'cst/ml': 13421719, 'FOTU_gr': 16772242, 'st': 13421785,
    'VISp_1': 558220, 'VISp_5': 558217, 'VISp_4': 558218, 'sm': 13421790, 'ORBm_3': 2394206, 'VISpl_1': 557196,
    'ORBm_1': 2394208, 'VISpl_4': 557194, 'ORBm_6': 2394202, 'ORBm_5': 2394204, 'ENTm_3': 3323427,
    'ENTm_2': 3323430, 'ENTm_1': 3323431, 'AHN_p': 15883837, 'ENTm_6': 3323424, 'ENTm_5': 3323425,
    'ENTm_4': 3323426, 'LIN': 16755410, 'ANcr1_gr': 16774546, 'AHN_c': 15883836, 'MOs_2/3': 2071641,
    'AHN_a': 15883835, 'SSp_tr_4': 1601890, 'CENT3_gr': 16774802, 'PVH_pv': 15881277, 'sctv/ii': 13421694,
    'RT': 16748703, 'AId_5': 2201700, 'AOB': 10350802, 'RR': 16683007, 'AId_1': 2201702, 'SAG': 16679167,
    'AD': 16749215, 'RE': 16750239, 'V3': 11184811, 'PRP': 16749778, 'RL': 16682495, 'RM': 16753874, 'RN': 16682751,
    'RO': 16755154, 'PFL_gr': 16776082, 'PM_v': 15880508, 'tsp': 13421722, 'gVLLn': 13421683, 'TM_d': 15886651,
    'ENTl_4/5': 3323935, 'TEa_1': 1421491, 'NOD_mo': 16773777, 'bsc/opt/cpd': 13421739, 'TTd_4': 6475932,
    'MRN': 16683775, 'TTd_1': 6475935, 'TTd_2': 6475934, 'VPL': 16746911, 'VISC_6a': 1158527,
    'bsc/opt/cpt': 13421750, 'PVH_mm': 15881280, 'MOB_gr': 8570796, 'VISC_6b': 1158526, 'IPN': 16680703,
    'ANCr2_mo': 16774289, 'ORBvl_6b': 2394457, 'SFO': 15888955, 'ORBvl_6a': 2394459, 'APN': 16684543,
    'MOB_gl': 8570798, 'CUL4/5_mo': 16775057, 'AId_6b': 2201697, 'em': 13421765, 'SFO/V3': 11184812,
    'RSPagl_1': 1746840, 'BST_mg': 11780057, 'PRC': 16685823, 'ect': 13421786, 'rc/sez': 11184810,
    'Scig_b': 16677375, 'ENTl_2/3': 3323937, 'CA2_slm': 8311630, 'AUDp_4': 103063, 'ORBl_6a': 2394715,
    'fx': 13421782, 'ORBl_6b': 2394713, 'VI': 16753362, 'mcp/cst/ml/ii': 13421716, 'sctv': 13421693,
    'MOs_5': 2071640, 'SSp_bfd_6b': 1602143, 'SSp_bfd_6a': 1602144, 'ACAv_6a': 4236643, 'VISal_2/3': 557963,
    'ACAv_6b': 4236642, 'PAA_2': 5888684, 'PAA_3': 5888683, 'PAA_1': 5888685, 'BST_dm': 11780054, 'V4r': 11184815,
    'sctv/ml/tb/py': 13421700, 'ORBm_6a': 2394203, 'EW': 16682239, 'IC_d': 16678910, 'PVH_ap': 15881278,
    'isl': 8441081, 'VIIIn': 13421685, 'FRP_1': 2527045, 'RSPagl_5': 1746838, 'fi/vhc': 13421771,
    'PRM_gr': 16773522, 'IO': 16754898, 'onl': 13421772, 'SIM_gr': 16775314, 'ORBm_2/3': 2394205, 'Y': 16748498,
    'TTv_2': 6475678, 'ISN': 16751826, 'VPM_pc': 16745888, 'ECT_1': 892817, 'ECT_5': 892815, 'IC_c': 16678911,
    'IC_e': 16678909, 'PVT': 16751519, 'rust/ii/tb/ml/py': 13421707, 'ccg/cing': 13421779, 'AM_v': 16749472,
    'PGRN_l': 16749522, 'ECU': 16747474, 'CENT2_mo': 16775569, 'PGRN_d': 16749523, 'AM_d': 16749471,
    'VTA': 16683519, 'SSp_ul_1': 1602916, 'B': 16755334, 'CLI': 16681727, 'SSp_ul_5': 1602913,
    'mcp/cpd/rust/ii': 13421720, 'COApl_1': 6416054, 'COApl_2': 6416053, 'VTN': 16677887, 'SSp_ll_2/3': 1603171,
    'PERI_2/3': 956035, 'BST_se': 11780061, 'ACAv_1': 4236646, 'ZI_FF': 15884093, 'BST_ju': 11780066,
    'KF': 16758406, 'arb': 13421691, 'CA3_slm': 8311375, 'VISpm_1': 557708, 'MOB_ipl': 8570800, 'VISpl_2/3': 557195,
    'ORBl_1': 2394718, 'VISpm_5': 557705, 'VISpm_4': 557706, 'ORBl_5': 2394716, 'PCN': 16746143, 'SSs_6a': 1605472,
    'SSs_6b': 1605471, 'MEA_ad': 8437980, 'DN': 16776849, 'NTS_ge': 16754388, 'AAA': 8438753, 'TR_3': 11070673,
    'TR_2': 11070674, 'TR_1': 11070675, 'PTLp_6a': 40872, 'ILA_1': 5878627, 'ILA_2': 5878626, 'ILA_3': 5878624,
    'Vlln': 13421689, 'RSPagl_2/3': 1746839, 'ENTl_2': 3323941, 'ENTl_3': 3323938, 'COApl_3': 6416052,
    'ENTl_1': 3323942, 'ENTl_6': 3323931, 'tb/sctv/sptV/rust/vVlln/icp/arb': 13421681, 'ENTl_4': 3323936,
    'ENTl_5': 3323934, 'DP_6a': 10803873, 'CENT3_mo': 16774801, 'TTv_3': 6475677, 'VISp_2/3': 558219,
    'POR': 16758918, 'vtd': 13421732, 'DG_mo': 8311115, 'RPA': 16752594, 'COAa_2': 6416310, 'POL': 16743839,
    'ccg/cing/fi/vhc/df/ec': 13421769, 'SSp_ll_1': 1603172, 'VISal_1': 557964, 'SSp_ll_4': 1603170,
    'SSp_ll_5': 1603169, 'VISal_5': 557961, 'VISal_4': 557962, 'AON_pv': 5554067, 'SSp_ul_4': 1602914,
    'SSp_2/3': 1605731, 'SN_c': 16683262, 'dscp': 13421718, 'VCO': 16753618, 'ORBm_2': 2394207, 'SLD': 16755846,
    'BST_AM': 11780064, 'BST_AL': 11780063, 'AUDPo_5': 103574, 'AUDPo_4': 103575, 'LRN_p': 16746706,
    'ccs/cing/alv/dhc/ec/alv/st': 13421747, 'mcp/cst/ml/cpd/rust/bic': 13421723,
    'ccg/cing/fi/alv/df/int/st/cpd/opt/ec/amc': 13421760, 'PVH_mpv': 15881276, 'PVH_f': 15881275, 'VMH_a': 15880766,
    'VMH_c': 15880764, 'PVH_a': 15881282, 'LRN_m': 16746707, 'PVH_mpd': 15881279, 'fr/mp': 13421737,
    'FRP_2/3': 2527044, 'PAS': 16755922, 'Gpi': 8755659, 'PERI_1': 956036, 'Gpe': 8755660, 'ILA_6a': 5878622,
    'PERI_5': 956034, 'SCm_dg': 16680447, 'PAG': 16684031, 'ENTl_6a': 3323933, 'VISl_5': 557449, 'och': 13421780,
    'VISl_1': 557452, 'mcp/ii': 13421715, 'ACVII': 16750546, 'SSp_bfd_5': 1602145, 'SSp_bfd_4': 1602146,
    'SSp_bfd_1': 1602148, 'bsc': 13421755, 'sctv/sptV/rust/icp': 13421676, 'IAM': 16750751,
    'mcp/tb/ml/py/vn/rust/ii': 13421711, 'df': 13421792, 'XII': 16747218, 'LDT': 16756358,
    'ccg/cing/fi/alv/df/dhc/int/ec/amc': 13421754, 'X': 16748242, 'ACAd_2/3': 4236901, 'BORDER3': 15090744,
    'SUM_m': 15880251, 'SUM_l': 15880252, 'LING_gr': 16774034, 'BORDER5': 16737535, 'LG_d': 16744352,
    'py/tb/ml': 13421706, 'ECT_6b': 892813, 'CA1_slm': 8311886, 'dhc/ec/alv': 13421717, 'VISp_6a': 558216,
    'VISp_6b': 558215, 'DG_sg': 8311116, 'AIp_6b': 2201186, 'border_11': 0, 'CUL_mo': 16776337, 'NTS_co': 16754390,
    'BMA_p': 8710784, 'AIp_2/3': 2201189, 'CA1_sr': 8311885, 'NTS_ce': 16754389, 'MEA_av': 8437979,
    'AId_2/3': 2201701, 'SSp_n_1': 1602404, 'AUDv_1': 103321, 'SSp_n_5': 1602401, 'SSp_n_4': 1602402,
    'DMX': 16746194, 'BMA_a': 8710785, 'PR': 16746655, 'PS': 15888443, 'PP': 16744095, 'AON': 5554063,
    'PT': 16751263, 'TEa_5': 1421488, 'PA': 9956499, 'PF': 16744607, 'PG': 16759430, 'SIM_mo': 16775313,
    'LS_c': 9489646, 'GU_2/3': 40052, 'ORBl_6': 2394714, 'PH': 15885627, 'PO': 16745631, 'AId_6': 2201699,
    'AUDpo_6b': 103572, 'SSp_ll_6b': 1603167, 'SSp_ll_6a': 1603168, 'CA3_slu': 8311373, 'DEC_mo': 16772753,
    'PL_2/3': 3123279, 'LS_r': 9489645, 'ORBvl_6': 2394458, 'ORBvl_5': 2394460, 'LS_v': 9489647, 'ORBvl_1': 2394462,
    'PFL_mo': 16776081, 'BLA_a': 10348444, 'VLPO': 15887419, 'IMD': 16748447, 'BLA_p': 10348445, 'rust': 13421725,
    'MOB': 8570795, 'PSV': 16758662, 'PST': 15886139, 'NLOT_1': 9823434, 'RSPv_6b': 1746323, 'COApm_2': 6416565,
    'mcp/vn/rust/ii/py/ml': 13421714, 'NLOT_2': 9823433, 'BST_pr': 11780062, 'VISC_1': 1158531, 'CA3_sp': 8311372,
    'CA3_sr': 8311374, 'LG_v': 16744351, 'CA3_so': 8311371, 'MEA_pv': 8437981, 'PBm_m': 16756614, 'VISam_1': 558476,
    'VISam_4': 558474, 'VISam_5': 558473, 'PIR_1': 6998970, 'ENTmv_1': 3323685, 'ENTmv_2': 3323684,
    'ENTmv_3': 3323683, 'AIv_6b': 2201442, 'AIv_6a': 2201443, 'AUDv_2/3': 103320, 'ILA_5': 5878623, 'pm': 13421748,
    'TEa_2/3': 1421490, 'MD_c': 16751777, 'CM': 16751007, 'CL': 16746399, 'MD_m': 16751776, 'rust/ii': 13421705,
    'DP_1': 10803876, 'CP': 10016505, 'CU': 16746450, 'AUDPo_2/3': 103576, 'VII': 16753106, 'SPVO_mdmv': 16749013,
    'tb/sctv/sptV/rust/vlln': 13421687, 'RH': 16750495, 'RSPv_6a': 1746324, 'MD_I': 16751775, 'border9': 10146493,
    'border8': 16751565, 'MPN_m': 15888190, 'MPN_l': 15888188, 'RSPd_2/3': 1746583, 'SPVO_mdmd': 16749014,
    'SPVO_cdm': 16749012, 'RSPd_6a': 1746581, 'NDB': 9873363, 'RSPd_6b': 1746580, 'MPN_c': 15888189,
    'border7': 16751496, 'VISam_6a': 558472, 'mlf/ml': 13421675, 'SSp_tr_6a': 1601888, 'arbc/icp': 13421686,
    'SSp_tr_6b': 1601887, 'central_canal': 11184816, 'PRM_mo': 16773521, 'PONS': 16754310, 'FL_gr': 16775826,
    'SSp-un_6b': 1603423, 'SN_r': 16683263, 'SSp-un_6a': 1603424, 'RCH': 15883579, 'ORBvl_2/3': 2394461,
    'SCs_sg': 16680190, 'VISC_2/3': 1158530, 'MOB_opl': 8570799, 'DR': 16678399, 'dhc': 13421710, 'PPN': 16685567,
    'BST_OV': 11780067, 'ENTm_2b': 3323428, 'TEa_4': 1421489, 'ENTm_2a': 3323429, 'V4': 11184814, 'islm': 8441082,
    'PPT': 16685055, 'CENT2_gr': 16775570, 'PPY': 16749266, 'mcp/vn': 13421708, 'BLA_v': 10348446,
    'VISal_6b': 557959, 'VISal_6a': 557960, 'IP': 16776593, 'VL': 11184809, 'PTLp_2/3': 40875, 'IV': 16678655,
    'll': 13421709, 'IRN': 16752082, 'IA': 8438497, 'AIv_2/3': 2201445, 'IG': 8310859, 'IF': 16679935,
    'LPO': 15885371, 'SSp-un_5': 1603425, 'SSp-un_4': 1603426, 'GU_6b': 40048, 'SSp-un_1': 1603428,
    'UVU_gr': 16773010, 'TM_v': 15886652, 'GU_1': 40053, 'SSp_bfd_2/3': 1602147, 'ARH': 15881787,
    'ACAd_6b': 4236897, 'ACAd_6a': 4236898, 'STN': 15885883, 'TTv_1': 6475679, 'BA': 8439009, 'COApm_1': 6416566,
    'PARN': 16751570, 'TTd_3': 6475933, 'MOp_6b': 2071893, 'MOp_6a': 2071894, 'SSp_m_6b': 1602655,
    'COApm_3': 6416564, 'bsc/opt/cpd/mp': 13421740, 'CEA_l': 8438238, 'rust/ml': 13421738, 'ECT_2/3': 892816,
    'tb/sctv/sptV/rust/vVllln': 13421684, 'SSp_m_4': 1602658, 'SSp_m_5': 1602657, 'SSp_m_1': 1602660,
    'SBPV': 15882811, 'cpd/opt': 13421763, 'DG_po': 8311117, 'CEA_c': 8438240, 'CEA_m': 8438239, 'VISpm_6a': 557704,
    'VISpm_6b': 557703, 'ENTl_2a': 3323940, 'ENTl_2b': 3323939, 'opt': 13421793, 'VISpl_6b': 557191,
    'VISpl_6a': 557192, 'VISam_6b': 558471, 'BST_fu': 11780065, 'DMH_v': 15881021, 'amc': 13224393,
    'vtd/rust': 13421729, 'bic': 13421728, 'DMH_p': 15881020, 'MEPO': 15884859, 'SSp_n_6b': 1602399,
    'DMH_a': 15881019, 'SSp_n_6a': 1602400, 'MH': 16748191, 'CLA': 9099911, 'AUDPo_6a': 103573, 'ENTl_6b': 3323932,
    'py/tb/sctv/sptV/rust/Vlln': 13421690, 'SSp_1': 1605732, 'moV': 13421703, 'SSp_4': 1605730, 'SSp_5': 1605729,
    'arb/cbc': 13421679, 'RPO': 16757638, 'ECT_6a': 892814, 'OV': 15884603, 'LHA': 15884347, 'OP': 16684799,
    'NLL_h': 16759176, 'HY': 15889211, 'MDRN_d': 16755667, 'ccg/cing/fi/alv/df/int/ec/amc': 13421756,
    'ACAd_1': 4236902, 'ACAd_5': 4236900, 'ACAd_6': 4236899, 'SPF_m': 16745119, 'AOB_mi': 10350800,
    'PYR_gr': 16772498, 'MDRN_v': 16755666, 'NLL_v': 16759174, 'VISl_2/3': 557451, 'PV_a': 15881531,
    'SPV_i': 16747730, 'AUDd_6a': 102805, 'AUDd_6b': 102804, 'PV_i': 15881532, 'AMB': 16754644, 'SPV_c': 16747731,
    'SOC_l': 16757894, 'PV_p': 15881534, 'VM': 16747423, 'FN': 16777105, 'ICB': 16756434, 'PTLp_1': 40876,
    'icp': 13421680, 'PTLp_5': 40873, 'PTLp_4': 40874, 'hsc': 13421752, 'fp/dhc/ec': 13421731, 'TRN': 16759686,
    'MG_v': 16743583, 'PBG': 16679423, 'MG_m': 16743584, 'CS_m': 16760198, 'CS_l': 16760199, 'ACB': 8446456,
    'MG_d': 16743585, 'AVPV': 15887931, 'EP_d': 10546845, 'MPN': 15888187, 'MPO': 15885115, 'CA1_sp': 8311884,
    'dhc/ec': 13421713, 'dscp/scp': 13421712, 'MPT': 16685311, 'CA1_so': 8311883, 'act': 13421783, 'PIR_3': 6998968,
    'BST_tr': 11780059, 'PL_6a': 3123276, 'PL_6b': 3123275, 'py': 13421682, 'RSPagl_6b': 1746836,
    'RSPagl_6a': 1746837, 'cpd/opt/st': 13421757, 'FOTU_mo': 16772241, 'SUV': 16750802, 'mcp': 13421733,
    'SUT': 16757126, 'PM_d': 15880507, 'SSp_6a': 1605728, 'AUDPo_1': 103577, 'SSp_6b': 1605727, 'NI': 16754566,
    'pc': 13421753, 'SSp_ul_6a': 1602912, 'SSs_1': 1605476, 'NB': 16681471, 'NC': 15879483, 'ND': 16676863,
    'ACAv_5': 4236644, 'AUDp_6a': 103061, 'AUDp_6b': 103060, 'lot': 13421774, 'NR': 16746962, 'SLC': 16757382,
    'DP_5': 10803874, 'SSp-un_2/3': 1603427, 'ADP': 15888699, 'SSp_ul_6b': 1602911, 'SPF_p': 16745120,
    'DEC_gr': 16772754, 'NLL_d': 16759175, 'PBm_me': 16756615, 'AUDp_5': 103062, 'CUN': 16678143,
    'COPY_mo': 16773265, 'AUDp_1': 103065, 'cic': 13421696, 'PVH_pmm': 15881283, 'PVH_pml': 15881281,
    'AUDv_5': 103318, 'AUDv_4': 103319, 'mtv': 13421695, 'ADH_p': 15882555, 'mtt': 13421768, 'MEV': 16677631,
    'ccg/cing/fi/alv/dhc/int/ec': 13421751, 'sctv/sptV/rust': 13421678, 'mtg': 13421674, 'vhc': 13421788,
    'COAa_1': 6416311, 'AIv_1': 2201446, 'SPVO_vl': 16749011, 'ccg/cing/fi/alv/df/ec/amc': 13421766,
    'AIv_5': 2201444, 'int': 13421781, 'RSPd_1': 1746584, 'ENTmv_5/6': 3323682, 'SSp_ul_2/3': 1602915,
    'RSPd_5': 1746582, 'SPVO_rdm': 16749010, 'SPIV': 16747986, 'AUDd_2/3': 102808, 'SUBd_m': 4961607,
    'SCm_ig': 16680442, 'GU_6a': 40049, 'A13': 15882299, 'scp/tsp/dtd': 13421724, 'BST_v': 11780058, 'TU': 15882043,
    'GU_5': 40050, 'GU_4': 40051, 'SSp_m_6a': 1602656, 'SCm_iw': 16680446, 'AVP': 15887675,
    'ccg/cing/fi/vhc/df/ec/amc': 13421767, 'SSp_n_2/3': 1602403, 'SGN': 16752287, 'fp/dhc/alv/ec': 13421743,
    'BST_d': 11780056, 'ACAv_2/3': 4236645, 'NOD_gr': 16773778, 'py/tb/ml/sctv/sptV/rust/vn': 13421697,
    'VISl_6a': 557448, 'VISl_6b': 557447, 'AQ': 11184813, 'AP': 16756178, 'PVH_dp': 15881285, 'AT': 16681215,
    'AV': 16748959, 'SSs_5': 1605473, 'SSs_4': 1605474, 'UVU_mo': 16773009, 'mcp/sptV/tb/vn/rust': 13421698,
    'SCH': 15883323, 'MOp_1': 2071898, 'MOp_5': 2071896, 'MOp_6': 2071895, 'SubG': 16752031, 'cpd': 13421745,
    'VISam_2/3': 558475, 'SUBd_sr': 4961608, 'SUBd_sp': 4961609
}

INDEX2ROI = dict((v, k) for k, v in ROI2INDEX.items())

GRAY_MATTER_INDICES = set([ROI2INDEX[roi] for roi in ROI2INDEX if roi not in NON_GRAYMATTER_ROIS])


class ROIInfo:
    def __init__(self, rgb_codec):
        assert isinstance(rgb_codec, TranslateColors), \
            "TranslateColors object expected"

        self._associated_atlas = rgb_codec.associated_atlas
        self.rgb_codec = rgb_codec
        if self._associated_atlas == TranslateColors.DEFAULT_ASSOCIATED_ATLAS:
            self.index2roi = deepcopy(INDEX2ROI)
            self.roi2index = deepcopy(ROI2INDEX)
            self.gray_matter_indices = deepcopy(GRAY_MATTER_INDICES)
        else:
            self.index2roi = {}
            self.roi2index = {}
            self.gray_matter_indices = set()
            self.custom_atlas_init()

    def __eq__(self, other):
        assert isinstance(other, ROIInfo), \
            "operator == between ROIInfo and another type is not defined"
        return self._associated_atlas == other._associated_atlas

    def custom_atlas_init(self):
        custom_index2roi_ = map(ROIInfo.convert_lookup, self.rgb_codec.LOOKUP.items())
        custom_index2roi = dict(custom_index2roi_)
        for k, v in custom_index2roi.items():
            self.index2roi[k] = v
            self.roi2index[v] = k
            if k in GRAY_MATTER_INDICES:
                self.gray_matter_indices.add(k)

    @staticmethod
    def convert_lookup(lookup_item):
        """
        convert a tuple in format of TranslateColors.
        LOOKUP key value pair to [rgb_index, roi]
        :param lookup_item:
        :return: [rgb_index, roi]
        """
        rgb_code = lookup_item[0]
        roi = lookup_item[1]
        index = TranslateColors.colorstring_to_index(rgb_code)
        return [index, roi]


