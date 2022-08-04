# data_preparation.py


"""

Useful functions for handling PV System Timeseries Data


"""


__all__ = ["get_timestep_interval"]


import numpy as np
import pandas as pd
from scipy import stats


def get_timestep_interval(df):
    """Infers the interval of the DateTimeIndex of a pd.DataFrame in seconds."""
    timesteplens = []
    for i in range((int(df.shape[0] * 0.5))):
        diff = df.index[i + 1] - df.index[i]
        timesteplen = int(diff.total_seconds())
        timesteplens.append(timesteplen)
    timesteplen_final = int(stats.mode(np.array(timesteplens)).mode[0])

    return timesteplen_final


def reindexer(df, ts_freq: int):
    return df.reindex(pd.date_range(df.index[0], df.index[-1], freq=str(ts_freq) + "S"))
