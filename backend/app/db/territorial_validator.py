"""
TerritorialValidator — ADR-003 Decision 4.

Hard-gates the ingestion pipeline for the five declared territorial positions
in POLICY.md § Specific Positions. Must be called before any INSERT into
simulation_entities. Raises TerritorialValidationError (batch-collected) if
any feature violates a declared position.

The five positions enforced here:

  TWN — Taiwan: canonical display name "Taiwan". Prohibited names:
        "Taiwan, Province of China", "Chinese Taipei". Entity must not be
        merged with CHN data.

  PSE — Palestine: code PSE. Entity must not be coded as an Israeli
        subnational entity (code prefix "ISR" or any IL-* variant).

  XKX — Kosovo: user-assigned code XKX (no ISO 3166-1 assignment).
        Must not be coded as a Serbian subnational entity (RS-*).

  ESH — Western Sahara: code ESH. Must not be coded as a Moroccan
        entity or territory (MA-*, MAR).

  CRIMEA — Must not appear as a top-level country entity. Modeled within
           Ukraine (UKR) with subnational code UA-43.

See POLICY.md § Territorial and Nomenclature Positions for the full
rationale and display-note text for each case.
"""
from __future__ import annotations

from typing import Any


class TerritorialValidationError(ValueError):
    """Raised when one or more territorial position violations are detected.

    Batch-collected: the validator accumulates all errors across all features
    before raising. The operator sees every violation in a single error rather
    than fixing them one at a time.
    """


# ---------------------------------------------------------------------------
# Canonical positions from POLICY.md
# ---------------------------------------------------------------------------

# Taiwan: names that must never appear on a TWN entity.
# "Taiwan, Province of China" — PRC/UN framing, asserts Chinese sovereignty.
# "Chinese Taipei" — IOC framing, used in contexts where sovereignty is
# deliberately obscured. Neither is acceptable in WorldSim.
_TAIWAN_PROHIBITED_NAMES: frozenset[str] = frozenset({
    "Taiwan, Province of China",
    "Chinese Taipei",
    "Formosa",  # archaic; included defensively
})

# Property keys in Natural Earth features that may carry a display name.
_NE_NAME_KEYS: tuple[str, ...] = (
    "NAME",
    "NAME_LONG",
    "FORMAL_EN",
    "NAME_CIAWF",
    "SOVEREIGNT",
    "ADMIN",
    "BRK_NAME",
)

# Crimea: names that must not appear as a top-level country entity.
# Crimea has no ISO 3166-1 code and must not be modeled as a country.
# Per POLICY.md: modeled within UKR (UA-43) with administrative change note.
_CRIMEA_PROHIBITED_COUNTRY_NAMES: frozenset[str] = frozenset({
    "Crimea",
    "Republic of Crimea",
    "Autonomous Republic of Crimea",
})

# ISO alpha-3 codes that must never be used to identify Palestine.
# PSE is the correct ISO 3166-1 alpha-3 for Palestinian Territory, Occupied.
_PALESTINE_PROHIBITED_CODES: frozenset[str] = frozenset({
    "ISR",   # Israel — Palestine data must not be merged into Israel
    "IL",    # ISO 3166-1 alpha-2 for Israel — wrong code
})

# ISO alpha-3 codes that must never be used to identify Kosovo.
# XKX is the user-assigned code; Kosovo is not in ISO 3166-1.
_KOSOVO_PROHIBITED_CODES: frozenset[str] = frozenset({
    "SRB",   # Serbia — Kosovo must not be merged into Serbia
    "RS",    # ISO 3166-1 alpha-2 for Serbia
})

# ISO alpha-3 codes that must never be used to identify Western Sahara.
_WESTERN_SAHARA_PROHIBITED_CODES: frozenset[str] = frozenset({
    "MAR",   # Morocco — Western Sahara must not be merged into Morocco
    "MA",    # ISO 3166-1 alpha-2 for Morocco
})

# Natural Earth property keys that carry an ISO or ADM code.
_NE_CODE_KEYS: tuple[str, ...] = (
    "ISO_A3",
    "ADM0_A3",
    "ADM0_A3_IS",
    "ADM0_A3_IL",
    "ADM0_A3_UN",
    "ADM0_A3_WB",
    "ISO_A3_EH",
    "WB_A3",
    "BRK_A3",
)


