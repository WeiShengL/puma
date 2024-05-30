"""Example of histogram plot that deviates from puma default plots."""

from __future__ import annotations

import numpy as np

from puma import Histogram, HistogramPlot
import h5py
import pandas as pd


fname_dict = {
    "zprime_UFO": '/share/rcifdata/wlai/dataset/p6057/low_stats/zprime_UFO/merged.h5',
}
for keys in fname_dict:
    with h5py.File(fname_dict[keys], 'r') as hdf:
        jets_array = np.array(hdf.get('jets'))
        # dR_tracks_array = np.array(hdf.get('dRtracks'))
        # GA_tracks_array = np.array(hdf.get('GAtracks'))
df = pd.DataFrame(jets_array)


# pt_bins = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]
pt_bins = np.linspace(300, 5000, 50)
avg_n_dRtracks = []
avg_n_GAtracks = []
for i in range(len(pt_bins)-1):
    select = df.loc[(df['pt']/1000 > pt_bins[i]) & (df['pt']/1000 < pt_bins[i+1])]
    avg_n_dRtracks.append(select['n_dRtracks'].mean())
    avg_n_GAtracks.append(select['n_GAtracks'].mean())



# # Generate two distributions to plot
# N_BKG = int(1e6)
# N_SIG = int(2e4)
# rng = np.random.default_rng(seed=42)
# expectation = rng.exponential(size=N_BKG)
# measurement = np.concatenate((
#     rng.exponential(size=N_BKG),
#     rng.normal(loc=2, scale=0.2, size=N_SIG),
# ))
# expectation_hist = Histogram(expectation, label="MC", histtype="stepfilled", alpha=1)
# measurement_hist = Histogram(measurement, label="dummy data")
    
dRtracks_hist = Histogram(avg_n_dRtracks, label="dR tracks", histtype="stepfilled", alpha=1)
GAtracks_hist = Histogram(avg_n_GAtracks, label="Ghost tracks", histtype="stepfilled", alpha=1)
print(avg_n_dRtracks)

# Initialise histogram plot
plot_histo = HistogramPlot(
    ylabel="Track Multiplicity",
    xlabel="pT",
    logy=False,
    # bins=np.linspace(0, 5, 60),  # you can force a binning for the plot here
    # bins=50,  # you can also define an integer number for the number of bins
    # bins_range=(1.1, 4),  # only considered if bins is an integer
    bins=pt_bins,
    norm=False,
    atlas_first_tag="Simulation Internal",
    atlas_second_tag="Example for more general plot",
    figsize=(6, 5),
    n_ratio_panels=1,
)

# Add histograms and plot
plot_histo.add(dRtracks_hist, reference=True)
plot_histo.add(GAtracks_hist)
plot_histo.draw()

plot_histo.savefig("/share/rcifdata/wlai/projects/UFO/data_plot/track_multiplicity.png", transparent=False)
