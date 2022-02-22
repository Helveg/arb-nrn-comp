import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import os
import time
import pickle
import dbbs_models
import arbor
from arbor import single_cell_model

def plot():
    arb_data = {}
    for name, model in vars(dbbs_models).items():
        if name.endswith("Cell"):
            print("Running", name, flush=True)
            arb_model = single_cell_model(model.cable_cell(labels=arbor.label_dict({"midpoint": "(root)"})))
            arb_model.properties.set_ion(
                ion="h", valence=1, int_con=1.0, ext_con=1.0, rev_pot=-34
            )
            arb_model.properties.catalogue = model.get_catalogue()
            arb_model.probe('voltage', '"midpoint"', frequency=10)
            arb_model.run(10, dt=0.025)
            arb_data[name] = go.Figure(go.Scatter(x=m.traces[0].time, y=m.traces[0].value))
    return arb_data
