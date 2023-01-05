# data_preparation.py


"""

Useful functions for handling PV System Timeseries Data


"""


__all__ = ["get_timestep_interval"]


import numpy as np
import pandas as pd
from scipy import stats
from pvlib import irradiance


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


def pv_day_filter(data, lat, lon, tilt, azimuth, timesteplen):

    site = Location(lat, lon)
    index = data.index
    times = pd.date_range(index[0], index[-1], freq=str(timesteplen) + "T")
    clearsky = site.get_clearsky(times)
    solar_position = site.get_solarposition(times=times)
    # Use the get_total_irradiance function to transpose the GHI to POA
    POA_irradiance = irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        dni=clearsky["dni"],
        ghi=clearsky["ghi"],
        dhi=clearsky["dhi"],
        solar_zenith=solar_position["apparent_zenith"],
        solar_azimuth=solar_position["azimuth"],
    )

    day_index = POA_irradiance[POA_irradiance["poa_global"] > 0].index

    data_day_values = data.reindex(day_index).dropna()

    return data_day_values
