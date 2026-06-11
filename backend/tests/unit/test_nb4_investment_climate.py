"""Unit tests for NB-4 — investment climate state variables (Issue #34).

Covers: sovereign_risk_premium, fdi_stock_pct_gdp, portfolio_flow_velocity,
credit_rating_score in both the Greece 2010 and Argentina 2001 demo fixtures.
Validates values, units, attribute_types, variable_types, and confidence tiers
against the historical sources cited in each fixture.

Greece 2010 sources:
  ECB_SDW_GRC_SPREAD_2010     — ECB Statistical Data Warehouse 10Y spread
  UNCTAD_FDI_STATS_GRC_2010   — UNCTAD World Investment Report 2010
  IMF_BOP_GRC_2010            — IMF Balance of Payments Statistics 2010
  SP_SOVEREIGN_RATINGS_GRC_2010 — S&P sovereign rating January 2010 (BBB+→55)

Argentina 2001 sources:
  JPMORGAN_EMBI_ARG_2000      — JP Morgan EMBI+ spread December 2000
  UNCTAD_FDI_STATS_ARG_2000   — UNCTAD World Investment Report 2001
  INDEC_BOP_ARG_2000          — INDEC Balance of Payments 2000
  SP_SOVEREIGN_RATINGS_ARG_2001 — S&P sovereign rating January 2001 (BB→38)
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from tests.fixtures.argentina_2001_2002_scenario import build_argentina_scenario
from tests.fixtures.greece_2010_scenario import build_greece_scenario

# ---------------------------------------------------------------------------
# Greece 2010 — investment climate initial attributes
# ---------------------------------------------------------------------------

class TestGreeceInvestmentClimate:
    """Investment climate state variables seeded for Greece 2010 (NB-4, Issue #34)."""

    def _grc_attrs(self) -> dict:  # type: ignore[type-arg]
        req = build_greece_scenario()
        return req.configuration.initial_attributes["GRC"]  # type: ignore[index]

    def test_sovereign_risk_premium_present(self) -> None:
        assert "sovereign_risk_premium" in self._grc_attrs()

    def test_sovereign_risk_premium_value(self) -> None:
        attr = self._grc_attrs()["sovereign_risk_premium"]
        assert Decimal(attr.value) == pytest.approx(Decimal("0.030"))

    def test_sovereign_risk_premium_unit(self) -> None:
        assert self._grc_attrs()["sovereign_risk_premium"].unit == "ratio"

    def test_sovereign_risk_premium_attribute_type(self) -> None:
        assert self._grc_attrs()["sovereign_risk_premium"].attribute_type == "rate"

    def test_sovereign_risk_premium_variable_type(self) -> None:
        assert self._grc_attrs()["sovereign_risk_premium"].variable_type == "ratio"

    def test_sovereign_risk_premium_confidence_tier(self) -> None:
        assert self._grc_attrs()["sovereign_risk_premium"].confidence_tier == 2

    def test_sovereign_risk_premium_source(self) -> None:
        source = self._grc_attrs()["sovereign_risk_premium"].source_registry_id
        assert source == "ECB_SDW_GRC_SPREAD_2010"

    def test_sovereign_risk_premium_framework(self) -> None:
        assert self._grc_attrs()["sovereign_risk_premium"].measurement_framework == "financial"

    def test_fdi_stock_pct_gdp_present(self) -> None:
        assert "fdi_stock_pct_gdp" in self._grc_attrs()

    def test_fdi_stock_pct_gdp_value(self) -> None:
        attr = self._grc_attrs()["fdi_stock_pct_gdp"]
        assert Decimal(attr.value) == pytest.approx(Decimal("0.105"))

    def test_fdi_stock_pct_gdp_attribute_type(self) -> None:
        assert self._grc_attrs()["fdi_stock_pct_gdp"].attribute_type == "stock"

    def test_fdi_stock_pct_gdp_variable_type(self) -> None:
        assert self._grc_attrs()["fdi_stock_pct_gdp"].variable_type == "stock"

    def test_fdi_stock_pct_gdp_confidence_tier(self) -> None:
        assert self._grc_attrs()["fdi_stock_pct_gdp"].confidence_tier == 2

    def test_portfolio_flow_velocity_present(self) -> None:
        assert "portfolio_flow_velocity" in self._grc_attrs()

    def test_portfolio_flow_velocity_value(self) -> None:
        attr = self._grc_attrs()["portfolio_flow_velocity"]
        assert Decimal(attr.value) == pytest.approx(Decimal("-0.080"))

    def test_portfolio_flow_velocity_attribute_type(self) -> None:
        assert self._grc_attrs()["portfolio_flow_velocity"].attribute_type == "flow"

    def test_portfolio_flow_velocity_negative(self) -> None:
        # Capital outflow: portfolio_flow_velocity must be negative for Greece 2010.
        assert Decimal(self._grc_attrs()["portfolio_flow_velocity"].value) < 0

    def test_credit_rating_score_present(self) -> None:
        assert "credit_rating_score" in self._grc_attrs()

    def test_credit_rating_score_value(self) -> None:
        attr = self._grc_attrs()["credit_rating_score"]
        assert Decimal(attr.value) == pytest.approx(Decimal("55.0"))

    def test_credit_rating_score_attribute_type(self) -> None:
        assert self._grc_attrs()["credit_rating_score"].attribute_type == "structural_index"

    def test_credit_rating_score_unit(self) -> None:
        assert self._grc_attrs()["credit_rating_score"].unit == "index_0_100"

    def test_credit_rating_score_confidence_tier(self) -> None:
        # Confidence tier 1: direct observation from rating agency announcement.
        assert self._grc_attrs()["credit_rating_score"].confidence_tier == 1


# ---------------------------------------------------------------------------
# Argentina 2001 — investment climate initial attributes
# ---------------------------------------------------------------------------

class TestArgentinaInvestmentClimate:
    """Investment climate state variables seeded for Argentina 2001 (NB-4, Issue #34)."""

    def _arg_attrs(self) -> dict:  # type: ignore[type-arg]
        req = build_argentina_scenario()
        return req.configuration.initial_attributes["ARG"]  # type: ignore[index]

    def test_sovereign_risk_premium_present(self) -> None:
        assert "sovereign_risk_premium" in self._arg_attrs()

    def test_sovereign_risk_premium_value(self) -> None:
        attr = self._arg_attrs()["sovereign_risk_premium"]
        assert Decimal(attr.value) == pytest.approx(Decimal("0.075"))

    def test_sovereign_risk_premium_attribute_type(self) -> None:
        assert self._arg_attrs()["sovereign_risk_premium"].attribute_type == "rate"

    def test_sovereign_risk_premium_higher_than_greece(self) -> None:
        # Argentina 2001 spread (~750bps) must exceed Greece 2010 spread (~300bps).
        arg_spread = Decimal(self._arg_attrs()["sovereign_risk_premium"].value)
        grc_attrs = build_greece_scenario().configuration.initial_attributes["GRC"]  # type: ignore[index]
        grc_spread = Decimal(grc_attrs["sovereign_risk_premium"].value)
        assert arg_spread > grc_spread

    def test_fdi_stock_pct_gdp_present(self) -> None:
        assert "fdi_stock_pct_gdp" in self._arg_attrs()

    def test_fdi_stock_pct_gdp_value(self) -> None:
        attr = self._arg_attrs()["fdi_stock_pct_gdp"]
        assert Decimal(attr.value) == pytest.approx(Decimal("0.251"))

    def test_fdi_stock_pct_gdp_attribute_type(self) -> None:
        assert self._arg_attrs()["fdi_stock_pct_gdp"].attribute_type == "stock"

    def test_portfolio_flow_velocity_present(self) -> None:
        assert "portfolio_flow_velocity" in self._arg_attrs()

    def test_portfolio_flow_velocity_value(self) -> None:
        attr = self._arg_attrs()["portfolio_flow_velocity"]
        assert Decimal(attr.value) == pytest.approx(Decimal("-0.045"))

    def test_portfolio_flow_velocity_attribute_type(self) -> None:
        assert self._arg_attrs()["portfolio_flow_velocity"].attribute_type == "flow"

    def test_portfolio_flow_velocity_negative(self) -> None:
        # Capital outflow: portfolio_flow_velocity must be negative for Argentina 2001.
        assert Decimal(self._arg_attrs()["portfolio_flow_velocity"].value) < 0

    def test_credit_rating_score_present(self) -> None:
        assert "credit_rating_score" in self._arg_attrs()

    def test_credit_rating_score_value(self) -> None:
        attr = self._arg_attrs()["credit_rating_score"]
        assert Decimal(attr.value) == pytest.approx(Decimal("38.0"))

    def test_credit_rating_score_attribute_type(self) -> None:
        assert self._arg_attrs()["credit_rating_score"].attribute_type == "structural_index"

    def test_credit_rating_score_lower_than_greece(self) -> None:
        # Argentina BB (38) must score lower than Greece BBB+ (55).
        arg_score = Decimal(self._arg_attrs()["credit_rating_score"].value)
        grc_attrs = build_greece_scenario().configuration.initial_attributes["GRC"]  # type: ignore[index]
        grc_score = Decimal(grc_attrs["credit_rating_score"].value)
        assert arg_score < grc_score


# ---------------------------------------------------------------------------
# Cross-fixture consistency
# ---------------------------------------------------------------------------

_INVESTMENT_CLIMATE_KEYS = (
    "sovereign_risk_premium",
    "fdi_stock_pct_gdp",
    "portfolio_flow_velocity",
    "credit_rating_score",
)


class TestInvestmentClimateConsistency:
    """Cross-fixture consistency checks for investment climate variables (NB-4)."""

    def test_all_four_variables_in_grc(self) -> None:
        attrs = build_greece_scenario().configuration.initial_attributes["GRC"]  # type: ignore[index]
        for key in _INVESTMENT_CLIMATE_KEYS:
            assert key in attrs, f"Missing {key} in GRC initial_attributes"

    def test_all_four_variables_in_arg(self) -> None:
        attrs = build_argentina_scenario().configuration.initial_attributes["ARG"]  # type: ignore[index]
        for key in _INVESTMENT_CLIMATE_KEYS:
            assert key in attrs, f"Missing {key} in ARG initial_attributes"

    def test_attribute_types_consistent_across_fixtures(self) -> None:
        grc = build_greece_scenario().configuration.initial_attributes["GRC"]  # type: ignore[index]
        arg = build_argentina_scenario().configuration.initial_attributes["ARG"]  # type: ignore[index]
        for key in _INVESTMENT_CLIMATE_KEYS:
            grc_type = grc[key].attribute_type
            arg_type = arg[key].attribute_type
            assert grc_type == arg_type, (
                f"attribute_type mismatch for {key}: GRC={grc_type} ARG={arg_type}"
            )

    def test_measurement_framework_financial_all_vars(self) -> None:
        for build_fn, entity in [
            (build_greece_scenario, "GRC"),
            (build_argentina_scenario, "ARG"),
        ]:
            attrs = build_fn().configuration.initial_attributes[entity]  # type: ignore[index]
            for key in _INVESTMENT_CLIMATE_KEYS:
                assert attrs[key].measurement_framework == "financial", (
                    f"{entity}.{key}.measurement_framework should be 'financial'"
                )
