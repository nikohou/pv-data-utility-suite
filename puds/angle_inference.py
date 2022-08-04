# angle_inference.py

"""

Infer the tilt and azimuth angle of a PV system based on PV system power measurement data.

"""


__all__ = []


import pandas as pd
import numpy as np
import itertools
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from pvlib.pvsystem import PVSystem
from pvlib.location import Location
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS


def physical_profile(row, df_irr):
    latitude, longitude, tilt, azimuth, capacity = row

    temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS["sapm"][
        "open_rack_glass_glass"
    ]

    location = Location(latitude=latitude, longitude=longitude)

    pvwatts_system = PVSystem(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        module_parameters={"pdc0": capacity, "gamma_pdc": -0.004},
        inverter_parameters={"pdc0": capacity},
        temperature_model_parameters=temperature_model_parameters,
    )

    mc = ModelChain(
        pvwatts_system, location, aoi_model="physical", spectral_model="no_loss"
    )
    mc.run_model(df_irr)
    results = mc.results.ac

    df_results = pd.Series(results)
    df_results.index = df_results.index.tz_localize(None)
    df_results.index.name = "timestamp"
    df_results.name = str(tilt) + ";" + str(azimuth)

    return df_results


def infer_tilt_azimuth(df_irr, df_measurements, location, verbose):

    "Pass a dataset for PV Meta Data: Location, Tilt, Azimuth, Capacity and a Dataset for irradiance: DNI, DHI, GHI to calculate profiles with PV Watts"

    latitude, longitude, tilt_estimated, azimuth_estimated, capacity = row

    first_timestep = df_measurements.index[0]
    last_timestep = df_measurements.index[-1]
    df_irr = df_irr[first_timestep:last_timestep]
    n_combis = len(combinations)
    counter = 0
    errors = {}

    combinations = get_combinations()

    for combi in combinations:
        counter += 1
        tilt = combi[0]
        azimuth = combi[1]

        temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS["sapm"][
            "open_rack_glass_glass"
        ]

        pvwatts_system = PVSystem(
            surface_tilt=tilt,
            surface_azimuth=azimuth,
            module_parameters={"pdc0": capacity, "gamma_pdc": -0.004},
            inverter_parameters={"pdc0": capacity},
            temperature_model_parameters=temperature_model_parameters,
        )

        mc = ModelChain(
            pvwatts_system, location, aoi_model="physical", spectral_model="no_loss"
        )
        mc.run_model(df_irr)
        results = mc.results.ac
        df_results = pd.Series(results)
        df_results.index = df_results.index.tz_localize(None)
        df_results.index.name = "timestamp"

        df_compare = pd.merge(
            df_results, df_measurements, left_index=True, right_index=True
        )

        scaler = MinMaxScaler()
        df_compare[df_compare.columns] = scaler.fit_transform(
            df_compare[df_compare.columns]
        )

        df_compare = df_compare.replace(
            0, np.nan
        )  # excluding the 0s in the error calculations
        df_compare.dropna(inplace=True)

        if (
            counter % int((0.05 * n_combis)) == 0 and verbose
        ):  # plot every 5% of iterations
            print(counter)
            print(df_compare.head())
        errors[combi] = mean_squared_error(
            df_compare.iloc[:, :1], df_compare.iloc[:, -1:]
        )

    # picking out the tilt/azimuth combination with the lowest error
    df_errors = pd.DataFrame.from_dict(errors, orient="index")
    df_errors.sort_values(by=0)

    tilt_derived = df_errors.iloc[:1, :].index[0][0]
    azimuth_derived = df_errors.iloc[:1, :].index[0][1]

    print(
        "Old estimated 'azimuth angle' was {0} and new estimated azimuth is {1}".format(
            azimuth_estimated, azimuth_derived
        )
    )
    print(
        "Old estimated 'tilt angle' was {0} and new estimated 'tilt angle' is {1}".format(
            tilt_estimated, tilt_derived
        )
    )

    return tilt_derived, azimuth_derived
