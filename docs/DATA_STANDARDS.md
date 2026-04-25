# WorldSim Data Standards

WorldSim ingests data from dozens of source systems with different encodings,
calendar systems, unit conventions, currency bases, territorial assumptions,
and quality levels. Without explicit standards, these differences produce
silent errors — outputs that look plausible, pass code review, and mislead
users.

Seasonal and fiscal calendar errors are among the most dangerous because they
produce outputs that are systematically wrong in ways that survive testing.
Unit errors lose spacecraft. Float monetary arithmetic accumulates error
across thousands of simulation steps. Territorial assumptions embed contested
political positions without declaring them.

These standards exist to make such errors loud and immediate rather than
silent and cumulative.

---

## Character Encoding and Language

### Encoding: UTF-8 Everywhere

All text data in WorldSim — source files, database content, API responses,
configuration, logs — is UTF-8. No exceptions.

Conversion to UTF-8 is the **mandatory first step** of every data ingestion
pipeline, before any other processing. Source data that arrives in Latin-1,
Windows-1252, ISO-8859-1, or any other encoding is converted immediately
on ingestion. The raw bytes are discarded after conversion. Only UTF-8 bytes
enter the processing pipeline.

```python
def ingest_csv(path: Path, encoding: str = "utf-8") -> pd.DataFrame:
    """Ingest a CSV file, converting to UTF-8 before any processing."""
    raw_bytes = path.read_bytes()
    text = raw_bytes.decode(encoding, errors="strict")  # fail loud, not silent
    utf8_bytes = text.encode("utf-8")
    return pd.read_csv(io.BytesIO(utf8_bytes))
```

`errors="strict"` — never `errors="ignore"` or `errors="replace"`. Silent
encoding errors corrupt data without any signal.

### Internal Language: English

The simulation's internal canonical language is English. This is a pragmatic
choice, not a cultural one. The primary data sources (World Bank, IMF, BIS,
UN agencies) publish reference data in English. Using English internally
minimizes transformation loss between source and simulation.

**Simulation reproducibility requires this.** Two users running the same
scenario in different display languages must produce identical internal
simulation states. Language-dependent simulation logic would make scenarios
non-reproducible across language settings — a backtesting integrity failure.

**Implementation principle:** Translation keys, not translated strings,
exist in the simulation layer. Translation to the user's display language
happens at the presentation boundary only.

```python
# Forbidden — translated string in simulation layer
entity.metadata["name"] = "Grèce"

# Correct — translation key in simulation layer, resolved at presentation
entity.metadata["name_key"] = "country.GRC.name"
entity.metadata["name_en"] = "Greece"  # canonical fallback
```

The translation key registry lives in `frontend/src/i18n/`. The simulation
engine has no dependency on it.

---

## DateTime Standards

### UTC Everywhere in Storage

All timestamps stored in the database are UTC. The database layer never
stores local times. Never.

```sql
-- Correct column type
observation_timestamp TIMESTAMPTZ NOT NULL,

-- Forbidden — no timezone context
observation_timestamp TIMESTAMP NOT NULL,
```

### ISO 8601 Always

- Dates: `YYYY-MM-DD` (e.g., `2023-04-15`)
- Timestamps: `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2023-04-15T14:30:00Z`)
- Durations: ISO 8601 duration format (e.g., `P1Y` for one year, `P3M` for
  three months)

No other date format appears in data storage, API responses, or configuration.

### Timezone of Origin

