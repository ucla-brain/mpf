# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


#import image_resources
from translate_colors import TranslateColors
'''
    This file hard codes all available Tracers and their associated colors,
    color codes (for colorize_tif), and the color code scale image files.
    REGIONS - list of regions (injection sites) dynamically generated from
        tranlsate colors hard coded dictionary
    TRACER_TYPES - List of valid Tracer types
    TRACERTOCOLOR - dictionary of tracer names mapped to a color
        color must be defined in both COLORTOCODE and COLORTOSCALEIMAGE
    TRACERTOTYPE -dictionary of tracer names mapped to type(ant/ret/both)
    TRACERTOLIMS - dictionary of tracer names mapped to name in LIMS
    TRACERTOTABLE - dictionary of tracer names mapped to name in Reg table
    COLORTOCODE - dictionary of colors to rgb scaling values for gray -> color
    NOTE - to use image files in COLORTOSCALEIMAGE make sure module imports
        image_resources
    TO ADD NEW TRACERS
        - Add name as key to TRACERTOCOLOR with value a key in COLORTOCODE
        - Add same name as key to TRACERTOTYPE with value a member of
            TRACER_TYPES
        - Add same name as key to TRACERTOTABLE with value of name in reg table
        - Add same name as key to TRACERTOLIMS with value of name in LIMS
'''


