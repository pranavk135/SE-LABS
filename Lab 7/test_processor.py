import math

from hypothesis import given, strategies as st
from processor import lookup_drink_code, calculate_average_shot_cost, parse_order_modifiers

MENU = {"LAT": 4.50, "CAP": 4.00, "ESP": 3.00, "AME": 3.50, "MOC": 5.00}


# ---------------------------------------------------------------------------
# 1. Crash tests: each function must never raise, whatever it is given.
# ---------------------------------------------------------------------------
@given(st.text() | st.none())
def test_lookup_drink_code_no_crash(s):
    try:
        lookup_drink_code(s)
    except Exception as e:
        assert False, f"lookup_drink_code crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_calculate_average_shot_cost_safe(s):
    try:
        calculate_average_shot_cost(s)
    except Exception as e:
        assert False, f"calculate_average_shot_cost crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_parse_order_modifiers_safe(s):
    try:
        parse_order_modifiers(s)
    except Exception as e:
        assert False, f"parse_order_modifiers crashed with: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# 2. Property tests: the functions must also return *correct* results.
# ---------------------------------------------------------------------------
@given(st.sampled_from(sorted(MENU)), st.text(max_size=5), st.booleans())
def test_lookup_known_codes_return_price(code, suffix, lower):
    s = (code.lower() if lower else code) + suffix
    assert lookup_drink_code(s) == MENU[code]


@given(st.text())
def test_lookup_unknown_code_returns_none(s):
    if s.strip().upper()[:3] not in MENU:
        assert lookup_drink_code(s) is None


@given(st.lists(st.floats(min_value=0, max_value=1e6, allow_nan=False), min_size=1, max_size=20))
def test_average_of_valid_prices_is_within_bounds(prices):
    csv = ",".join(repr(p) for p in prices)
    avg = calculate_average_shot_cost(csv)
    assert avg is not None and math.isfinite(avg)
    assert min(prices) - 1e-6 <= avg <= max(prices) + 1e-6


@given(st.sampled_from(["", " ", ",", ",,", "abc", "1,abc", "nan", "inf", "-inf", "1,nan"]))
def test_average_rejects_invalid_csv(s):
    assert calculate_average_shot_cost(s) is None


@given(
    st.dictionaries(
        st.text(alphabet=st.characters(blacklist_characters=":;", blacklist_categories=("Cs", "Z", "C")), min_size=1),
        st.text(alphabet=st.characters(blacklist_characters=";", blacklist_categories=("Cs", "Z", "C")), min_size=0),
    )
)
def test_parse_round_trips_well_formed_specs(d):
    spec = ";".join(f"{k}:{v}" for k, v in d.items())
    assert parse_order_modifiers(spec) == d


@given(st.sampled_from(["", ";", "milk", "milk:", ":oat", "a:b;;c:d", "milk:oat;broken"]))
def test_parse_malformed_specs_return_dict(s):
    assert isinstance(parse_order_modifiers(s), dict)