The timezone where a measurement was taken or recorded is stored as a
separate field using [IANA timezone database](https://www.iana.org/time-zones)
names, not UTC offsets.

```python
@dataclass
class TimestampedObservation:
    value: Decimal
    utc_timestamp: datetime          # always UTC
    origin_timezone: str             # IANA name, e.g. "Asia/Beirut"
    observation_date: date           # date in origin timezone
```

**Rationale:** UTC offsets change with daylight saving time. IANA names are
stable identifiers that resolve correctly across historical DST transitions.

Timezone conversion is a presentation concern, not a data concern. The
database layer does not perform timezone conversion. The presentation layer
performs it on display only.

---

## Calendar Support Architecture

### The Calendar Service

A dedicated `CalendarService` owns all calendar arithmetic in WorldSim.
The simulation engine calls the service and never performs calendar math
directly.

```python
class CalendarService:
    def to_gregorian(self, date: CalendarDate) -> date: ...
    def from_gregorian(self, date: date, system: CalendarSystem) -> CalendarDate: ...
    def fiscal_year_for(self, country: str, date: date) -> FiscalYear: ...
    def season_for(self, date: date, context: SeasonalContext) -> str: ...
    def days_in_period(self, start: date, end: date, calendar: CalendarSystem) -> int: ...
    def add_period(self, date: CalendarDate, period: str) -> CalendarDate: ...
```

This isolates calendar complexity into one tested and maintainable place.
Calendar arithmetic is notoriously error-prone — leap year rules, intercalary
months, and epoch differences are non-trivial. Centralizing this prevents the
same bugs from appearing independently across modules.

### Supported Calendar Systems

The simulation must correctly model economic phenomena that are
calendar-system-dependent. Ramadan effects on economic activity, lunar
agricultural cycles, and fiscal year boundaries that follow non-Gregorian
systems are not approximations — they are first-class simulation inputs.

**Gregorian** — Universal baseline. All other systems convert through
Gregorian for cross-system comparisons.

**Islamic Hijri (Lunar)** — 12 lunar months of 29 or 30 days. Approximately
354 days per year, advancing ~11 days relative to Gregorian each year.
Essential for correct modeling of Middle East and North Africa economic
cycles, Ramadan effects on banking hours, retail patterns, and government
activity, and Hajj-related economic flows in Saudi Arabia. Library:
`hijri-converter`.

**Solar Hijri (Persian/Shamsi)** — Used in Iran and Afghanistan. Solar year,
12 months of 29-31 days, new year at vernal equinox (Nowruz, approximately
March 20-21 Gregorian). Iranian fiscal year runs 1 Farvardin to 29 Esfand
(approximately March 21 to March 20). Any backtesting case involving Iran
requires correct Solar Hijri date handling. Library: `jdatetime`.

**Hebrew** — Lunisolar calendar. Used for Israel's religious calendar, Jewish
diaspora economic networks, and relevant for modeling certain Israeli fiscal
and religious holiday effects. Intercalary month added in leap years.
Library: `pyluach`.

**Ethiopian** — 13-month calendar (12 months of 30 days plus Pagumē of 5 or
6 days). Ethiopian fiscal year runs Hamle to Sene (approximately July to
June Gregorian). Essential for East Africa scenarios — Ethiopia is the region's
largest economy. Library: `ethiopian-date`.

### Extension Points

The `CalendarSystem` enum and `CalendarService` are designed for extension.
Adding a new calendar requires:
1. Implementing the `CalendarConverter` protocol for the new system
2. Registering it in `CalendarService`
3. Adding conversion test cases against known reference dates
4. Documenting any simulation phenomena that require the calendar system

---

## Fiscal Year Registry

Fiscal years are political boundaries, not astronomical ones. Countries choose
fiscal year boundaries based on history, climate, agricultural cycles, and
administrative tradition. Those choices change over time.

### `FiscalYearDefinition` Type

```python
@dataclass
class FiscalYearDefinition:
    country_code: str              # ISO 3166-1 alpha-3
    start_month: int               # 1-12 in Gregorian
    start_day: int                 # day of start_month
    naming_convention: FiscalYearNaming  # see below
    calendar_system: CalendarSystem      # calendar in which FY is defined
    effective_from: date           # when this definition became effective
    effective_to: date | None      # None means currently in effect
    notes: str                     # exceptions, legislative basis, history

class FiscalYearNaming(Enum):
    START_YEAR = "start_year"   # FY named for year it starts (US: FY2023 starts Oct 2022)
    END_YEAR = "end_year"       # FY named for year it ends (UK: FY2023 ends Mar 2023)
    STRADDLE = "straddle"       # Both years referenced (India: 2022-23)
```

### Naming Convention Resolution Is Mandatory

"FY2023" means different calendar periods in different countries:

| Country | FY start | FY end | Named for |
|---|---|---|---|
| United States | October 1, 2022 | September 30, 2023 | Year it ends |
| United Kingdom | April 6, 2022 | April 5, 2023 | Year it ends |
| Australia | July 1, 2022 | June 30, 2023 | Year it ends |
| Japan | April 1, 2022 | March 31, 2023 | Year it starts |
| India | April 1, 2022 | March 31, 2023 | Both (2022-23) |
| Pakistan | July 1, 2022 | June 30, 2023 | Year it ends |
| Ethiopia | July 8, 2022 | July 7, 2023 | Ethiopian calendar |

Any cross-country fiscal comparison that does not resolve this is producing
wrong results. The registry enforces resolution:

```python
def resolve_fiscal_year(
    country: str,
    label: str,           # e.g. "FY2023" or "2022-23"
    reference_date: date, # to select correct historical definition
) -> tuple[date, date]:   # (fy_start, fy_end) in Gregorian
```

### Historical Definitions Required for Backtesting

Countries change their fiscal years. The registry must support multiple
historical definitions per country. Known historical changes include:

- **Pakistan:** Changed from April-March to July-June in 1973
- **Bangladesh:** Changed from July-June to January-December in 2009-10,
  then back to July-June
- **New Zealand:** Changed from April-March to July-June in 1989
- **Ethiopia:** The Ethiopian fiscal year is defined in the Ethiopian calendar;
  any scenario involving Ethiopia before Gregorian adoption must account for this

Backtesting scenarios must use the fiscal year definition that was in effect
at the scenario start date, not the current definition.

---

## Seasonal Data Standards

Seasonal errors are among the most dangerous data errors in a global simulation
system. They produce outputs that are systematically wrong in ways that are
plausible to human reviewers, survive code review, and pass tests that check
for numeric plausibility without checking seasonal logic. A comparison between
Chilean grape harvest data and Californian grape harvest data that fails to
account for hemispheric inversion will show peak production in opposite quarters
and produce a structural agricultural module error with no obvious failure
signal.

### `SeasonalContext` Type

Attached to all time-series data that carries seasonal meaning:

```python
@dataclass
class SeasonalContext:
    reference_frame: SeasonalFrame
    hemisphere: Hemisphere
    region: str | None = None        # for monsoon, regional cyclone frames
    crop: str | None = None          # for crop-specific agricultural seasons
    seasons: dict[str, DateRange]    # named season -> date range in relevant calendar
    seasonally_adjusted: bool = False
    adjustment_methodology: str | None = None  # "X-13ARIMA-SEATS", "STL", etc.
    adjustment_base_country: str | None = None # whose seasonal removed (ISO alpha-3)

class SeasonalFrame(Enum):
    ASTRONOMICAL = "astronomical"    # solstice/equinox-defined
    AGRICULTURAL = "agricultural"    # growing season defined by FAO crop calendar
    MONSOON = "monsoon"              # defined by monsoon onset/retreat
    FISCAL = "fiscal"               # fiscal quarter / fiscal year
    CYCLONE = "cyclone"             # tropical cyclone season
    CUSTOM = "custom"               # regionally defined, documented in notes

class Hemisphere(Enum):
    NORTHERN = "northern"
    SOUTHERN = "southern"
    TROPICAL = "tropical"
    NOT_APPLICABLE = "not_applicable"  # for non-geographic seasons
```

### Hemisphere-Aware Season Name Mapping

Summer, winter, spring, and autumn map to opposite calendar periods in
opposite hemispheres. No hardcoded calendar ranges for season names appear
anywhere in the simulation engine.

```python
ASTRONOMICAL_SEASONS = {
    Hemisphere.NORTHERN: {
        "spring": DateRange(month_start=3, day_start=20, month_end=6, day_end=20),
        "summer": DateRange(month_start=6, day_start=21, month_end=9, day_end=22),
        "autumn": DateRange(month_start=9, day_start=23, month_end=12, day_end=20),
        "winter": DateRange(month_start=12, day_start=21, month_end=3, day_end=19),
    },
    Hemisphere.SOUTHERN: {
        "spring": DateRange(month_start=9, day_start=23, month_end=12, day_end=20),
        "summer": DateRange(month_start=12, day_start=21, month_end=3, day_end=19),
        "autumn": DateRange(month_start=3, day_start=20, month_end=6, day_end=20),
        "winter": DateRange(month_start=6, day_start=21, month_end=9, day_end=22),
    },
}
```

### Growing Season Registry

FAO crop calendar data ([https://www.fao.org/giews/cropmonitor/](https://www.fao.org/giews/cropmonitor/))
defines planting and harvest windows by crop by country. The agricultural
module uses this registry for all seasonal calculations — hardcoding crop
seasons is not permitted.

```python
@dataclass
class CropSeasonDefinition:
    country_code: str          # ISO 3166-1 alpha-3
    crop_fao_code: str         # FAO crop code
    crop_name_en: str
    planting_start: MonthDay
    planting_end: MonthDay
    harvest_start: MonthDay
    harvest_end: MonthDay
    hemisphere: Hemisphere
    season_type: str           # "main", "secondary", "off-season"
    notes: str
```

### Tropical and Monsoon Seasons

Tropical and monsoon seasons are a distinct framework from astronomical seasons,
defined by regional physical phenomena — onset of the Indian Ocean monsoon,
ITCZ migration, sea surface temperature thresholds. They do not map cleanly
onto the solstice/equinox framework.

Indian subcontinent monsoon: southwest monsoon typically onset June (Kerala),
withdrawal October-November. This timing is consequential for agricultural
output, rural income, and public health outcomes. Modeled using IMD (India
Meteorological Department) monsoon onset/withdrawal records, not approximated
from calendar.

### Seasonal Adjustment Metadata

When ingesting seasonally adjusted data, record:
- Which methodology removed the seasonal component (X-13ARIMA-SEATS, STL,
  Census Bureau X-11, other)
- Which country's seasonal pattern was removed — a seasonally adjusted US
  retail series has US seasonal patterns removed; comparing it raw to a
  South African series that had South African seasonals removed will produce
  cross-hemisphere artifacts

Cross-hemisphere comparisons of seasonally adjusted data are explicitly flagged
in simulation output.

---

## Units and Measurements

### The `Quantity` Type

All physical and economic measurements in the simulation are represented as
`Quantity`. Never raw `float`, never raw `Decimal` without a unit.

```python
class VariableType(Enum):
    STOCK = "stock"           # level at a point in time (reserves, debt outstanding)
    FLOW = "flow"             # change over a period (GDP, exports, deficit)
    RATIO = "ratio"           # dimensionless fraction derived from other quantities
    DIMENSIONLESS = "dimensionless"  # index or score not reducible to a ratio

@dataclass(kw_only=True)
class Quantity:
    value: Decimal             # never float
    unit: Unit
    variable_type: VariableType  # required; see VariableType enum above
    observation_date: date
    source_registry_id: str    # must be registered in SourceRegistry
    confidence_tier: int       # 1–5, see Data Quality Tier System

    def convert_to(self, target_unit: Unit) -> "Quantity":
        """Convert to target unit. Raises UnitError if dimensions incompatible."""
        if self.unit.dimension != target_unit.dimension:
            raise UnitError(
                f"Cannot convert {self.unit.dimension} to {target_unit.dimension}"
            )
        ...
```

#### Confidence Tier Propagation

When a calculation derives a new `Quantity` from existing `Quantity` inputs,
the output `confidence_tier` is the **maximum** of all input tier numbers
(higher number = lower confidence quality; the output inherits the worst-quality
input's tier).

```
confidence_tier(output) = max(confidence_tier(input₁), confidence_tier(input₂), ...)
```

This is a deliberately conservative policy approximation, not a statistical
formula. Its properties:

- **Monotone non-decreasing**: derived quantities cannot be more confident
  than their least confident input.
- **Known direction bias**: it overstates uncertainty when inputs are
  independent and mutually corroborating. This is documented and accepted.
  Code comments must not describe it as a statistical rule.
- **Not a statistical formula**: it governs the `confidence_tier` integer field
  only. Where genuine statistical propagation of probability distributions is
  required (e.g., Monte Carlo quantification), use the appropriate statistical
  method instead.

The rule applies to all arithmetic derivations: ratios, sums, differences,
products. It does not apply to:
- Pure unit conversions of a single `Quantity` (no new uncertainty introduced)
- Currency conversions where the exchange rate carries its own `confidence_tier`
  (apply the rule to the exchange rate `Quantity` and the input monetary `Quantity`)

All functions that derive `Quantity` outputs from `Quantity` inputs must
explicitly compute and pass `confidence_tier=max(...)` — no implicit defaulting.

**Known Limitation (IA-1):** This rule does not account for projection horizon.
A 30-year forward projection derived from a Tier 1 historical observation retains
Tier 1 confidence under this rule, which overstates reliability for long-horizon
projections. See the formal definition, canonical disclosure text, and remediation
plan in **Known Limitation IA-1: Projection Horizon Confidence** at the end of
this document (Issue #69, Milestone 4).

### The `Unit` Type

```python
@dataclass
class Unit:
    dimension: Dimension
    scale: Decimal          # multiplier relative to SI base unit
    offset: Decimal         # for non-ratio scales (Celsius: 273.15, Fahrenheit: 255.372)
    symbol: str             # display symbol, e.g. "km²"
    name: str               # full name, e.g. "square kilometre"
```

### Dimensions

```python
class Dimension(Enum):
    # Physical
    MONETARY_VALUE = "monetary_value"
    POPULATION = "population"
    MASS = "mass"
    ENERGY = "energy"
    POWER = "power"
    TEMPERATURE = "temperature"
    AREA = "area"
    VOLUME = "volume"
    LENGTH = "length"
    TIME_DURATION = "time_duration"
    # Derived
    CROP_YIELD = "crop_yield"            # mass per area (kg/ha)
    ENERGY_INTENSITY = "energy_intensity" # energy per capita (J/person) or power per capita
    MONETARY_PER_CAPITA = "monetary_per_capita"
    # Dimensionless
    RATIO = "ratio"
    INDEX = "index"
```

### Canonical Internal Units

The simulation engine stores all quantities in canonical units. Conversion
to display units happens at the presentation boundary.

| Dimension | Canonical Unit | Symbol | Rationale |
|---|---|---|---|
| Monetary value | Constant 2015 USD | USD_2015 | Matches World Bank ICP base year for cross-country PPP comparability |
| Population | Integer persons | persons | Persons, not thousands — loss of precision in large-country aggregations |
| Mass | Kilogram | kg | SI base |
| Energy | Joule | J | SI base; covers electricity, heat, fuel |
| Power | Watt | W | SI base |
| Temperature | Kelvin | K | Ratio scale; Celsius and Fahrenheit require offset conversion |
| Area | Square kilometre | km² | World Bank and FAO standard for country-level geography |
| Volume | Cubic metre | m³ | SI base; covers water, gas |
| Length | Metre | m | SI base |
| Time duration | Second for sub-day; ISO 8601 date for calendar time | s / date | |
| Crop yield | Kilogram per hectare | kg/ha | FAO standard |
| Ratio / rate | Decimal fraction | — | Percentages are a display convention only |

### Dimensional Safety

Unit conversion raises `UnitError` immediately and loudly when dimensions are
incompatible. Silent coercion is not permitted.

```python
# This must raise UnitError immediately
gdp = Quantity(value=Decimal("44e9"), unit=USD_2015, ...)
population = Quantity(value=Decimal("12e6"), unit=PERSONS, ...)
gdp.convert_to(PERSONS)  # raises UnitError: cannot convert monetary_value to population
```

### Specific Conversion Coverage Required

**Energy:**
- BTU → J: 1 BTU = 1055.06 J
- Tonne of oil equivalent (TOE) → J: 1 TOE = 41.868 GJ (IEA convention)
  — the IEA uses a net calorific value convention; document this explicitly
  as different sources use different TOE definitions
- Kilowatt-hour → J: 1 kWh = 3,600,000 J
- Cubic metre of natural gas → J: country-specific calorific values required;
  use IEA country-specific heat content data, not a single global average

**Agricultural yield:**
- US bushel conversions are crop-specific:
  - Wheat: 1 bushel = 27.2155 kg
  - Corn (maize): 1 bushel = 25.4012 kg
  - Soybeans: 1 bushel = 27.2155 kg
  - Barley: 1 bushel = 21.7724 kg
- Never apply a single bushel weight to all crops

**Population scale:**
- Persons, thousands of persons, millions of persons — always check source
  table headers; IMF data frequently uses millions without labeling

**Temperature:**
- Celsius → Kelvin: K = °C + 273.15
- Fahrenheit → Kelvin: K = (°F + 459.67) × 5/9
- Offset handling is required — temperature ratios are meaningless in
  non-Kelvin scales (20°C is not twice 10°C)

**Geographic area:**
- km² → m²: 1 km² = 1,000,000 m²
- Square mile → km²: 1 mi² = 2.58999 km²
- Hectare → km²: 1 ha = 0.01 km²
- Acre → km²: 1 acre = 0.00404686 km²

### Dimensionless Quantities and Index Numbers

Index numbers (HDI, Freedom House score, V-Dem indicators) are not convertible
to other units. They carry:
- `methodology_version`: the version of the index methodology used
- `base_year`: if applicable
- `provider`: the institution publishing the index

Index values from different methodology versions are not directly comparable
and must not be mixed in a single time series without explicit handling.

### Ratios and Rates Are Decimal Fractions

Percentages are a display convention. Internally, all ratios and rates are
decimal fractions:

```python
# Correct internal representation
inflation_rate = Decimal("0.082")  # 8.2%
debt_gdp_ratio = Decimal("1.46")   # 146%
unemployment_rate = Decimal("0.271")  # 27.1%

# Forbidden — percentages as internal values
inflation_rate = Decimal("8.2")
```

Conversion to percentage for display: `value * 100` at the presentation
boundary only. The simulation never performs arithmetic on percentage-scale
values.

---

## Currency and Monetary Value Standards

### The `MonetaryValue` Type

All monetary measurements use `MonetaryValue`. Never raw numbers for money.

`MonetaryValue` is a `Quantity` subclass. All `Quantity` rules — including
`variable_type`, `confidence_tier`, and `source_registry_id` requirements —
apply to monetary values.

```python
@dataclass(kw_only=True)
class MonetaryValue(Quantity):
    """A Quantity that is specifically a monetary amount.

    Inherits from Quantity: value, unit, variable_type, observation_date,
    source_registry_id, confidence_tier.

    The inherited 'value' field is the monetary amount (replaces the former
    'amount' field). The inherited 'unit' field carries the canonical storage
    unit (USD_2015) or the source currency unit before conversion at ingestion.
    'currency_code' is the ISO 4217 code of the source currency; it is
    redundant with 'unit' for canonical values but required at ingestion before
    conversion so the pipeline can construct the correct Unit.
    """
    currency_code: str               # ISO 4217, e.g. "USD", "EUR", "GHS"
    price_basis: PriceBasis
    exchange_rate_type: ExchangeRateType

class PriceBasis(Enum):
    NOMINAL = "nominal"              # current prices at observation date
    CONSTANT = "constant"           # real terms; base_year encoded in unit
    PPP = "ppp"                     # PPP-adjusted; base_year encoded in unit

class ExchangeRateType(Enum):
    OFFICIAL = "official"
    PARALLEL = "parallel"           # black market / unofficial rate
    PPP = "ppp"
    FIXED = "fixed"                 # pegged rate; document peg terms in metadata
```

**Note on the `amount` → `value` rename:** The former standalone `amount` field
is removed. Access the monetary amount via the inherited `value` field from
`Quantity`. Code using `monetary_value.amount` must be updated to `monetary_value.value`.

**Cross-reference:** `CODING_STANDARDS.md § Monetary and Quantity Standards`
governs usage rules. This section governs the type contract.

### Canonical Internal Currency: Constant 2015 USD

All stored monetary values in the simulation are in constant 2015 USD
(World Bank International Comparison Program base year). This enables:
- Cross-country comparison at PPP-adjusted real values
- Consistent backtesting without nominal price level distortion
- Alignment with the most widely used international dataset base year

An unmarked monetary value — one without an explicit `price_basis` and
`currency_code` — is a data quality error and must be rejected at ingestion.

### Exchange Rate Regime Awareness

The simulation distinguishes official from parallel market rates as a
first-class property. In countries with significant official/unofficial
divergence, using the official rate for simulating real purchasing power
produces systematically wrong human cost outputs.

**Countries requiring parallel rate data (non-exhaustive):**

| Country | Period | Source | Notes |
|---|---|---|---|
| Iran | 2012-present | Multiple aggregators; no single authoritative source | Sanctions-driven divergence |
| Venezuela | 2003-present | DolarToday (historical), official + black market tracked | Extreme divergence during hyperinflation |
| Argentina | Periodic | Oficial vs. blue dollar | Recurrent FX controls |
| Zimbabwe | 2008-2009, 2019-present | Historical records, current aggregators | Hyperinflation period requires special handling |
| Lebanon | 2019-present | BDL official vs. Sayrafa vs. parallel | Three-tier rate system |
| Egypt | 2016, 2022-2023 | EGP official vs. black market | Around devaluation periods |

### PPP vs. Market Rate Assignment

The rule is not optional:
- **Human cost ledger outputs** use PPP rates — these measure real purchasing
  power and living standards, not financial flows
- **Financial flow outputs** (debt service, trade balances, reserve adequacy)
  use market exchange rates — these are the rates at which actual transactions
  occur
- **Mixed outputs** document explicitly which concept applies to which component

Using PPP for debt service calculations or market rates for poverty comparisons
are both methodological errors.

### Historical Exchange Rate Sources

- **BIS** (Bank for International Settlements): Major currency pairs, daily
  rates with correct vintage dating. Use for backtesting scenarios involving
  major currencies.
- **IMF International Financial Statistics (IFS)**: Broad country coverage,
  monthly. Use for developing country currency scenarios.
- **Federal Reserve H.10**: Major currencies against USD, daily. Use for USD
  bilateral rate precision.
- **World Bank**: Annual data, broad coverage, consistent with WDI baselines.
  Use for annual averages in long-run scenarios.

Vintage dating is required. An exchange rate must be recorded with the date
it was first published, not just the observation date.

### Currency Event Registry

The registry records events that break monetary continuity:

```python
@dataclass
class CurrencyEvent:
    country_code: str
    event_type: CurrencyEventType
    old_currency_code: str          # ISO 4217
    new_currency_code: str          # ISO 4217
    effective_date: date
    conversion_factor: Decimal      # units of old per unit of new
    notes: str                      # legislative basis, IMF classification

class CurrencyEventType(Enum):
    REDENOMINATION = "redenomination"     # same currency, remove zeros
    REPLACEMENT = "replacement"           # new currency introduced
    DOLLARIZATION = "dollarization"       # foreign currency adopted
    DEDOLLARIZATION = "dedollarization"
    CURRENCY_UNION_ENTRY = "union_entry"
    CURRENCY_UNION_EXIT = "union_exit"
```

Known events requiring registry entries (non-exhaustive):
- Zimbabwe: ZWD → ZWN (2006, ÷1000), ZWN → ZWR (2008, ÷10B), ZWR → ZWL
  (2009, ÷10^12), ZWL abandoned (2009), ZWL reintroduced (2019)
- Brazil: Cruzeiro → Cruzado (1986), Cruzado → Cruzado Novo (1989),
  Cruzado Novo → Cruzeiro (1990), Cruzeiro → Cruzeiro Real (1993),
  Cruzeiro Real → Real (1994)
- Germany: DDR Mark → DEM (1990, 1:1 for wages, 2:1 for savings)
- Euro zone entries: each country's entry date and conversion rate

Continuous backtesting time series must be constructed through these events
using the registry, not with gaps or false rate continuity.

### Prohibition on Float for Monetary Values

`float` is forbidden for monetary arithmetic. The failure mode is:

```
float example:
0.1 + 0.2 = 0.30000000000000004  (not 0.3)

In a simulation:
annual_debt_service = loan_balance * float_interest_rate
for year in range(30):
    loan_balance = loan_balance - annual_payment
    # float rounding accumulates
# After 30 years: error of thousands of USD in a million-dollar loan
# After 30 years × 200 countries × 10 relationships: meaningless outputs
```

This is not theoretical. It is the reason Python's `decimal` module exists.

---

## Data Provenance Requirements

Every dataset used in WorldSim must have a documented `SourceRegistration`
before its data can be used in simulation:

```python
@dataclass
class SourceRegistration:
    source_id: str                   # unique, stable identifier
    name: str                        # human-readable dataset name
    provider: str                    # institution publishing the data
    dataset_name: str                # specific dataset within provider
    version: str                     # version or release date
    permanent_url: str               # DOI preferred, stable URL required
    access_date: date                # when we accessed this version
    license: str                     # license terms; can we redistribute?
    coverage_start: date
    coverage_end: date | None        # None for ongoing series
    coverage_countries: list[str]    # ISO 3166-1 alpha-3 list; [] for global
    quality_tier: int                # 1-5; see Data Quality Tier System
    simulation_variables: list[str]  # which simulation attributes this feeds
    known_limitations: str           # honest documentation of gaps and caveats
```

No ingestion pipeline may write to the simulation database without a registered
`source_id`.

---

## Data Quality Tier System

Confidence intervals in simulation outputs widen as input data tier decreases.
This relationship is quantified, not qualitative — a Tier 4 input produces
wider output uncertainty bands than a Tier 2 input by a documented multiplier.

### Tier 1 — Primary Official Statistics

**Definition:** Directly measured data published by authoritative primary
sources with published methodology.

**Sources:** World Bank Open Data, IMF Balance of Payments Statistics,
UN Population Division, national statistical offices of the country in
question, BIS International Banking Statistics, WHO Global Health Observatory.

**Weight in simulation:** Full weight.

**Example:** World Bank GDP (current USD) for a year with national accounts
finalized and audited.

### Tier 2 — Derived Official Statistics

**Definition:** Calculated from Tier 1 sources by reputable institutions
using documented, reproducible methodology.

**Sources:** OECD calculations from national accounts, World Bank derived
indicators (e.g., GNI per capita from GDP and population), IMF article IV
consultation estimates.

**Weight in simulation:** Full weight.

**Requirement:** Source chain must be documented — which Tier 1 sources
were combined, how.

### Tier 3 — Research Estimates

**Definition:** Published estimates from peer-reviewed academic sources or
major research institutions with documented methodology and uncertainty ranges.

**Sources:** Tax Justice Network illicit flow estimates, UNCTAD FDI
analysis, GDELT project coded events, Uppsala Conflict Data Program.

**Weight in simulation:** Weighted by stated uncertainty. Flagged in outputs.

### Tier 4 — Model Estimates

**Definition:** Values produced by other simulation models, including
WorldSim's own projections. Forward projections. Extrapolations beyond
source coverage.

**Weight in simulation:** Used only where no Tier 1-3 source exists.
Explicitly flagged as estimated. Uncertainty bands are wide.

**Prohibition:** WorldSim outputs from one scenario run may not be used as
Tier 4 inputs to a different scenario run without explicit documentation
and user notification. This prevents circular reasoning from being laundered
through the tool.

### Tier 5 — Gap-Filled Values

**Definition:** Values produced by interpolation, extrapolation, or regional
averaging where no source data exists.

**Weight in simulation:** Last resort only. Excluded from high-stakes outputs
(IMF loan evaluation, privatization assessment, financial attack detection)
unless no alternative exists, in which case the gap-filled proportion is
prominently displayed.

---

## Data Lineage Tracking

Every transformation from raw source data to simulation attribute is documented
as structured metadata, not free text.

```python
@dataclass
class TransformationStep:
    step_type: TransformationType
    description: str
    input_unit: Unit | None
    output_unit: Unit | None
    parameters: dict[str, Any]       # conversion factors, interpolation method, etc.
    applied_at: datetime

class TransformationType(Enum):
    UNIT_CONVERSION = "unit_conversion"
    CURRENCY_CONVERSION = "currency_conversion"
    AGGREGATION = "aggregation"
    INTERPOLATION = "interpolation"
    GAP_FILL = "gap_fill"
    SEASONAL_ADJUSTMENT = "seasonal_adjustment"
    DEFLATION = "deflation"          # nominal to real
    PPP_CONVERSION = "ppp_conversion"

@dataclass
class DataLineage:
    source_registry_id: str
    transformations: list[TransformationStep]
    output_attribute: str            # which simulation variable this feeds
```

### Output Attribution

Simulation outputs shown to users must display:
1. Which data sources produced this output (source names + tiers)
2. The confidence tier of the output
3. The key assumptions in the calculation
4. A link to the methodology ADR
5. An explicit statement: **"This output is a structured reasoning tool, not
   a prediction. Treat it as a distribution, not a fact."**

---

## Backtesting Integrity Rules

A simulation cannot be validated by running it forward from a baseline seeded
with data that was not available at the baseline date. This is not a minor
methodological concern — it invalidates the backtesting discipline entirely.

### Vintage Dating Requirement

When running a historical scenario with start date T:
- Only data **published on or before date T** may be used to seed the scenario
- This requires storing not just values but the date each value was **first
  published** (`vintage_date` field on all historical data)
- Revised figures published after T are explicitly prohibited as backtesting
  seed data

### Sources with Vintage Retrieval Support

| Source | Vintage Support | Access Method |
|---|---|---|
| IMF World Economic Outlook | Yes — WEO archive available | `imf.org/en/Publications/WEO/weo-database/` |
| World Bank WDI | Partial — some historical snapshots | World Bank Data API with date filtering |
| FRED (Federal Reserve) | Yes — full vintage system | `api.stlouisfed.org/fred/release/dates` |
| BIS Statistics | Partial | Contact BIS; not all series have vintage |

### Sources Without Vintage Retrieval

For sources that do not support vintage retrieval, use the following handling:
1. Document that vintage dating is not available for this source
2. Use the earliest available release as the backtesting seed and flag this limitation
3. For high-stakes backtesting cases, seek an alternative Tier 1/2 source with
   vintage support before proceeding

---

## Gap-Filling Standards

### Permissible Methods, in Order of Preference

1. **Temporal interpolation** — for short gaps (≤3 time periods) in a
   continuous series where the values before and after are known. Linear
   interpolation for economic series; log-linear for ratio series.
2. **Regional or income-group averages** — for cross-sectional gaps where
   comparable countries have data. The comparison group must be documented.
3. **Model-based estimation** — as last resort. The model used, its inputs,
   and its uncertainty range must be documented.

### Gap-Fill Flags

Every gap-filled value carries:
- `gap_filled: True` flag
- `gap_fill_method: str` — the method used
- `confidence_tier: 5` — always Tier 5 regardless of method

These flags are visible in output attribution. They are never hidden.

---

## Source Registry Schema

The machine-readable source registry lives in `backend/app/data/source_registry.py`.
Every data ingestion pipeline registers its source before writing data.

Minimum registry entries required at Milestone 1:
- World Bank WDI GDP data
- World Bank WDI population data
- IMF WEO GDP and fiscal data
- UN Population Division demographic data
- Natural Earth country boundary data (Milestone 2 prerequisite)

---

## Political and Territorial Nomenclature Standards

WorldSim presents territorial and political designations transparently, without
silently asserting contested positions. This is both a methodological standard
and an ethical commitment.

### Primary Standard: ISO 3166-1 alpha-3

All country codes throughout the codebase use ISO 3166-1 alpha-3. This is
non-negotiable. No numeric codes, no alpha-2 codes in internal identifiers.

```python
# Correct
entity_id = "GRC"
entity_id = "BOL"

# Forbidden in internal identifiers
entity_id = "GR"   # alpha-2
entity_id = 300    # numeric
```

Where ISO 3166-1 is silent or ambiguous:
- Economic entities: follow IMF country list
- Political designations: follow UN Secretariat terminology

### Historical Entities: ISO 3166-3

Dissolved entities have ISO 3166-3 codes and must be used for backtesting
scenarios set during their existence:

| Entity | ISO 3166-3 | Period | Successor(s) |
|---|---|---|---|
| Soviet Union | SUHH | -1991 | RUS, UKR, BLR, KAZ, UZB, TKM, KGZ, TJK, ARM, AZE, GEO, MDA, LVA, LTU, EST |
| Czechoslovakia | CSHH | -1993 | CZE, SVK |
| Yugoslavia | YUCS | -2003 | SVN, HRV, BIH, MKD, FRY (SRB+MNE), then MNE, SRB, XKX |
| German Democratic Republic | DDDE | -1990 | Merged into DEU |
| South Vietnam | VNVN | -1975 | Merged into VNM |

### Subnational Divisions: ISO 3166-2

Subnational entities use ISO 3166-2 codes as their `id` field.

### Geospatial Boundary Data: Natural Earth

Primary geospatial boundary source: [Natural Earth](https://www.naturalearthdata.com/)
at 1:10m scale. Natural Earth explicitly marks disputed areas rather than
silently asserting a resolution — this aligns with WorldSim's transparency
principle.

### Disputed Territory Framework

```python
@dataclass
class TerritorialDesignation:
    entity_id: str                          # ISO code for administrative entity
    de_facto_admin: str                     # who actually administers
    de_jure_claimants: list[str]            # who claims sovereignty
    dispute_status: DisputeStatus
    effective_date: date                    # when this designation became effective
    source: str                             # UN resolution, ICJ decision, etc.
    display_note: str                       # shown to users: explains the dispute

class DisputeStatus(Enum):
    UNDISPUTED = "undisputed"
    DISPUTED = "disputed"
    CONTESTED_ADMIN = "contested_admin"     # disputed who administers
    CONTESTED_SOVEREIGNTY = "contested_sovereignty"  # administered, sovereignty disputed
```

Scenario-date-aware boundary selection is applied in all historical scenarios —
the boundary that was effective at the scenario date, not the current boundary.

### High-Risk Specific Cases

These cases require special handling and may never be left to default behavior:

**Taiwan (TWN)**
- ISO 3166-1 alpha-3: TWN
- De facto independent government since 1949; not a UN member state
- PRC claims sovereignty; Taiwan's government claims to be the Republic of China
- Internal code: TWN
- Display: "Taiwan" in most contexts; note displayed: "Taiwan's international
  status is disputed. WorldSim follows ISO 3166-1 for internal identifiers
  and presents this as a separate economic entity for simulation purposes,
  which does not constitute a political position on sovereignty."
- Economic data: treated as a separate entity; sourced from ADB, IMF (Article
  IV consultations), Taiwan's own statistics

**Palestine (PSE)**
- ISO 3166-1 alpha-3: PSE (Palestinian Territory, Occupied)
- Includes West Bank and Gaza Strip as a single administrative entity in
  most international datasets, despite distinct governance
- UN non-member observer state since 2012
- Display: "State of Palestine" (self-designation) with note on administrative
  complexity where scenario-relevant
- Economic data: World Bank WDI, PCBS (Palestinian Central Bureau of Statistics)

**Kosovo (XKX)**
- Not an ISO 3166-1 member; uses XKX (user-assigned code)
- Declared independence 2008; recognized by ~100 states; not recognized by
  Russia, China, Serbia, five EU members
- IMF member since 2009; World Bank member since 2009
- Internal code: XKX
- Display: "Kosovo" with note on recognition status where scenario-relevant
- Economic data: World Bank WDI, IMF Article IV, Kosovo Statistics Agency

**Western Sahara (ESH)**
- ISO 3166-1 alpha-3: ESH
- Administered primarily by Morocco; Sahrawi Arab Democratic Republic controls
  eastern portions
- UN lists as a Non-Self-Governing Territory
- Display: "Western Sahara" with note: "Non-Self-Governing Territory. Majority
  administered by Morocco; eastern territory by the Sahrawi Arab Democratic
  Republic."

**Crimea**
- Administered by Russia since 2014; internationally recognized as Ukraine
- Internal handling: Ukraine (UKR) national-level data with administrative
  change noted in entity metadata from 2014
- No separate Crimea entity — this would implicitly endorse annexation
- Subnational scenario work uses UA-43 (Autonomous Republic of Crimea,
  ISO 3166-2) with explicit status note

**China/Taiwan Economic Separation**
- CHN data excludes Taiwan, Hong Kong (HKG), and Macao (MAC) throughout
- Each is a separate simulation entity with its own data sources
- Ensure no World Bank or IMF aggregates silently include or exclude these
  without documentation

### Display Principle

- Non-disputed cases: use the name the entity uses in its own official
  communications (i.e., "Bolivia" not "Plurinational State of Bolivia" in
  short form, but use the full official name in formal contexts)
- Disputed cases: use the most internationally neutral designation, with
  an explicit dispute note visible to users
- Never silently choose one claimant's terminology

### Historical Name Changes Registry

```python
HISTORICAL_NAME_CHANGES = [
    # (historical_name, iso_code, name_effective_from, name_effective_to, notes)
    ("Rhodesia", "ZWE", date(1965, 11, 11), date(1980, 4, 18), "UDI period"),
    ("Zimbabwe Rhodesia", "ZWE", date(1979, 6, 1), date(1980, 4, 18), "Transition period"),
    ("Zaire", "COD", date(1971, 10, 27), date(1997, 5, 17), "Mobutu period"),
    ("Ceylon", "LKA", date(1815, 3, 2), date(1972, 5, 22), "British colonial and independence period"),
    ("Persia", "IRN", None, date(1935, 3, 21), "International usage before Iranian government request"),
    ("Burma", "MMR", None, date(1989, 6, 18), "Name changed by military government; 'Myanmar' used by UN; 'Burma' still used by some governments"),
    ("Swaziland", "SWZ", None, date(2018, 4, 19), "Renamed to Kingdom of Eswatini"),
    ("Byelorussia", "BLR", None, date(1991, 8, 25), "Soviet Socialist Republic to Republic of Belarus"),
    ("Upper Volta", "BFA", None, date(1984, 8, 4), "Renamed to Burkina Faso"),
    ("Dahomey", "BEN", None, date(1975, 11, 30), "Renamed to Benin"),
    ("Dutch Guiana", "SUR", None, date(1975, 11, 25), "Independence as Suriname"),
]
```

### Governing Principle

WorldSim follows internationally recognized standards bodies and presents
disputed cases transparently without taking political positions that are not
ours to take. Where standards are silent or disputed, we document our choice
and the rationale explicitly. This principle is the rationale for every specific
decision in this section and is stated here explicitly so that no individual
choice appears arbitrary.

---

## Known Limitations

This section documents formally acknowledged limitations in WorldSim's data
standards and confidence tier system. Each limitation has a canonical
identifier, a disclosure text hardcoded in the relevant modules, and a
remediation plan tracked in GitHub.

---

### Known Limitation IA-1: Projection Horizon Confidence

**What the limitation is**

`confidence_tier` does not degrade with projection horizon distance. A
`Quantity` derived from a Tier 1 historical observation retains Tier 1
confidence regardless of how far forward in time it is projected. A 30-year
forward projection carries the same confidence tier as the historical
observation it was derived from, which overstates reliability for long-horizon
projections.

**Why it exists**

Time-horizon confidence degradation requires a calibration infrastructure —
specifically, a mapping from (horizon distance, variable type, model lineage)
to a tier penalty — that has not yet been implemented. Until that
infrastructure exists, applying automatic degradation would introduce
arbitrary penalties with no empirical basis, which would be worse than the
current known limitation. The limitation is therefore documented and disclosed
rather than patched with an uncalibrated heuristic.

**Canonical disclosure text**

The following string is defined as `IA1_CANONICAL_PHRASE` in
`backend/app/simulation/repositories/quantity_serde.py`. This exact text
must appear verbatim in every `ia1_disclosure` field. It must not be
paraphrased or abbreviated:

```
Forward projections carry inherited confidence tier without time-horizon
degradation. Confidence tiers reflect data quality at observation date, not
projection reliability. See DATA_STANDARDS.md Known Limitation IA-1.
```

`validate_ia1_disclosure()` in `quantity_serde.py` enforces that
`ia1_disclosure` is non-empty and non-whitespace at every snapshot write
path. The database `NOT NULL` constraint prevents NULL. Unit tests assert
that `IA1_CANONICAL_PHRASE` appears verbatim in snapshot output.

**Where it appears**

- `scenario_state_snapshots.ia1_disclosure` — populated on every snapshot
  write by the scenario runner. Present in all M3 and later scenario outputs.
- `MultiFrameworkOutput.ia1_disclosure` (Milestone 4) — required
  non-nullable constructor argument on every `MultiFrameworkOutput` instance
  per ADR-005 Decision 2. Carries the same canonical phrase.

**Remediation plan**

Issue #69, Milestone 4. Implement time-horizon confidence degradation as a
calibration table keyed by `(horizon_steps, variable_type)`. When implemented,
forward projection `confidence_tier` will be computed as
`max(source_tier, horizon_penalty_tier)`, where `horizon_penalty_tier` is
drawn from the calibration table. `IA1_CANONICAL_PHRASE` will be retired and
replaced by output that reflects actual calibrated confidence. The
`ia1_disclosure` field will remain but its content will shift from a blanket
limitation notice to a calibration provenance statement.
