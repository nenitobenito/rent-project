# rent-project

This repository does not include the data used in the analysis, as it is licensed from third parties (e.g. Ordnance Survey, ...) and cannot be redistributed. To reproduce this analysis, you will need to obtain:

- [Dataset name] from [source]
- [Dataset name] from [source]
- Place files in data/raw/

This project consists of three stages:

01 Assembling dataset

uv run build-dataset

02 Modelling rental and price values

uv run fit-models

Plus a notebook for model diagnostics and comparison

03 Analysis

A notebook