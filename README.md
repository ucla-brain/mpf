# Medial Prefrontal Cortex (MPFC) Connectivity Analysis
This repository contains analysis code and data for the paper `Neural Networks of the Mouse Primary Visceromotor Cortex`.

### System requirements
This software is designed to work with any computer running Python 3 but was developed for Linux, and specifically tested on Ubuntu 22.04.5 and Linux Mint 21.3. As detailed in the installation guide, all package requirements are listed in requirements.txt. No non-standard hardware is required. 

### Installation guide
Installation can be performed in seconds using a Python 3 virtual environment:

```
python3 -m venv mpf_venv
. mpf_venv/bin/activate
pip install -r requirements.txt
```

### Demo and Instructions for use
The directories SW******-**A each contains anterograde and retrograde tracer quantificatification data for a single rodent brain.

The file `case_sheet.csv` contains the injection site and tracers used for each rodent brain.

The `mpfc_analysis.py` program performs analysis and visualization for MPFC regions. It reads the raw data listed in `case_sheet.csv`, computes the fraction and density connectivity matrices, and plots the connectivity matrices as scatter plots and 2D heatmaps. You can run  script from within the repo: 
  
```
python -m mpfc_analysis
```

resulting in the output of approximately 100 images with corresponding metadata will be written to plots/ over the span of about 5 minutes.

The notebook `do_mpfc_analysis.ipynb` computes connectivity "reciprocity" between brain regions, using fraction matrices of both anterograde and retrograde tracers. `mpfc_anterograde_ctx_fractions_all_merge.csv` and `mpfc_retrograde_ctx_fractions_all_merge.csv` are example inputs. The numbers in these sheets are merged fraction results across multiple rodent brains.  
