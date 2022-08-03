Copyright (c) 2022 Nikolaus Houben

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# PV Utility Suite

## Prelude

This repository is a collection of useful python modules for PV System Engineering. They make use of the core functionalities of the <a href="https://pvlib-python.readthedocs.io/en/stable/" target="_blank">pvlib</a> package, but extend these for specific problems I had to solve within my own research. 

I have included a tutorial-style jupyter notebook, pre-trained models, and exemplary data, which should allow you to make full use of this repo in no time. 

## List of Modules

* tilt_and_azimuth_inference: If all you have is some measurement data from a PV system and you would to find out its tilt and azimuth angles, this module has got you covered. 
* inverse_pv_yield_model: If you would like to transpose your measurement data back into ghi, dni, and dhi irradiance data, this module is for you. 
* data_cleaning_module: If you need some powerful functions to clean you PV system measurement data to prepare it for your 
 
  – remove night values
