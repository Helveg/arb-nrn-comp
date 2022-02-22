import plotly.graph_objs as go
from pathlib import Path
import numpy as np
import os
os.environ["USING_NEURON"] = "TRUE"
import dbbs_models
import dbbs_models.test
import time
import pickle
from patch import p

def plot():
    nrn_data = {}
    pkl_data = {}
    for name, model in vars(dbbs_models).items():
        if name.endswith("Cell"):
            print("Running", name)
            nrn_data[name] = []
            cell = model()
            time = p.time
            dbbs_models.test.quick_test(cell, duration=1000)
            nrn_data[name] = (list(time), list(cell.Vm))
            arb_data[name] = go.Figure(go.Scatter(x=nrn_data[name][0], y=nrn_data[name][1]))
    with open("arb_sc.pkl", "wb") as f:
        pickle.dump(pkl_data, f)
