
import numpy as np
import pandas as pd
import tigramite
import tigramite.data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.cmiknn import CMIknn
import matplotlib.pyplot as plt

def load_ts(filename):
    X=pd.read_csv(filename)
    return np.array(X['x'])
suffix='.daily.detrend.csv'
f_nics=['gun_data/raw/background_checks_daily.np']
f_twit=['gun_data/raw/users_count_daily_proreg.np',
            'gun_data/raw/users_count_daily_antireg.np']
#'gun_data/raw/media_violence.np',
f_med=[
            'gun_data/raw/media_regulation.np',
            'gun_data/raw/media_shootings.np',
            'gun_data/raw/media_violence.np',
           
]
        
def name_vars(v):
    return [x.split('/')[-1].replace(
            '.np','').replace('_daily','').replace(
            '_count','')
            for x in v]
import statsmodels.api as sm
import scipy.stats


vars_=f_nics+f_med+f_twit
file_names=[v+suffix for v in vars_]
data=np.array([(load_ts(fname)) for fname in file_names]).T

N=len(file_names)
var_names=name_vars(vars_)

dataframe = pp.DataFrame(data, 
                 datatime = np.arange(data.shape[0]), 
                 var_names=var_names)


pcmci=PCMCI( 
    dataframe=dataframe, 
    cond_ind_test=CMIknn(sig_samples=250),verbosity=4)

results = pcmci_corr1.run_pcmci(tau_max=2, pc_alpha=0.05, max_conds_dim=2)

pcmci.print_significant_links(
    p_matrix = results['p_matrix'],
    val_matrix = results['val_matrix'],
    alpha_level = 0.05)

tp.plot_graph(
    val_matrix=results['val_matrix'],
    graph=results['graph'],
    var_names=var_names,
    link_colorbar_label='cross-MCI',
    node_colorbar_label='auto-MCI',
    )
plt.show()
