"""Unit tests for _classify_direction — NM-098 fix (G8).

Verifies that primary_indicator is respected when it names a composite field,
and that the PSP → fin_composite fallback chain is preserved for None / 'psp'.
"""

from decimal import Decimal

from app.harness.mode3_harness import DirectionVerdict, _classify_direction


class TestClassifyDirection:
    def _make_records(self, **kwargs: str) -> list[dict]:
        return [{k: Decimal(v) for k, v in kwargs.items()}]

    def test_hd_composite_primary_indicator_used(self) -> None:
        cf = self._make_records(hd_composite="0.70", fin_composite="0.50")
        bl = self._make_records(hd_composite="0.60", fin_composite="0.50")
        verdict, diffs, _ = _classify_direction(cf, bl, 1, "hd_composite")
        assert diffs == [Decimal("0.10")]
        assert verdict == DirectionVerdict.COUNTER_FACTUAL_BETTER

    def test_fin_composite_primary_indicator_used(self) -> None:
        cf = self._make_records(hd_composite="0.90", fin_composite="0.40")
        bl = self._make_records(hd_composite="0.80", fin_composite="0.55")
        verdict, diffs, _ = _classify_direction(cf, bl, 1, "fin_composite")
        assert diffs == [Decimal("-0.15")]
        assert verdict == DirectionVerdict.BASELINE_BETTER

    def test_eco_composite_primary_indicator_used(self) -> None:
        cf = self._make_records(eco_composite="0.30", fin_composite="0.50")
        bl = self._make_records(eco_composite="0.20", fin_composite="0.50")
        verdict, diffs, _ = _classify_direction(cf, bl, 1, "eco_composite")
        assert diffs == [Decimal("0.10")]
        assert verdict == DirectionVerdict.COUNTER_FACTUAL_BETTER

    def test_gov_composite_primary_indicator_used(self) -> None:
        cf = self._make_records(gov_composite="0.65", fin_composite="0.50")
        bl = self._make_records(gov_composite="0.65", fin_composite="0.50")
        verdict, diffs, _ = _classify_direction(cf, bl, 1, "gov_composite")
        assert diffs == [Decimal("0.00")]
        assert verdict == DirectionVerdict.INDISTINGUISHABLE

    def test_none_primary_indicator_falls_back_to_psp(self) -> None:
        cf = self._make_records(psp="0.05", fin_composite="0.50")
        bl = self._make_records(psp="0.02", fin_composite="0.50")
        _, diffs, _ = _classify_direction(cf, bl, 1, None)
        assert diffs == [Decimal("0.03")]

    def test_none_primary_indicator_falls_back_to_fin_composite_when_no_psp(self) -> None:
        cf = self._make_records(fin_composite="0.60")
        bl = self._make_records(fin_composite="0.40")
        _, diffs, _ = _classify_direction(cf, bl, 1, None)
        assert diffs == [Decimal("0.20")]

    def test_psp_primary_indicator_uses_fallback_chain(self) -> None:
        cf = self._make_records(psp="0.04", hd_composite="0.90")
        bl = self._make_records(psp="0.02", hd_composite="0.50")
        _, diffs, _ = _classify_direction(cf, bl, 1, "psp")
        assert diffs == [Decimal("0.02")]

    def test_composite_field_absent_appends_zero(self) -> None:
        cf = self._make_records(fin_composite="0.50")
        bl = self._make_records(fin_composite="0.40")
        _, diffs, _ = _classify_direction(cf, bl, 1, "hd_composite")
        assert diffs == [Decimal("0")]

    def test_hd_composite_multi_step(self) -> None:
        cf = [
            {"hd_composite": Decimal("0.70")},
            {"hd_composite": Decimal("0.72")},
            {"hd_composite": Decimal("0.74")},
        ]
        bl = [
            {"hd_composite": Decimal("0.60")},
            {"hd_composite": Decimal("0.58")},
            {"hd_composite": Decimal("0.57")},
        ]
        verdict, diffs, first_sig = _classify_direction(cf, bl, 3, "hd_composite")
        assert diffs == [Decimal("0.10"), Decimal("0.14"), Decimal("0.17")]
        assert verdict == DirectionVerdict.COUNTER_FACTUAL_BETTER
        assert first_sig == 1
