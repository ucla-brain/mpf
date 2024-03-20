import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage

def compute_pr(df_projection, df_input):
    # Drop the 'Case ID' and the last column which seems to contain NaN values
    df_projection = df_projection.drop(['Case ID', df_projection.columns[-1]], axis=1)
    df_input = df_input.drop(['Case ID', df_input.columns[-1]], axis=1)
    
    # Set the 'Injection Site' as the index
    df_projection = df_projection.set_index('Injection Site')
    df_input = df_input.set_index('Injection Site')
    
    # Ensure the columns match for both dataframes, assuming they should be the same
    if not all(df_projection.columns == df_input.columns):
        raise ValueError("The columns of the two matrices do not match.")
    
    # Compute the numerator (min part) and denominator (max part) of the formula
    min_matrix = np.minimum(df_projection, df_input)
    max_matrix = np.maximum(df_projection, df_input)
    # Replace zeros in max_matrix to avoid division by zero
    max_matrix.replace(0, np.finfo(float).eps, inplace=True)
    
    # Calculate the reciprocity matrix based on the provided formula
    df_pr = (min_matrix / max_matrix) * ((df_projection + df_input) / 2)
    
    return df_pr

def _mod_cos_pair_distance(v0, v1):
        """ modified cosine for fractions, cosine for densities """
        epsilon = 1e-6
        cosine_d = 1 - np.dot(v0, v1) / \
                       (np.linalg.norm(v0, 2) * np.linalg.norm(v1, 2) + epsilon)
        r_d = max(np.sum(v0), np.sum(v1)) / (min(np.sum(v0), np.sum(v1)) + epsilon)
        return cosine_d * r_d
    
def cluster_2d(selected_matrix_df, roi_lbls, inj_site_lbls, title=None, 
               out_dir=None, fmt=None):
    if not isinstance(selected_matrix_df, pd.DataFrame):
        raise ValueError('expecting pandas DataFrame')
    
    # create a selected_matrix np array
    selected_matrix = selected_matrix_df.values

    # Check that the matrix dimensions match the labels provided
    if selected_matrix.shape[0] != len(inj_site_lbls):
        raise ValueError('matrix row number and injection labels length inconsistent')
    if selected_matrix.shape[1] != len(roi_lbls):
        raise ValueError('matrix column number and roi labels length inconsistent')

    # distances between inj sites and regions  
    inj_site_distance_vec = pdist(selected_matrix, _mod_cos_pair_distance)
    inj_site_distance_vec = np.clip(inj_site_distance_vec,
                                a_min=0, a_max=np.iinfo('i').max)
    inj_site_distance_vec[np.isnan(inj_site_distance_vec)] = 0
    Z_injections = linkage(inj_site_distance_vec, method='complete')
    Z_injections = np.clip(Z_injections, a_min=0, a_max=np.inf)

    D = np.transpose(selected_matrix)
    region_distance_vec = pdist(D, _mod_cos_pair_distance)
    region_distance_vec = np.clip(region_distance_vec,
                                    a_min=0, a_max=np.iinfo('i').max)
    region_distance_vec[np.isnan(region_distance_vec)] = 0
    Z_rois = linkage(region_distance_vec, method='complete')
    Z_rois = np.clip(Z_rois, a_min=0, a_max=np.inf)

    # create visualization dataframe
    vis_ceil_val = 0.1
    vis_df = pd.DataFrame(np.clip(selected_matrix, 0, vis_ceil_val),
                          index=inj_site_lbls, columns=roi_lbls, copy=True)

    # Create Seaborn clustermap
    cg = sns.clustermap(vis_df, row_linkage=Z_injections, col_linkage=Z_rois,
                        xticklabels=True, cmap='copper', robust=False,
                        figsize=(30, 2))

    # Set the title if provided
    if title is not None:
        cg.fig.suptitle(title)

    # Set up the heatmap aesthetics
    plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
    plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90, fontsize=8)

    # cg.ax_heatmap.tick_params(axis='x', which='major', rotation=90, labelsize=8,)

    # Show plot if no output directory is provided
    if out_dir is None:
        plt.show()
    else:
        # Save the plot to the specified directory
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        fig_path = os.path.join(out_dir, '{}_cluster.{}'.format(title, fmt))
        plt.savefig(fig_path, dpi=600)

