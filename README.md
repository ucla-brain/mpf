# Medial Prefrontal Cortex (MPFC) Connectivity Analysis
This repo contains analysis code and data for the paper `Neural Networks of the Mouse Primary Visceromotor Cortex`.

### Data
* The directories SW******-**A each contains anterograde and retrograde tracer quantificatification data for a single rodent brain.
* `case_sheet.csv` contains the injection site and tracers used for each rodent brain.
* `mpfc_analysis.py` performs analysis and visualization for MPFC regions. It reads the raw data listed in `case_sheet.csv`, computes the fraction and density connectivity matrices, and plots the connectivity matrices as scatter plots and 2D heatmaps.
  * You can run  script from within the repo: `python -m mpfc_analysis.py`.
* `connectivity_bar_plot.ipynb` computes connectivity "reciprocity" between brain regions, using fraction matrices of both anterograde and retrograde tracers.
  * `mpfc_anterograde_ctx_fractions_all_merge.csv` and `mpfc_retrograde_ctx_fractions_all_merge.csv` are example inputs. The numbers in these sheets are merged fraction results across multiple rodent brains.  
