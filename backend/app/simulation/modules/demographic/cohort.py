"""Cohort segmentation axes and CohortSpec — ADR-005 Decision 1."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class IncomeQuintile(int, Enum):
    Q1 = 1  # bottom 20%
    Q2 = 2
    Q3 = 3
    Q4 = 4
    Q5 = 5  # top 20%


class AgeBand(str, Enum):
    AGE_0_14    = "0-14"
    AGE_15_24   = "15-24"
    AGE_25_54   = "25-54"
    AGE_55_64   = "55-64"
    AGE_65_PLUS = "65+"


class EmploymentSector(str, Enum):
    FORMAL      = "FORMAL"
    INFORMAL    = "INFORMAL"
    AGRICULTURE = "AGRICULTURE"
    UNEMPLOYED  = "UNEMPLOYED"


@dataclass(frozen=True)
class CohortSpec:
    income_quintile: IncomeQuintile
    age_band: AgeBand
    employment_sector: EmploymentSector

    def entity_id(self, country_iso3: str) -> str:
        """Canonical cohort entity ID.

        Format: {ISO3}:CHT:{quintile}-{age_band}-{sector}
        Example: GRC:CHT:1-25-54-FORMAL
        """
        return (
            f"{country_iso3}:CHT:"
            f"{self.income_quintile.value}"
            f"-{self.age_band.value}"
            f"-{self.employment_sector.value}"
        )


def generate_cohort_specs() -> list[CohortSpec]:
    """Generate all 5 × 5 × 4 = 100 CohortSpec instances."""
    return [
        CohortSpec(q, a, s)
        for q in IncomeQuintile
        for a in AgeBand
        for s in EmploymentSector
    ]
