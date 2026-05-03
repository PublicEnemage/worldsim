# Approved Data Sources

> Extracted from CLAUDE.md at M4 exit (2026-04-26). These are the intended
> data sources for WorldSim. All sources must be registered in the
> `source_registry` table before their data is loaded into the simulation.
> Data quality tiers, provenance requirements, and backtesting integrity
> rules are governed by `docs/DATA_STANDARDS.md`.

---

## Economic and Financial

- World Bank Open Data — GDP, health, education, poverty (historical)
- IMF Balance of Payments Statistics
- BIS International Banking Statistics
- UNCTAD FDI database
- Tax Justice Network illicit flow estimates

## Geopolitical and Governance

- V-Dem (Varieties of Democracy) — institutional quality indicators
- Freedom House — press freedom, political rights
- Transparency International — corruption perception
- GDELT Project — coded global events since 1979
- Uppsala Conflict Data Program — armed conflict database

## Climate and Physical

- ERA5 Reanalysis (Copernicus) — historical climate 1940-present
- NOAA Climate Data Online
- UK Met Office HadCRUT
- IPCC Scenario Data (SSP/RCP) — future climate projections
- FAO AQUASTAT — water resources data

## Ecological

- **NASA/NOAA Mauna Loa CO2 Atmospheric Measurements** — Atmospheric CO2
  concentration time series (1958–present). *License:* Public domain (US
  Government data). *Access:* NOAA GML FTP (ftp.cmdl.noaa.gov) and NOAA GML
  API. *Supports:* `co2_concentration_ppm` (STOCK) on country entities;
  global atmospheric stock shared across all entities.

- **Stockholm Resilience Centre Planetary Boundary Calibrations** —
  Authoritative boundary values for the nine planetary boundary domains
  (climate change, biosphere integrity, land-system change, freshwater use,
  biogeochemical flows, ocean acidification, atmospheric aerosol loading,
  stratospheric ozone, novel entities). Published in Rockström et al. (2009)
  and Richardson et al. (2023). *License:* CC BY 4.0 (journal supplementary
  materials). *Access:* DOI 10.1126/science.abn2458 (Richardson 2023);
  tabular boundary values in supplementary data. *Supports:*
  `planetary_boundary_proximity` ratio calculations — boundary values are the
  denominator in proximity scoring; required before any M6 ecological
  indicator can be expressed as a fraction of safe operating space.

- **FAO Global Forest Resources Assessment (FRA)** — Country-level forest
  area, deforestation rates, and land-use change data, published every 5
  years (most recent: FRA 2020). *License:* CC BY-NC-SA 3.0 IGO. *Access:*
  https://www.fao.org/forest-resources-assessment/en/ (national data tables
  available as CSV download). *Supports:* `land_use_pressure_index` (RATIO) —
  fraction of country forest coverage change relative to safe land-system
  boundary; confidence tier 3 (5-year data requires annual interpolation).

- **Global Carbon Project — CO2 Budget Data** — Annual global and national
  CO2 emissions, land-use change emissions, and ocean/land sink estimates
  (1959–present). Published annually in *Earth System Science Data*.
  *License:* CC BY 4.0. *Access:* https://globalcarbonproject.org/carbonbudget/;
  ICOS data portal. *Supports:* `co2_trajectory` (FLOW) — annual CO2
  emissions as a FLOW input to the atmospheric CO2 stock; country-level
  emissions attribution for responsibility metrics.

## Demographic and Health

- UN Population Division — historical and projected demographics
- WHO Global Health Observatory
- Our World in Data — aggregated cross-domain datasets