class TracersAndRegions:
    TRACER_ANT = 'Anterograde'
    TRACER_RET = 'Retrograde'
    TRACER_EITHER = 'Antereograde/Retrograde'
    TRACER_RB = 'Rabies'
    TRACER_NONE = None
    TRACER_TYPES = [TRACER_ANT, TRACER_RET, TRACER_EITHER, TRACER_RB]
    REGIONS = TranslateColors.known_regions()
    # keep these single line
    TRACERTOCOLOR = {
        'Nissl': 'Blue',
        'PHAL': 'Green',
        'FG': 'Gold',
        'BDA': 'Red',
        'CTB-488': 'Green',
        'CTB-555': 'Red',
        'CTB-549': 'Red',
        'CTB-647': 'Purple',
        'AAV-GFP': 'Green',
        'AAV-RFP': 'Red',
        'RB-BFP': 'Blue',
        'RB-GFP': 'Green',
        'RB-mCherry': 'Red',
        'RB-GFP+CTB-488': 'Green',
        'RB-mCherry+CTB-555': 'Red',
        'rb.4gfp': 'Green',
        'rb.4tdtomato': 'Red',
        'PHAL-647': 'Purple',
        'EM48': 'Purple',
        'AAV-tdTomato': 'Red',
        'AAVRetro-Cre': 'Purple',
        'AAVRetro-Cre+CTB-488': 'Green',
        'AAVRetro-CRE(UNC)': 'Purple',
        'AAVRetro-RPF(UNC)': 'Red',
        'RetroAAV-GFP': 'Green',
        'RetroAAV-tdTomato': 'Red',
        'AAV1.eGFP': 'Green',
        'AAV1.tdTomato': 'Red',
        'AAV1-EF1a-DIO-HB': 'Green',
        'smRB-HA+CTB-488': 'Green',
        'smRB-HA+CTB-555': 'Red',
        'smRB-HA+CTB-647': 'Purple',
        'smRB-OLLAS+CTB-488': 'Green',
        'smRB-OLLAS+CTB-555': 'Red',
        'smRB-OLLAS+CTB-647': 'Purple',
        'smRB-V5+CTB-488': 'Green',
        'smRB-V5+CTB-555': 'Red',
        'smRB-V5+CTB-647': 'Purple',
        'AAV8-hSyn-FLEX-TVA-P2A-GFP-2A-oG': 'Green',
        'EnvA-RB-RVdG-4mCherry': 'Red',
        'EnvA-RB-dsRedXpress': 'Red',
        'EnvA-RB-mCherry': 'Red'
    }

    # Consider adding unlocked generic tracers to options
    GEN_TRACERS = {
        'retro_red': 'Red',
        'retro_green': "Green",
        'retro_blue': "Blue",
        'retro_gold': "Gold",
        'retro_purple': 'Purple',
        'retro_cyan': "Cyan",
        'antero_red': 'Red',
        'antero_green': "Green",
        'antero_blue': "Blue",
        'antero_gold': "Gold",
        'antero_purple': 'Purple',
        'antero_cyan': "Cyan",
        'rabies_red': 'Red',
        'rabies_green': "Green",
        'rabies_blue': "Blue",
        'rabies_gold': "Gold",
        'rabies_purple': 'Purple',
        'rabies_cyan': "Cyan"
    }

    # TO ADD Awaiting clarifying info
    TRACERTOTYPE = {
        'Nissl': TRACER_NONE,
        'PHAL': TRACER_ANT,
        'FG': TRACER_RET,
        'BDA': TRACER_EITHER,
        'CTB-488': TRACER_RET,
        'CTB-555': TRACER_RET,
        'CTB-549': TRACER_RET,
        'CTB-647': TRACER_RET,
        'AAV-GFP': TRACER_ANT,
        'AAV-RFP': TRACER_ANT,
        'RB-BFP': TRACER_RB,
        'RB-GFP': TRACER_RB,
        'RB-mCherry': TRACER_RB,
        'RB-GFP+CTB-488': TRACER_RB,
        'RB-mCherry+CTB-555': TRACER_RB,
        'rb.4gfp': TRACER_RB,
        'rb.4tdtomato': TRACER_RB,
        'PHAL-647': TRACER_ANT,
        'EM48': TRACER_EITHER,
        'AAV-tdTomato': TRACER_ANT,
        'AAVRetro-Cre': TRACER_RET,
        'AAVRetro-Cre+CTB-488': TRACER_RET,
        'AAVRetro-CRE(UNC)': TRACER_RET,
        'AAVRetro-RPF(UNC)': TRACER_RET,
        'RetroAAV-GFP': TRACER_RET,
        'RetroAAV-tdTomato': TRACER_RET,
        'AAV1.eGFP': TRACER_EITHER,
        'AAV1.tdTomato': TRACER_EITHER,
        'AAV1-EF1a-DIO-HB': TRACER_EITHER,
        'smRB-HA+CTB-488': TRACER_RB,
        'smRB-HA+CTB-555': TRACER_RB,
        'smRB-HA+CTB-647': TRACER_RB,
        'smRB-OLLAS+CTB-488': TRACER_RB,
        'smRB-OLLAS+CTB-555': TRACER_RB,
        'smRB-OLLAS+CTB-647': TRACER_RB,
        'smRB-V5+CTB-488': TRACER_RB,
        'smRB-V5+CTB-555': TRACER_RB,
        'smRB-V5+CTB-647': TRACER_RB,
        'AAV8-hSyn-FLEX-TVA-P2A-GFP-2A-oG': TRACER_EITHER,
        'EnvA-RB-RVdG-4mCherry': TRACER_RB,
        'EnvA-RB-dsRedXpress': TRACER_RB,
        'EnvA-RB-mCherry': TRACER_RB
    }
    TRACERTOLIMS = {
        'Nissl': None,
        'PHAL': u'phal',
        'FG': u'fg',
        'BDA': u'bda',
        'CTB-488': u'ctb-488',
        'CTB-555': u'ctb-555',
        'CTB-549': u'ctb-549',
        'CTB-647': u'ctb-647',
        'AAV-GFP': u'aav-gfp',
        'AAV-RFP': u'aav-rfp',
        'RB-BFP': u'rb-bfp',
        'RB-GFP': u'rb-gfp',
        'RB-mCherry': u'rb-mCherry',
        'RB-GFP+CTB-488': u'rb-gfp+ctb-488',
        'RB-mCherry+CTB-555': u'rb-mcherry+ctb-555',
        'rb.4gfp': u'rb.4gfp',
        'rb.4tdtomato': u'rb.4tdtomato',
        'PHAL-647': u'phal-647',
        'EM48': None,
        'AAV-tdTomato': u'aav-tdTomato',
        'AAVRetro-Cre': u'aavRetro-Cre',
        'AAVRetro-Cre+CTB-488': u'aav-retro-cre+ctb-488',
        'AAVRetro-CRE(UNC)': u'aav-retro-cre-unc',
        'AAVRetro-RPF(UNC)': u'aav-retro-rfp-unc',
        'RetroAAV-GFP': u'raav-gfp',
        'RetroAAV-tdTomato': u'raav-tdtomato',
        'AAV1.eGFP': u'aav1.eGfp',
        'AAV1.tdTomato': u'aav1.tdTomato',
        'AAV1-EF1a-DIO-HB': u'aav1-ef1a-dio-hb',
        'smRB-HA+CTB-488': u'smrb-HA+ctb-488',
        'smRB-HA+CTB-555': u'smrb-HA+ctb-555',
        'smRB-HA+CTB-647': u'smrb-ha+ctb-647',
        'smRB-OLLAS+CTB-488': u'smrb-ollas+ctb-488',
        'smRB-OLLAS+CTB-555': u'smrb-OLLAS+ctb-555',
        'smRB-OLLAS+CTB-647': u'smrb-OLLAS+ctb-647',
        'smRB-V5+CTB-488': u'smrb-V5+ctb-488',
        'smRB-V5+CTB-555': u'smrb-v5+ctb-555',
        'smRB-V5+CTB-647': u'smrb-V5+ctb-647',
        'AAV8-hSyn-FLEX-TVA-P2A-GFP-2A-oG': u'aav8-hsyn-flex-tva-p2a-gfp-2a-og',
        'EnvA-RB-RVdG-4mCherry': u'enva-gdel-rb-rvdg-4mcherry',
        'EnvA-RB-dsRedXpress': u'enva-gdel-rb-dsredexpress',
        'EnvA-RB-mCherry': u'enva-gdel-rb-mcherry'
    }
    TRACERTOTABLE = {
        'Nissl': 'nissl',
        'PHAL': 'phal',
        'FG': 'fg',
        'BDA': 'bda',
        'CTB-488': 'ctb-488',
        'CTB-555': 'ctb-555',
        'CTB-549': 'ctb-549',
        'CTB-647': 'ctb-647',
        'AAV-GFP': 'aav-gfp',
        'AAV-RFP': 'aav-rfp',
        'RB-BFP': 'rb-bfp',
        'RB-GFP': 'rb-gfp',
        'RB-mCherry': 'rb-mCherry',
        'RB-GFP+CTB-488': 'rb-gfp+ctb-488',
        'RB-mCherry+CTB-555': 'rb-mCherry+ctb-555',
        'rb.4gfp': 'rb.4gfp',
        'rb.4tdtomato': 'rb.4tdtomato',
        'PHAL-647': 'phal-647',
        'EM48': None,
        'AAV-tdTomato': 'aav-tdTomato',
        'AAVRetro-Cre': 'aavRetro-Cre',
        'AAVRetro-Cre+CTB-488': 'aav-retro-cre+ctb-488',
        'AAVRetro-CRE(UNC)': 'aav-retro-cre-unc',
        'AAVRetro-RPF(UNC)': 'aav-retro-rfp-unc',
        'RetroAAV-GFP': 'raav-gfp',
        'RetroAAV-tdTomato': 'raav-tdtomato',
        'AAV1.eGFP': 'aav1.eGfp',
        'AAV1.tdTomato': 'aav1.tdTomato',
        'AAV1-EF1a-DIO-HB': 'aav1-ef1a-dio-hb',
        'smRB-HA+CTB-488': 'smrb-HA+ctb-488',
        'smRB-HA+CTB-555': 'smrb-HA+ctb-555',
        'smRB-HA+CTB-647': 'smrb-ha+ctb-647',
        'smRB-OLLAS+CTB-488': 'smrb-ollas+ctb-488',
        'smRB-OLLAS+CTB-555': 'smrb-OLLAS+ctb-555',
        'smRB-OLLAS+CTB-647': 'smrb-OLLAS+ctb-647',
        'smRB-V5+CTB-488': 'smrb-V5+ctb-488',
        'smRB-V5+CTB-555': 'smrb-v5+ctb-555',
        'smRB-V5+CTB-647': 'smrb-V5+ctb-647',
        'AAV8-hSyn-FLEX-TVA-P2A-GFP-2A-oG': 'aav8-hsyn-flex-tva-p2a-gfp-2a-og',
        'EnvA-RB-RVdG-4mCherry': 'enva-gdel-rb-rvdg-4mcherry',
        'EnvA-RB-dsRedXpress': 'enva-gdel-rb-dsredexpress',
        'EnvA-RB-mCherry': 'enva-gdel-rb-mcherry'
    }
    COLORTOCODE = {
        'Blue': '0,0,1',
        'Green': '0,1,0',
        'Gold': '1,1,0',
        'Red': '1,0,0',
        'Purple': '1,0,1',
        'Cyan': '0,1,1'
    }
    COLORTOSCALEIMAGE = {
        'Blue': ':/color-scale/blue.png',
        'Green': ':/color-scale/green.png',
        'Gold': ':/color-scale/gold.png',
        'Red': ':/color-scale/red.png',
        'Purple': ':/color-scale/purple.png',
        'Cyan': ':/color-scale/cyan.png',
    }

    @staticmethod
    def get_tracers():
        return [t for t in TracersAndRegions.TRACERTOCOLOR]

    # returns a dictionary of tracer names:
    # key = lowercase tracername
    # value = full tracer name as used in TRACERTOCOLOR dictionary
    @staticmethod
    def get_lowercase_tracers_to_name():
        return {t.lower(): t for t in TracersAndRegions.TRACERTOCOLOR}

    @staticmethod
    def get_colors():
        return [c for c in TracersAndRegions.COLORTOCODE]

    @staticmethod
    def get_types():
        return TracersAndRegions.TRACER_TYPES

    @staticmethod
    def get_tracer_type(tracer):
        if tracer in TracersAndRegions.TRACERTOTYPE:
            return TracersAndRegions.TRACERTOTYPE[tracer]
        return None

    @staticmethod
    def get_tracer_code(tracer):
        if tracer in TracersAndRegions.TRACERTOCOLOR:
            color = TracersAndRegions.TRACERTOCOLOR[tracer]
            if color in TracersAndRegions.COLORTOCODE:
                return TracersAndRegions.COLORTOCODE[color]
        return None

    @staticmethod
    def get_tracer_color(tracer):
        if tracer in TracersAndRegions.TRACERTOCOLOR:
            return TracersAndRegions.TRACERTOCOLOR[tracer]
        return None

    @staticmethod
    def get_color_code(color):
        if color in TracersAndRegions.COLORTOCODE:
            return TracersAndRegions.COLORTOCODE[color]
        return None

    @staticmethod
    def get_color_scale_pixmap(color):
        if color in TracersAndRegions.COLORTOSCALEIMAGE:
            return TracersAndRegions.COLORTOSCALEIMAGE[color]
        return None

    @staticmethod
    def get_tracer_lims_name(tracer):
        if tracer in TracersAndRegions.TRACERTOLIMS:
            return TracersAndRegions.TRACERTOLIMS[tracer]
        return None

    @staticmethod
    def get_tracer_table_name(tracer):
        if tracer in TracersAndRegions.TRACERTOTABLE:
            return TracersAndRegions.TRACERTOTABLE[tracer]
        return None

    @staticmethod
    def get_table_tracer_id(table_name):
        table_to_tracer = {v: k for k, v in
                           TracersAndRegions.TRACERTOTABLE.iteritems()
                           if v is not None}
        if table_name in table_to_tracer:
            return table_to_tracer[table_name]
        return None
