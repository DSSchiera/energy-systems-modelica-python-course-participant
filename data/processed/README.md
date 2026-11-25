# Course data

## `weather_turin_tmy.csv` — typical meteorological year, Turin

| | |
|---|---|
| **Source** | PVGIS 5.3, European Commission Joint Research Centre (JRC), tool *TMY* |
| **Site** | Turin, Italy: latitude 45.070° N, longitude 7.687° E, elevation 250 m (as reported by PVGIS) |
| **Data** | solar radiation PVGIS-SARAH3; other variables ERA5; years 2005–2023; horizon shading included |
| **Downloaded** | 2026-11-19 |
| **Rows** | 8760 hourly values, time stamps in UTC |
| **Irradiance time offset** | 0.1762 h: rows are labelled HH:00, the irradiance values belong to HH:10.6 UTC (PVGIS-SARAH3 time stamp); use it when computing the sun position |

Columns, as delivered by PVGIS:

| Column | Quantity | Unit |
|--------|----------|------|
| `time_utc` | time stamp (UTC) | – |
| `T2m` | 2-m air temperature | °C |
| `RH` | relative humidity | % |
| `G(h)` | global irradiance on the horizontal plane | W/m² |
| `Gb(n)` | beam irradiance on a plane normal to the sun rays | W/m² |
| `Gd(h)` | diffuse irradiance on the horizontal plane | W/m² |
| `IR(h)` | infrared (thermal) irradiance on the horizontal plane | W/m² |
| `WS10m` | 10-m wind speed | m/s |
| `WD10m` | 10-m wind direction (0 = N, 90 = E) | ° |
| `SP` | surface air pressure | Pa |

A typical meteorological year joins twelve months taken from different years. The months were
taken from: Jan 2016, Feb 2006, Mar 2019, Apr 2023, May 2011, Jun 2012, Jul 2018, Aug 2006,
Sep 2007, Oct 2005, Nov 2007, Dec 2016. The time stamps therefore jump between years at month
boundaries. Use `energy_training.data.weather.load_tmy()` to get one continuous year in SI units.

**Reuse.** JRC data may be reused provided the source is acknowledged (JRC Data Policy, 2019,
Art. 6; Commission Decision 2011/833/EU). Credit line, as given by the JRC for PVGIS data:
*PVGIS © European Communities, 2001-2026.*

The meteorological variables (all except the irradiance columns) come from ERA5, a Copernicus
Climate Change Service product (Copernicus licence, cl. 5.1.2–5.1.3): *Contains modified
Copernicus Climate Change Service information 2026. Neither the European Commission nor ECMWF is
responsible for any use that may be made of the Copernicus information or data it contains.*
