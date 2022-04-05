import h5py
import numpy as np
from bsb.plotting import hdf5_plot_spike_raster
import itertools

def plot():
    with h5py.File("results/results_arbor.hdf5", "a") as f, h5py.File("results/results_nrn_fixed.hdf5", "r") as g:
        f.require_group("recorders/deduped")
        del f["recorders/deduped"]
        f.require_group("recorders/deduped")
        avg_arb = {}
        for spikes in f["recorders/soma_spikes"].values():
            # Accidentally, the spikes of each synapse instead of just the soma were recorded,
            # meaning that all along the axon, duplicated spikes with slightly different times
            # are recorded; so we remove all duplicates that occur in rapid succession of
            # eachother.
            nondupes = np.diff(np.sort(spikes)) > 1
            # Super optimized numpy code, please copy paste to all your own projects.
            ns = np.concatenate(([spikes[0]], spikes[1:][nondupes]))
            avg_arb.setdefault(spikes.attrs["display_label"], []).append(len(ns))
            ds = f["recorders/deduped"].create_dataset(str(spikes.attrs['cell_id']), data=ns)
            for k,v in spikes.attrs.items():
                ds.attrs[k] = v
        avg_nrn = {}
        for spikes in g["recorders/soma_spikes"].values():
            avg_nrn.setdefault(spikes.attrs["display_label"], []).append(len(spikes))
        print("Averages, Arbor:")
        for k, v in avg_arb.items():
            print(f" *{k}:", np.mean(v), "std", np.std(v))
        print("Averages, nrn:")
        for k, v in avg_nrn.items():
            print(f" *{k}:", np.mean(v), "std", np.std(v))
        nrn = hdf5_plot_spike_raster(g["recorders/soma_spikes"], show=False)
        arb = hdf5_plot_spike_raster(f["recorders/deduped"], show=False)
        for dat in itertools.chain(nrn.data, arb.data):
            dat.marker.size = 2
        return {"nrn": nrn, "arb": arb}
