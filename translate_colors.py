import numpy as np
import warnings
from copy import deepcopy
import string
import sys


class UnknownCustomAtlasError(ValueError):
    def __init__(self, custom_atlas_name):
        self._custom_atlas_name = custom_atlas_name
        self._custom_atlas_candidates = UnknownCustomAtlasError.get_candidates()
        self.message = "unknown custom atlas provided: {0}. Candidate custom atlas are {1}".\
                       format(self._custom_atlas_name, self._custom_atlas_candidates)

    @staticmethod
    def get_candidates():
        candidates = ""
        for candidate in TranslateColors.CUSTOM_ATLAS_LOOKUP.keys():
            candidates += candidate + ", "
        return candidates[:-2]


class TranslateColors:
    """
    TranslateColors.LOOKUP defaults to ARA regular atlas rgb codes.
    application interested in custom atlases needs to call
    TranslateColors.custom_atlas_init(custom_atlas=xxx) once
    before querying look up table for appropriate atlas binding
    Note: color codes in 'R:G:B' order
    """
    LOOKUP = {
        '0:156:112': 'GU_6b', '0:156:113': 'GU_6a', '0:156:114': 'GU_5',
        '0:156:115': 'GU_4', '0:156:116': 'GU_2/3', '0:156:117': 'GU_1',
        '0:159:167': 'PTLp_6b', '0:159:168': 'PTLp_6a', '0:159:169': 'PTLp_5',
        '0:159:170': 'PTLp_4', '0:159:171': 'PTLp_2/3', '0:159:172': 'PTLp_1',
        '1:145:148': 'AUDd_6b', '1:145:149': 'AUDd_6a', '1:145:150': 'AUDd_5',
        '1:145:151': 'AUDd_4', '1:145:152': 'AUDd_2/3', '1:145:153': 'AUDd_1',
        '1:146:148': 'AUDp_6b', '1:146:149': 'AUDp_6a', '1:146:150': 'AUDp_5',
        '1:146:151': 'AUDp_4', '1:146:152': 'AUDp_2/3', '1:146:153': 'AUDp_1',
        '1:147:148': 'AUDv_6b', '1:147:149': 'AUDv_6a', '1:147:150': 'AUDv_5',
        '1:147:151': 'AUDv_4', '1:147:152': 'AUDv_2/3', '1:147:153': 'AUDv_1',
        '1:148:148': 'AUDpo_6b', '1:148:149': 'AUDPo_6a', '1:148:150': 'AUDPo_5',
        '1:148:151': 'AUDPo_4', '1:148:152': 'AUDPo_2/3', '1:148:153': 'AUDPo_1',
        '8:128:135': 'VISpl_6b', '8:128:136': 'VISpl_6a', '8:128:137': 'VISpl_5',
        '8:128:138': 'VISpl_4', '8:128:139': 'VISpl_2/3', '8:128:140': 'VISpl_1',
        '8:129:135': 'VISl_6b', '8:129:136': 'VISl_6a', '8:129:137': 'VISl_5',
        '8:129:138': 'VISl_4', '8:129:139': 'VISl_2/3', '8:129:140': 'VISl_1',
        '8:130:135': 'VISpm_6b', '8:130:136': 'VISpm_6a', '8:130:137': 'VISpm_5',
        '8:130:138': 'VISpm_4', '8:130:139': 'VISpm_2/3', '8:130:140': 'VISpm_1',
        '8:131:135': 'VISal_6b', '8:131:136': 'VISal_6a', '8:131:137': 'VISal_5',
        '8:131:138': 'VISal_4', '8:131:139': 'VISal_2/3', '8:131:140': 'VISal_1',
        '8:132:135': 'VISp_6b', '8:132:136': 'VISp_6a', '8:132:137': 'VISp_5',
        '8:132:138': 'VISp_4', '8:132:139': 'VISp_2/3', '8:132:140': 'VISp_1',
        '8:133:135': 'VISam_6b', '8:133:136': 'VISam_6a', '8:133:137': 'VISam_5',
        '8:133:138': 'VISam_4', '8:133:139': 'VISam_2/3', '8:133:140': 'VISam_1',
        '13:159:141': 'ECT_6b', '13:159:142': 'ECT_6a', '13:159:143': 'ECT_5',
        '13:159:144': 'ECT_2/3', '13:159:145': 'ECT_1', '14:150:128': 'PERI_6b',
        '14:150:129': 'PERI_6a', '14:150:130': 'PERI_5', '14:150:131': 'PERI_2/3',
        '14:150:132': 'PERI_1', '17:173:126': 'VISC_6b', '17:173:127': 'VISC_6a',
        '17:173:128': 'VISC_5', '17:173:129': 'VISC_4', '17:173:130': 'VISC_2/3',
        '17:173:131': 'VISC_1', '21:176:174': 'TEa_6b', '21:176:175': 'TEa_6a',
        '21:176:176': 'TEa_5', '21:176:177': 'TEa_4', '21:176:178': 'TEa_2/3',
        '21:176:179': 'TEa_1', '24:113:95': 'SSp_tr_6b', '24:113:96': 'SSp_tr_6a',
        '24:113:97': 'SSp_tr_5', '24:113:98': 'SSp_tr_4', '24:113:99': 'SSp_tr_2/3',
        '24:113:100': 'SSp_tr_1', '24:114:95': 'SSp_bfd_6b', '24:114:96': 'SSp_bfd_6a',
        '24:114:97': 'SSp_bfd_5', '24:114:98': 'SSp_bfd_4', '24:114:99': 'SSp_bfd_2/3',
        '24:114:100': 'SSp_bfd_1', '24:115:95': 'SSp_n_6b', '24:115:96': 'SSp_n_6a',
        '24:115:97': 'SSp_n_5', '24:115:98': 'SSp_n_4', '24:115:99': 'SSp_n_2/3',
        '24:115:100': 'SSp_n_1', '24:116:95': 'SSp_m_6b', '24:116:96': 'SSp_m_6a',
        '24:116:97': 'SSp_m_5', '24:116:98': 'SSp_m_4', '24:116:99': 'SSp_m_2/3',
        '24:116:100': 'SSp_m_1', '24:117:95': 'SSp_ul_6b', '24:117:96': 'SSp_ul_6a',
        '24:117:97': 'SSp_ul_5', '24:117:98': 'SSp_ul_4', '24:117:99': 'SSp_ul_2/3',
        '24:117:100': 'SSp_ul_1', '24:118:95': 'SSp_ll_6b', '24:118:96': 'SSp_ll_6a',
        '24:118:97': 'SSp_ll_5', '24:118:98': 'SSp_ll_4', '24:118:99': 'SSp_ll_2/3',
        '24:118:100': 'SSp_ll_1', '24:119:95': 'SSp-un_6b', '24:119:96': 'SSp-un_6a',
        '24:119:97': 'SSp-un_5', '24:119:98': 'SSp-un_4', '24:119:99': 'SSp-un_2/3',
        '24:119:100': 'SSp-un_1', '24:127:95': 'SSs_6b', '24:127:96': 'SSs_6a',
        '24:127:97': 'SSs_5', '24:127:98': 'SSs_4', '24:127:99': 'SSs_2/3',
        '24:127:100': 'SSs_1', '24:128:95': 'SSp_6b', '24:128:96': 'SSp_6a',
        '24:128:97': 'SSp_5', '24:128:98': 'SSp_4', '24:128:99': 'SSp_2/3',
        '24:128:100': 'SSp_1', '26:165:147': 'RSPv_6b', '26:165:148': 'RSPv_6a',
        '26:165:149': 'RSPv_5', '26:165:150': 'RSPv_2/3', '26:165:151': 'RSPv_2',
        '26:165:152': 'RSPv_1', '26:166:148': 'RSPd_6b', '26:166:149': 'RSPd_6a',
        '26:166:150': 'RSPd_5', '26:166:151': 'RSPd_2/3', '26:166:152': 'RSPd_1',
        '26:167:148': 'RSPagl_6b', '26:167:149': 'RSPagl_6a', '26:167:150': 'RSPagl_5',
        '26:167:151': 'RSPagl_2/3', '26:167:152': 'RSPagl_1', '31:156:85': 'MOs_6b',
        '31:156:86': 'MOs_6a', '31:156:87': 'MOs_6', '31:156:88': 'MOs_5',
        '31:156:89': 'MOs_2/3', '31:156:90': 'MOs_1', '31:157:85': 'MOp_6b',
        '31:157:86': 'MOp_6a', '31:157:87': 'MOp_6', '31:157:88': 'MOp_5',
        '31:157:89': 'MOp_2/3', '31:157:90': 'MOp_1', '33:150:98': 'AIp_6b',
        '33:150:99': 'AIp_6a', '33:150:100': 'AIp_5', '33:150:101': 'AIp_2/3',
        '33:150:102': 'AIp_1', '33:151:98': 'AIv_6b', '33:151:99': 'AIv_6a',
        '33:151:100': 'AIv_5', '33:151:101': 'AIv_2/3', '33:151:102': 'AIv_1',
        '33:152:97': 'AId_6b', '33:152:98': 'AId_6a', '33:152:99': 'AId_6',
        '33:152:100': 'AId_5', '33:152:101': 'AId_2/3', '33:152:102': 'AId_1',
        '36:136:90': 'ORBm_6', '36:136:91': 'ORBm_6a', '36:136:92': 'ORBm_5',
        '36:136:93': 'ORBm_2/3', '36:136:94': 'ORBm_3', '36:136:95': 'ORBm_2',
        '36:136:96': 'ORBm_1', '36:137:89': 'ORBvl_6b', '36:137:90': 'ORBvl_6',
        '36:137:91': 'ORBvl_6a', '36:137:92': 'ORBvl_5', '36:137:93': 'ORBvl_2/3',
        '36:137:94': 'ORBvl_1', '36:138:89': 'ORBl_6b', '36:138:90': 'ORBl_6',
        '36:138:91': 'ORBl_6a', '36:138:92': 'ORBl_5', '36:138:93': 'ORBl_2/3',
        '36:138:94': 'ORBl_1', '38:143:68': 'FRP_2/3', '38:143:69': 'FRP_1',
        '47:168:74': 'PL_6', '47:168:75': 'PL_6b', '47:168:76': 'PL_6a',
        '47:168:77': 'PL_5', '47:168:78': 'PL_3', '47:168:79': 'PL_2/3',
        '47:168:80': 'PL_2', '47:168:81': 'PL_1', '50:182:32': 'ENTm_6',
        '50:182:33': 'ENTm_5', '50:182:34': 'ENTm_4', '50:182:35': 'ENTm_3',
        '50:182:36': 'ENTm_2b', '50:182:37': 'ENTm_2a', '50:182:38': 'ENTm_2',
        '50:182:39': 'ENTm_1', '50:183:34': 'ENTmv_5/6', '50:183:35': 'ENTmv_3',
        '50:183:36': 'ENTmv_2', '50:183:37': 'ENTmv_1', '50:184:27': 'ENTl_6',
        '50:184:28': 'ENTl_6b', '50:184:29': 'ENTl_6a', '50:184:30': 'ENTl_5',
        '50:184:31': 'ENTl_4/5', '50:184:32': 'ENTl_4', '50:184:33': 'ENTl_2/3',
        '50:184:34': 'ENTl_3', '50:184:35': 'ENTl_2b', '50:184:36': 'ENTl_2a',
        '50:184:37': 'ENTl_2', '50:184:38': 'ENTl_1', '64:165:98': 'ACAv_6b',
        '64:165:99': 'ACAv_6a', '64:165:100': 'ACAv_5', '64:165:101': 'ACAv_2/3',
        '64:165:102': 'ACAv_1', '64:166:97': 'ACAd_6b', '64:166:98': 'ACAd_6a',
        '64:166:99': 'ACAd_6', '64:166:100': 'ACAd_5', '64:166:101': 'ACAd_2/3',
        '64:166:102': 'ACAd_1', '72:200:60': 'POST_3', '72:200:61': 'POST_2',
        '72:200:62': 'POST_1', '75:181:71': 'SUBd_m', '75:181:72': 'SUBd_sr',
        '75:181:73': 'SUBd_sp', '75:182:71': 'SUBv_m', '75:182:72': 'SUBv_sr',
        '75:182:73': 'SUBv_sp', '84:191:143': 'AON', '84:191:144': 'AON_e',
        '84:191:145': 'AON_l', '84:191:146': 'AON_d', '84:191:147': 'AON_pv',
        '84:191:148': 'AON_m', '84:191:149': 'AON_1', '89:179:93': 'ILA_6b',
        '89:179:94': 'ILA_6a', '89:179:95': 'ILA_5', '89:179:96': 'ILA_3',
        '89:179:97': 'ILA_2/3', '89:179:98': 'ILA_2', '89:179:99': 'ILA_1',
        '89:185:71': 'PRE_3', '89:185:72': 'PRE_2', '89:185:73': 'PRE_1',
        '89:218:171': 'PAA_3', '89:218:172': 'PAA_2', '89:218:173': 'PAA_1',
        '97:230:180': 'COApl_3', '97:230:181': 'COApl_2', '97:230:182': 'COApl_1',
        '97:231:182': 'COAa_2', '97:231:183': 'COAa_1', '97:232:180': 'COApm_3',
        '97:232:181': 'COApm_2', '97:232:182': 'COApm_1', '98:207:157': 'TTv_3',
        '98:207:158': 'TTv_2', '98:207:159': 'TTv_1', '98:208:156': 'TTd_4',
        '98:208:157': 'TTd_3', '98:208:158': 'TTd_2', '98:208:159': 'TTd_1',
        '106:203:184': 'PIR_3', '106:203:185': 'PIR_2', '106:203:186': 'PIR_1',
        '114:213:103': 'PAR_3', '114:213:104': 'PAR_2', '114:213:105': 'PAR_1',
        '126:208:75': 'IG', '126:209:75': 'DG_mo', '126:209:76': 'DG_sg',
        '126:209:77': 'DG_po', '126:210:75': 'CA3_so', '126:210:76': 'CA3_sp',
        '126:210:77': 'CA3_slu', '126:210:78': 'CA3_sr', '126:210:79': 'CA3_slm',
        '126:211:75': 'CA2_so', '126:211:76': 'CA2_sp', '126:211:77': 'CA2_sr',
        '126:211:78': 'CA2_slm', '126:212:75': 'CA1_so', '126:212:76': 'CA1_sp',
        '126:212:77': 'CA1_sr', '126:212:78': 'CA1_slm', '126:213:75': 'FC',
        '128:192:215': 'sAMY', '128:192:216': 'MEA_pd_a', '128:192:217': 'MEA_pd_b',
        '128:192:218': 'MEA_pd_c', '128:192:219': 'MEA_av', '128:192:220': 'MEA_ad',
        '128:192:221': 'MEA_pv', '128:192:226': 'BORDER10', '128:193:222': 'CEA_l',
        '128:193:223': 'CEA_m', '128:193:224': 'CEA_c', '128:194:225': 'IA',
        '128:195:225': 'AAA', '128:196:225': 'BA', '128:204:249': 'isl',
        '128:204:250': 'islm', '128:205:246': 'OT_3', '128:205:247': 'OT_2',
        '128:205:248': 'OT_1', '128:206:248': 'FS', '128:225:248': 'ACB',
        '130:199:171': 'MOB', '130:199:172': 'MOB_gr', '130:199:173': 'MOB_mi',
        '130:199:174': 'MOB_gl', '130:199:175': 'MOB_opl', '130:199:176': 'MOB_ipl',
        '132:234:128': 'BMA_p', '132:234:129': 'BMA_a', '133:153:203': 'Gpi',
        '133:153:204': 'Gpe', '138:218:135': 'CLA', '144:203:236': 'SH',
        '144:203:237': 'SI', '144:203:238': 'SF', '144:204:237': 'LS_r',
        '144:204:238': 'LS_c', '144:204:239': 'LS_v', '149:228:200': 'NLOT_3',
        '149:228:201': 'NLOT_2', '149:228:202': 'NLOT_1', '150:166:210': 'TRS',
        '150:167:211': 'NDB', '150:168:211': 'MS', '151:236:147': 'PA',
        '152:214:249': 'CP', '154:210:189': 'border9', '157:231:156': 'BLA_a',
        '157:231:157': 'BLA_p', '157:231:158': 'BLA_v', '157:232:156': 'LA',
        '157:240:207': 'AOB_gr', '157:240:208': 'AOB_mi', '157:240:209': 'AOB_gl',
        '157:240:210': 'AOB', '160:238:156': 'Ep_v', '160:238:157': 'EP_d',
        '162:177:216': 'MA', '164:218:161': 'DP_6a', '164:218:162': 'DP_5',
        '164:218:163': 'DP_2/3', '164:218:164': 'DP_1', '168:236:209': 'TR_3',
        '168:236:210': 'TR_2', '168:236:211': 'TR_1', '170:170:169': 'VL',
        '170:170:170': 'rc/sez', '170:170:171': 'V3', '170:170:172': 'SFO/V3',
        '170:170:173': 'AQ', '170:170:174': 'V4', '170:170:175': 'V4r',
        '170:170:176': 'central_canal', '176:255:184': 'BORDER1',
        '179:191:214': 'BST_dm', '179:191:215': 'BST_rh', '179:191:216': 'BST_d',
        '179:191:217': 'BST_mg', '179:191:218': 'BST_v', '179:191:219': 'BST_tr',
        '179:191:220': 'BST_if', '179:191:221': 'BST_se', '179:191:222': 'BST_pr',
        '179:191:223': 'BST_AL', '179:191:224': 'BST_AM', '179:191:225': 'BST_fu',
        '179:191:226': 'BST_ju', '179:191:227': 'BST_OV', '179:192:227': 'BST_BAC',
        '191:218:227': 'BORDER0', '201:201:201': 'amc', '204:204:106': 'mtg',
        '204:204:107': 'mlf/ml', '204:204:108': 'sctv/sptV/rust/icp',
        '204:204:109': 'ts', '204:204:110': 'sctv/sptV/rust', '204:204:111': 'arb/cbc',
        '204:204:112': 'icp', '204:204:113': 'tb/sctv/sptV/rust/vVlln/icp/arb',
        '204:204:114': 'py', '204:204:115': 'gVLLn',
        '204:204:116': 'tb/sctv/sptV/rust/vVllln', '204:204:117': 'VIIIn',
        '204:204:118': 'arbc/icp', '204:204:119': 'tb/sctv/sptV/rust/vlln',
        '204:204:120': 'ml/py', '204:204:121': 'Vlln',
        '204:204:122': 'py/tb/sctv/sptV/rust/Vlln', '204:204:123': 'arb',
        '204:204:124': 'py/tb/ml/sctv/sptV/vn/grf', '204:204:125': 'sctv',
        '204:204:126': 'sctv/ii', '204:204:127': 'mtv', '204:204:128': 'cic',
        '204:204:129': 'py/tb/ml/sctv/sptV/rust/vn',
        '204:204:130': 'mcp/sptV/tb/vn/rust',
        '204:204:131': 'sctv/mcp/sptV/tb/vn/rust', '204:204:132': 'sctv/ml/tb/py',
        '204:204:133': 'scp', '204:204:134': 'sctv/rust/ii', '204:204:135': 'moV',
        '204:204:136': 'sptV/tb/vn/mcp', '204:204:137': 'rust/ii',
        '204:204:138': 'py/tb/ml', '204:204:139': 'rust/ii/tb/ml/py',
        '204:204:140': 'mcp/vn', '204:204:141': 'll', '204:204:142': 'dhc',
        '204:204:143': 'mcp/tb/ml/py/vn/rust/ii', '204:204:144': 'dscp/scp',
        '204:204:145': 'dhc/ec', '204:204:146': 'mcp/vn/rust/ii/py/ml',
        '204:204:147': 'mcp/ii', '204:204:148': 'mcp/cst/ml/ii',
        '204:204:149': 'dhc/ec/alv', '204:204:150': 'dscp', '204:204:151': 'cst/ml',
        '204:204:152': 'mcp/cpd/rust/ii', '204:204:153': 'scp/dtd/mlf',
        '204:204:154': 'tsp', '204:204:155': 'mcp/cst/ml/cpd/rust/bic',
        '204:204:156': 'scp/tsp/dtd', '204:204:157': 'rust',
        '204:204:158': 'mcp/cst/ml/cpd', '204:204:159': 'rust/scp/vtd/dtd/tsp',
        '204:204:160': 'bic', '204:204:161': 'vtd/rust', '204:204:162': 'alv',
        '204:204:163': 'fp/dhc/ec', '204:204:164': 'vtd', '204:204:165': 'mcp',
        '204:204:166': 'dhc/alv', '204:204:167': 'fp/ec', '204:204:168': 'mlf',
        '204:204:169': 'fr/mp', '204:204:170': 'rust/ml', '204:204:171': 'bsc/opt/cpd',
        '204:204:172': 'bsc/opt/cpd/mp', '204:204:174': 'csc',
        '204:204:175': 'fp/dhc/alv/ec', '204:204:176': 'mp', '204:204:177': 'cpd',
        '204:204:178': 'bsc/opt', '204:204:179': 'ccs/cing/alv/dhc/ec/alv/st',
        '204:204:180': 'pm', '204:204:181': 'smd', '204:204:182': 'bsc/opt/cpt',
        '204:204:183': 'ccg/cing/fi/alv/dhc/int/ec', '204:204:184': 'hsc',
        '204:204:185': 'pc', '204:204:186': 'ccg/cing/fi/alv/df/dhc/int/ec/amc',
        '204:204:187': 'bsc', '204:204:188': 'ccg/cing/fi/alv/df/int/ec/amc',
        '204:204:189': 'cpd/opt/st', '204:204:190': 'ml/em', '204:204:191': 'hbc',
        '204:204:192': 'ccg/cing/fi/alv/df/int/st/cpd/opt/ec/amc',
        '204:204:193': 'ml', '204:204:194': 'im', '204:204:195': 'cpd/opt',
        '204:204:196': 'fr', '204:204:197': 'em',
        '204:204:198': 'ccg/cing/fi/alv/df/ec/amc',
        '204:204:199': 'ccg/cing/fi/vhc/df/ec/amc', '204:204:200': 'mtt',
        '204:204:201': 'ccg/cing/fi/vhc/df/ec', '204:204:202': 'ccg/cing/df',
        '204:204:203': 'fi/vhc', '204:204:204': 'onl', '204:204:205': 'aco/lotd',
        '204:204:206': 'lot', '204:204:207': 'aco', '204:204:208': 'von',
        '204:204:209': 'fa', '204:204:210': 'fa/cing', '204:204:211': 'ccg/cing',
        '204:204:212': 'och', '204:204:213': 'int', '204:204:214': 'fx',
        '204:204:215': 'act', '204:204:216': 'aco/act', '204:204:217': 'st',
        '204:204:218': 'ect', '204:204:219': 'fi', '204:204:220': 'vhc',
        '204:204:221': 'ccg/cing/fi/vhc/df', '204:204:222': 'sm',
        '204:204:223': 'ccg/fi/cing', '204:204:224': 'df', '204:204:225': 'opt',
        '230:68:56': 'BORDER3', '240:240:128': 'BORDER4', '242:77:59': 'NC',
        '242:78:59': 'PVR_pd', '242:79:59': 'ME', '242:80:59': 'SUM_m',
        '242:80:60': 'SUM_l', '242:81:59': 'PM_d', '242:81:60': 'PM_v',
        '242:82:59': 'VMH_vl', '242:82:60': 'VMH_c', '242:82:61': 'VMH_dm',
        '242:82:62': 'VMH_a', '242:83:59': 'DMH_a', '242:83:60': 'DMH_p',
        '242:83:61': 'DMH_v', '242:84:59': 'PVH_f', '242:84:60': 'PVH_mpv',
        '242:84:61': 'PVH_pv', '242:84:62': 'PVH_ap', '242:84:63': 'PVH_mpd',
        '242:84:64': 'PVH_mm', '242:84:65': 'PVH_pml', '242:84:66': 'PVH_a',
        '242:84:67': 'PVH_pmm', '242:84:68': 'PVH_lp', '242:84:69': 'PVH_dp',
        '242:85:59': 'PV_a', '242:85:60': 'PV_i', '242:85:61': 'PV_po',
        '242:85:62': 'PV_p', '242:86:59': 'ARH', '242:87:59': 'TU', '242:88:59': 'A13',
        '242:89:59': 'ADH_p', '242:90:59': 'SBPV', '242:91:59': 'SO',
        '242:92:59': 'SCH', '242:93:59': 'RCH', '242:94:59': 'AHN_a',
        '242:94:60': 'AHN_c', '242:94:61': 'AHN_p', '242:95:59': 'ZI',
        '242:95:60': 'ZI_A13', '242:95:61': 'ZI_FF', '242:96:59': 'LHA',
        '242:97:59': 'OV', '242:98:59': 'MEPO', '242:99:59': 'MPO', '242:100:59': 'LPO',
        '242:101:59': 'PH', '242:102:59': 'STN', '242:103:59': 'PST',
        '242:104:59': 'PSTN', '242:105:59': 'TM_d', '242:105:60': 'TM_v',
        '242:106:59': 'LM', '242:107:59': 'MM', '242:107:60': 'MM_me',
        '242:108:59': 'VLPO', '242:109:59': 'AVP', '242:110:59': 'AVPV',
        '242:111:59': 'MPN', '242:111:60': 'MPN_l', '242:111:61': 'MPN_c',
        '242:111:62': 'MPN_m', '242:112:59': 'PS', '242:113:59': 'ADP',
        '242:114:59': 'SFO', '242:115:59': 'HY', '254:118:255': 'MB',
        '254:119:255': 'ND', '254:120:255': 'NOT', '254:121:255': 'Scig_b',
        '254:122:255': 'MEV', '254:123:255': 'VTN', '254:124:255': 'CUN',
        '254:125:255': 'DR', '254:126:255': 'IV', '254:127:253': 'IC_e',
        '254:127:254': 'IC_d', '254:127:255': 'IC_c', '254:128:255': 'SAG',
        '254:129:255': 'PBG', '254:130:255': 'LT', '254:131:255': 'IF',
        '254:132:253': 'SCs_zo', '254:132:254': 'SCs_sg', '254:132:255': 'SCs_op',
        '254:133:249': 'SCm_dw', '254:133:250': 'SCm_ig', '254:133:251': 'SCM_ig-c',
        '254:133:252': 'SCM_ig-b', '254:133:253': 'SCM_ig-a', '254:133:254': 'SCm_iw',
        '254:133:255': 'SCm_dg', '254:134:255': 'IPN', '254:135:255': 'INC',
        '254:136:255': 'AT', '254:137:255': 'NB', '254:138:255': 'CLI',
        '254:139:255': 'III', '254:140:255': 'EW', '254:141:255': 'RL',
        '254:142:255': 'RN', '254:143:255': 'RR', '254:144:254': 'SN_c',
        '254:144:255': 'SN_r', '254:145:255': 'VTA', '254:146:255': 'MRN',
        '254:147:255': 'PAG', '254:148:255': 'NPC', '254:149:255': 'APN',
        '254:150:255': 'OP', '254:151:255': 'PPT', '254:152:255': 'MPT',
        '254:153:255': 'PPN', '254:154:255': 'PRC', '255:100:255': 'BORDER5',
        '255:112:128': 'BORDER2', '255:124:159': 'MG_v', '255:124:160': 'MG_m',
        '255:124:161': 'MG_d', '255:125:159': 'POL', '255:126:159': 'PP',
        '255:127:159': 'LG_v', '255:127:160': 'LG_d', '255:127:161': 'IGL',
        '255:128:159': 'PF', '255:129:159': 'SPA', '255:130:159': 'SPF_m',
        '255:130:160': 'SPF_p', '255:131:159': 'LP', '255:132:159': 'PO',
        '255:132:210': 'MY', '255:133:159': 'VPM', '255:133:160': 'VPM_pc',
        '255:133:210': 'GR', '255:134:159': 'PCN', '255:134:210': 'DMX',
        '255:135:159': 'CL', '255:135:210': 'CU', '255:136:159': 'PR',
        '255:136:210': 'LRN_p', '255:136:211': 'LRN_m', '255:137:159': 'VPL',
        '255:137:160': 'VPL_pc', '255:137:210': 'NR', '255:138:159': 'SMT',
        '255:138:210': 'XII', '255:139:159': 'VM', '255:139:210': 'ECU',
        '255:140:159': 'LD', '255:140:210': 'SPV_i', '255:140:211': 'SPV_c',
        '255:141:159': 'LH', '255:141:210': 'SPIV', '255:142:159': 'MH',
        '255:142:210': 'X', '255:143:159': 'IMD', '255:143:210': 'Y',
        '255:144:159': 'RT', '255:144:210': 'DCO', '255:145:159': 'AV',
        '255:145:210': 'SPVO_rdm', '255:145:211': 'SPVO_vl', '255:145:212': 'SPVO_cdm',
        '255:145:213': 'SPVO_mdmv', '255:145:214': 'SPVO_mdmd', '255:146:159': 'AD',
        '255:146:210': 'PPY', '255:147:159': 'AM_d', '255:147:160': 'AM_v',
        '255:147:210': 'PGRN_l', '255:147:211': 'PGRN_d', '255:148:159': 'VAL',
        '255:148:210': 'PRP', '255:149:159': 'IAD', '255:149:210': 'CNlam',
        '255:149:211': 'CNspg', '255:150:159': 'RE', '255:150:210': 'LAV',
        '255:151:159': 'RH', '255:151:210': 'ACVII', '255:152:159': 'IAM',
        '255:152:210': 'SUV', '255:153:159': 'CM', '255:154:159': 'PT',
        '255:154:210': 'MV', '255:155:136': 'border7', '255:155:159': 'PVT',
        '255:155:205': 'border8', '255:155:210': 'PARN', '255:156:159': 'MD_I',
        '255:156:160': 'MD_m', '255:156:161': 'MD_c', '255:156:210': 'ISN',
        '255:157:159': 'SubG', '255:157:210': 'IRN', '255:158:159': 'SGN',
        '255:158:210': 'GRN', '255:159:210': 'RPA', '255:160:210': 'MARN',
        '255:161:210': 'VII', '255:162:210': 'VI', '255:163:210': 'VCO',
        '255:164:210': 'RM', '255:165:210': 'NTB', '255:166:134': 'PONS',
        '255:166:210': 'NTS_m', '255:166:211': 'NTS_l', '255:166:212': 'NTS_ge',
        '255:166:213': 'NTS_ce', '255:166:214': 'NTS_co', '255:167:134': 'NI',
        '255:167:210': 'AMB_v', '255:167:211': 'AMB_d', '255:167:212': 'AMB',
        '255:168:134': 'SG', '255:168:210': 'IO', '255:169:134': 'LC',
        '255:169:210': 'RO', '255:170:134': 'B', '255:170:210': 'LIN',
        '255:171:134': 'PCG', '255:171:210': 'MDRN_v', '255:171:211': 'MDRN_d',
        '255:172:134': 'SLD', '255:172:210': 'PAS', '255:173:134': 'DTN',
        '255:173:210': 'AP', '255:174:134': 'LDT', '255:174:210': 'ICB',
        '255:175:134': 'PBm_m', '255:175:135': 'PBm_me', '255:176:134': 'PBl_lv',
        '255:176:135': 'PBl_le', '255:176:136': 'PBl_ld', '255:176:137': 'PBl_lc',
        '255:176:138': 'PBl_ls', '255:177:134': 'SUT', '255:178:134': 'SLC',
        '255:179:134': 'RPO', '255:180:134': 'SOC_l', '255:180:135': 'SOC_m',
        '255:181:134': 'V', '255:182:134': 'KF', '255:183:134': 'PSV',
        '255:184:134': 'POR', '255:185:134': 'NLL_v', '255:185:135': 'NLL_d',
        '255:185:136': 'NLL_h', '255:186:134': 'PG', '255:187:134': 'TRN',
        '255:188:134': 'PRNr', '255:188:135': 'PRNc', '255:189:134': 'CS_m',
        '255:189:135': 'CS_l', '255:236:145': 'FOTU_mo', '255:236:146': 'FOTU_gr',
        '255:237:145': 'PYR_mo', '255:237:146': 'PYR_gr', '255:238:145': 'DEC_mo',
        '255:238:146': 'DEC_gr', '255:239:145': 'UVU_mo', '255:239:146': 'UVU_gr',
        '255:240:145': 'COPY_mo', '255:240:146': 'COPY_gr', '255:241:145': 'PRM_mo',
        '255:241:146': 'PRM_gr', '255:242:145': 'NOD_mo', '255:242:146': 'NOD_gr',
        '255:243:145': 'LING_mo', '255:243:146': 'LING_gr', '255:244:145': 'ANCr2_mo',
        '255:244:146': 'ANcr2_gr', '255:245:145': 'ANcr1_mo',
        '255:245:146': 'ANcr1_gr', '255:246:145': 'CENT3_mo',
        '255:246:146': 'CENT3_gr', '255:247:145': 'CUL4/5_mo',
        '255:247:146': 'CUL4/5_gr', '255:248:145': 'SIM_mo', '255:248:146': 'SIM_gr',
        '255:249:145': 'CENT2_mo', '255:249:146': 'CENT2_gr', '255:250:145': 'FL_mo',
        '255:250:146': 'FL_gr', '255:251:145': 'PFL_mo', '255:251:146': 'PFL_gr',
        '255:252:145': 'CUL_mo', '255:253:145': 'IP', '255:254:145': 'DN',
        '255:255:145': 'FN', '255:255:255': 'BORDER6', '0:0:0': 'border_11'
    }

    # CP VORONOI TE
    CPR_VORONOI = {
        '42:191:195': 'CPr.l.vm',
        '171:74:157': 'CPr.imv',
        '249:157:28': 'CPr.imd',
        '234:231:35': 'CPr.m',
        '70:195:208': 'CPr.l.ls',
    }

    CPI_VORONOI = {
        '33:122:242': 'CPi.dm.dm',
        '205:102:255': 'CPi.dm.d',
        '208:206:207': 'CPi.dm.dl',
        '197:224:181': 'CPi.dm.im',
        '10:251:32': 'CPi.dm.cd',
        '226:132:132': 'CPi.dl.d(tr)',
        '130:202:156': 'CPi.dl.imd(ll)',
        '248:9:252': 'CPi.vm.vm',
        '244:153:194': 'CPi.vm.cvm',
        '154:156:230': 'CPi.vm.v',
        '41:247:235': 'CPi.vl.cvl',
        '109:207:246': 'CPi.vl.imv(ul)',
        '246:194:137': 'CPi.vl.vt(m/o)',
        '239:244:152': 'CPi.vl.v(m/i)',
        '255:255:255': 'BORDER6'
    }

    CPC_VORONOI = {
        '101:112:200': 'CPc.d.dm',
        '230:234:131': 'CPc.d.dl',
        '97:161:136': 'CPc.d.vm',
        '109:202:205': 'CPc.i.d',
        '171:74:156': 'CPc.i.vm',
        '213:170:207': 'CPc.i.vl',
        '196:131:185': 'CPc.v',
    }
    BLAA_DIVISIONS = {
        '240:34:23': 'BLA_am',
        '23:34:240': 'BLA_al',
        '240:240:23': 'BLA_ac'
    }
    DP_DICT = {}
    SC_DIVISIONS = {
        '17:102:0': 'SCzo_div3',
        '17:102:20': 'SCop_div3',
        '17:102:80': 'SCiw_div3',
        '17:102:100': 'SCdg_div3',
        '17:102:120': 'SCdw_div3',
        '102:0:120': 'SCig_div4',
        '153:0:0': 'SCzo_div1',
        '153:0:20': 'SCsg_div1',
        '153:0:40': 'SCop_div1',
        '153:0:80': 'SCig_div1',
        '153:0:120': 'SCdg_div1',
        '153:0:130': 'SCdw_div1',
        '17:102:10': 'SCsg_div3',
        '17:102:60': 'SCig_div3',
        '102:0:140': 'SCiw_div4',
        '102:0:160': 'SCdg_div4',
        '102:0:180': 'SCdw_div4',
        '153:0:90': 'SCiw_div1',
        '255:102:0': 'SCzo_div2',
        '255:102:20': 'SCsg_div2',
        '255:102:40': 'SCop_div2',
        '255:102:80': 'SCig_div2',
        '255:102:120': 'SCiw_div2',
        '255:102:140': 'SCdg_div2',
        '255:102:160': 'SCdw_div2'
    }

    # primary dictionary name all uppercase letters
    CUSTOM_ATLAS_LOOKUP = {
        'ARA': [LOOKUP],
        'CP_VORONOI': [CPC_VORONOI, CPI_VORONOI, CPR_VORONOI],
        'CPC_VORONOI': [CPC_VORONOI],
        'CPI_VORONOI': [CPI_VORONOI],
        'CPR_VORONOI': [CPR_VORONOI],
        "BLAA_DIVISIONS": [BLAA_DIVISIONS],
        "DP": [DP_DICT],
        "SC_DIVISIONS": [SC_DIVISIONS]
    }

    CUSTOM_ATLAS_CLEAR_DEFAULT_LOOKUP = {
        'ARA': False,
        'CP_VORONOI': True,
        'CPC_VORONOI': True,
        'CPI_VORONOI': True,
        'CPR_VORONOI': True,
        'BLAA_DIVISIONS': False,
        'DP': False,
        'SC_DIVISIONS': False
    }

    BLA_REGION = [
        'BLA_am',
        'BLA_al',
        'BLA_ac'
    ]

    CP_REGION = [
        'CPc.v.vm',
        'CPc.v.vl',
        'CPc.ext.d',
        'CPc.ext.v'
    ]
    CPI_REGION = [
        'CPi.dl.d.r',
        'CPi.vl.imv.r',
        'CPi.vl.v.r'
    ]
    ACB_REGION = [
        'ACBsh.m',
        'ACBsh.l',
        'ACBc.v'
    ]

    CUSTOM_REGIONS_LOOKUP = {
        'CP': [CP_REGION, CPI_REGION],
        # 'BLA': [BLA_REGION]
        'ACB': [ACB_REGION]
    }

    DEFAULT_ASSOCIATED_ATLAS = 'ARA'

    def __init__(self, custom_atlas="ARA"):
        if custom_atlas not in TranslateColors.CUSTOM_ATLAS_LOOKUP:
            raise UnknownCustomAtlasError(custom_atlas)
        self.associated_atlas = custom_atlas

        if self.associated_atlas == TranslateColors.DEFAULT_ASSOCIATED_ATLAS:
            self.LOOKUP = deepcopy(TranslateColors.LOOKUP)
        else:
            if TranslateColors.CUSTOM_ATLAS_CLEAR_DEFAULT_LOOKUP[self.associated_atlas]:
                self.LOOKUP = {}
            else:
                self.LOOKUP = deepcopy(TranslateColors.LOOKUP)
            self.custom_atlas_init()
        self.REV_LOOKUP = {}
        for k, v in self.LOOKUP.items():
            self.REV_LOOKUP[v] = k

    def __eq__(self, other):
        assert isinstance(other, TranslateColors), "operator == between TranslateColors and another type is not defined"
        return self.associated_atlas == other.associated_atlas

    def custom_atlas_init(self):
        for custom_atlas_ in TranslateColors.CUSTOM_ATLAS_LOOKUP[self.associated_atlas]:
            for rgb, roi in custom_atlas_.items():
                if rgb in self.LOOKUP:
                    warnings.warn("rgb code clashing: default {0}: {1}. custom {2}: {3}".
                                  format(rgb, TranslateColors.LOOKUP[rgb],
                                         rgb, self.LOOKUP[rgb]), RuntimeWarning)
                self.LOOKUP[rgb] = roi

    def rgblisttoregionlist(self, rgbcodelist):
        reglist = []
        for code in rgbcodelist:
            reglist.append(self.rgbtoregion(code))
        return reglist

    def rgbtoregion(self, rgb):
        try:
            ret = self.LOOKUP[rgb]
        except KeyError:
            ret = '??!' + rgb + '!??'
        return ret

    def regiontorgb(self, region):
        try:
            ret = self.REV_LOOKUP[region]
        except KeyError:
            ret = '??!' + region + '!??'
        return ret

    @staticmethod
    def colorstring_to_index(colorstring):
        """
        colorstring is same format as key of TranslateColors.LOOKUP
        :param colorstring:
        :return: integer rgb index
        """
        r, g, b = colorstring.strip().split(':')
        return int(r) * 256 * 256 + int(g) * 256 + int(b)

    @staticmethod
    def index_to_colorstring(rgb_index):
        '''
        rgb_index is rgb index value
        :param rgb_index:
        :return: colorstring in TranslateColors.LOOKUP key format
        '''
        r, g, b = TranslateColors.index_to_rgb(rgb_index)
        return str(r) + ':' + str(g) + ':' + str(b)

    @staticmethod
    def rgb_to_index(rgb):
        """
        rgb is tuple of (r, g, b)
        :param rgb:
        :return: integer rgb index
                """
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return int(r) * 256 * 256 + int(g) * 256 + int(b)

    @staticmethod
    def index_to_rgb(rgb_index):
        """
        parse r, g, b values from rgb index
        :param rgb_index:
        :return: r, g, b
        """
        r = rgb_index >> 16
        g = rgb_index >> 8 & 255
        b = rgb_index & 255
        return r, g, b

    def index_to_region(self, rgb_index):
        color_str = TranslateColors.index_to_colorstring(rgb_index)
        return self.LOOKUP[color_str]

    @staticmethod
    def rgbatlas_to_indexatlas(rgb_atlas):
        """
        given a 3 channel rgb atlas image,
        return a index atlas with rgb index at each pixel location
        :param rgb_atlas:
        :return: index_atlas
        """
        assert len(rgb_atlas.shape) == 3, "rgb_atlas must have r, g, b channels"
        r_val = rgb_atlas[:, :, 2].astype(np.int32) * 256 * 256
        g_val = rgb_atlas[:, :, 1].astype(np.int32) * 256
        b_val = rgb_atlas[:, :, 0]
        index_atlas = r_val + g_val + b_val
        return index_atlas

    @staticmethod
    def available_atlas():
        atlas_names = []
        for k in TranslateColors.CUSTOM_ATLAS_LOOKUP.keys():
            # TODO Case like region names, capword all else
            atlas_name = string.capwords(k.replace('_', " "))
            atlas_names.append(atlas_name)
        return atlas_names

    @staticmethod
    def atlas_name_to_key(atlas_name):
        key = atlas_name.upper().replace(' ', '_')
        if key in TranslateColors.CUSTOM_ATLAS_LOOKUP:
            return key
        else:
            sys.stderr.write("Cannot get {} as valid atlas, using ARA".format(atlas_name))
            return 'ARA'

    @staticmethod
    def known_regions():
        region_names = set()
        for lookup_key in TranslateColors.CUSTOM_ATLAS_LOOKUP:
            for lookup_table in TranslateColors.CUSTOM_ATLAS_LOOKUP[lookup_key]:
                new_regions = lookup_table.values()
                region_names = region_names.union(new_regions)
        for lookup_key in TranslateColors.CUSTOM_REGIONS_LOOKUP:
            for new_regions in TranslateColors.CUSTOM_REGIONS_LOOKUP[lookup_key]:
                region_names = region_names.union(new_regions)
        return list(region_names)