class TerritorialValidator:
    """Validates Natural Earth feature properties against POLICY.md positions.

    Usage:
        validator = TerritorialValidator()
        validator.validate_all([(entity_id, ne_properties), ...])
        # raises TerritorialValidationError with all violations if any found

    The validator is stateless and reusable across loader invocations.
    It carries no external dependencies and requires no database connection.
    All checks are pure Python and run before any INSERT.
    """

    def _collect_names(self, ne_properties: dict[str, Any]) -> list[str]:
        """Return all non-empty name strings from the NE feature properties."""
        return [
            str(ne_properties[k])
            for k in _NE_NAME_KEYS
            if ne_properties.get(k)
        ]

    def _collect_codes(self, ne_properties: dict[str, Any]) -> list[str]:
        """Return all non-empty ISO/ADM codes from the NE feature properties."""
        return [
            str(ne_properties[k]).strip()
            for k in _NE_CODE_KEYS
            if ne_properties.get(k) and str(ne_properties[k]).strip() not in ("-99", "", "-1")
        ]

    def _check_taiwan(
        self, entity_id: str, ne_properties: dict[str, Any]
    ) -> list[str]:
        """Taiwan (TWN) must not carry prohibited display names."""
        if entity_id != "TWN":
            return []
        errors: list[str] = []
        names = self._collect_names(ne_properties)
        for name in names:
            if name in _TAIWAN_PROHIBITED_NAMES:
                errors.append(
                    f"[TWN] Feature for Taiwan carries prohibited name {name!r}. "
                    f"POLICY.md requires display name 'Taiwan'. "
                    f"Prohibited names assert contested sovereignty positions: "
                    f"{sorted(_TAIWAN_PROHIBITED_NAMES)}."
                )
        return errors

    def _check_palestine(
        self, entity_id: str, ne_properties: dict[str, Any]
    ) -> list[str]:
        """Palestine must use code PSE; must not be coded as an Israeli entity."""
        if entity_id != "PSE":
            return []
        errors: list[str] = []
        codes = self._collect_codes(ne_properties)
        for code in codes:
            if code in _PALESTINE_PROHIBITED_CODES:
                errors.append(
                    f"[PSE] Palestine feature carries prohibited code {code!r}. "
                    f"POLICY.md requires ISO code PSE. "
                    f"Palestine data must not be coded as an Israeli entity."
                )
        return errors

    def _check_kosovo(
        self, entity_id: str, ne_properties: dict[str, Any]
    ) -> list[str]:
        """Kosovo must use code XKX; must not be coded as a Serbian entity."""
        if entity_id != "XKX":
            return []
        errors: list[str] = []
        codes = self._collect_codes(ne_properties)
        for code in codes:
            if code in _KOSOVO_PROHIBITED_CODES:
                errors.append(
                    f"[XKX] Kosovo feature carries prohibited code {code!r}. "
                    f"POLICY.md requires user-assigned code XKX. "
                    f"Kosovo must not be coded as a Serbian subnational entity."
                )
        return errors

    def _check_western_sahara(
        self, entity_id: str, ne_properties: dict[str, Any]
    ) -> list[str]:
        """Western Sahara must use code ESH; must not be coded as Moroccan territory."""
        if entity_id != "ESH":
            return []
        errors: list[str] = []
        codes = self._collect_codes(ne_properties)
        for code in codes:
            if code in _WESTERN_SAHARA_PROHIBITED_CODES:
                errors.append(
                    f"[ESH] Western Sahara feature carries prohibited code {code!r}. "
                    f"POLICY.md requires ISO code ESH. "
                    f"Western Sahara must not be coded as Moroccan territory."
                )
        return errors

    def _check_crimea(
        self, entity_id: str, ne_properties: dict[str, Any]
    ) -> list[str]:
        """Crimea must not appear as a top-level country entity.

        POLICY.md: Crimea is modeled within Ukraine (UKR) with administrative
        change noted in entity metadata. No separate Crimea entity is created.
        UA-43 (ISO 3166-2) is acceptable as a subnational entity only.
        """
        names = self._collect_names(ne_properties)
        for name in names:
            if name in _CRIMEA_PROHIBITED_COUNTRY_NAMES:
                return [
                    f"[CRIMEA] Feature {name!r} (entity_id={entity_id!r}) "
                    f"must not appear as a top-level country entity. "
                    f"POLICY.md: Crimea is modeled within Ukraine (UKR, subnational UA-43). "
                    f"UNGA Resolution ES-11/1 (2022) and prior resolutions do not recognise "
                    f"the 2014 annexation."
                ]
        return []

    def validate_entity(
        self,
        entity_id: str,
        ne_properties: dict[str, Any],
    ) -> list[str]:
        """Return a list of violation messages for a single feature.

        Returns an empty list if the feature passes all checks.
        Does not raise — callers use validate_all() to batch-collect and raise.

        Args:
            entity_id: The ISO 3166-1 alpha-3 code (or user-assigned code)
                for this entity. Derived from the Natural Earth ISO_A3 field
                before calling.
            ne_properties: The raw properties dict from the Natural Earth
                GeoJSON feature.

        Returns:
            A list of human-readable violation messages. Empty if valid.
        """
        return (
            self._check_taiwan(entity_id, ne_properties)
            + self._check_palestine(entity_id, ne_properties)
            + self._check_kosovo(entity_id, ne_properties)
            + self._check_western_sahara(entity_id, ne_properties)
            + self._check_crimea(entity_id, ne_properties)
        )

    def validate_all(
        self,
        entities: list[tuple[str, dict[str, Any]]],
    ) -> None:
        """Validate a batch of (entity_id, ne_properties) pairs.

        Collects all violations across all features before raising, so the
        operator can fix every violation in one pass rather than one at a time.

        Args:
            entities: List of (entity_id, ne_properties) tuples to validate.

        Raises:
            TerritorialValidationError: If any feature fails validation.
                The message includes all violations with their entity_ids.
        """
        all_errors: list[str] = []
        for entity_id, props in entities:
            violations = self.validate_entity(entity_id, props)
            all_errors.extend(violations)

        if all_errors:
            count = len(all_errors)
            bullet_list = "\n".join(f"  • {e}" for e in all_errors)
            raise TerritorialValidationError(
                f"{count} territorial validation violation(s) detected. "
                f"Pipeline halted — no records written.\n{bullet_list}\n\n"
                f"See POLICY.md § Territorial and Nomenclature Positions "
                f"and DATA_STANDARDS.md § Disputed Territory Framework."
            )
