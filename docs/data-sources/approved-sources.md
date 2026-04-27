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

## Demographic and Health

- UN Population Division — historical and projected demographics
- WHO Global Health Observatory
- Our World in Data — aggregated cross-domain datasets
