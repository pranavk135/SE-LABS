"""Utility meter tracker: readings, tiered billing, spikes, JSON storage."""
import json
import math
from datetime import datetime

# Shared state: meter_id -> total units (mutated in place, never rebound)
meters = {}
DEFAULT_RATES = (3.5, 5.0, 7.5)
SPIKE_LIMIT = 500


def record_reading(meter_id, units, history=None):
    """Add a reading to a meter and return the reading history list."""
    if history is None:
        history = []
    if not math.isfinite(units) or units < 0:
        raise ValueError("units must be a finite, non-negative number")
    history.append((meter_id, units, str(datetime.now())))
    meters[meter_id] = meters.get(meter_id, 0) + units
    return history


def compute_bill(meter_id, tier_rates):
    """Return the three-tier bill (0-100, 101-300, 301+ units) for a meter."""
    units = meters[meter_id]
    if units <= 100:
        return units * tier_rates[0]
    if units <= 300:
        return 100 * tier_rates[0] + (units - 100) * tier_rates[1]
    return (100 * tier_rates[0] + 200 * tier_rates[1]
            + (units - 300) * tier_rates[2])


def raise_rates(rates, percent):
    """Return a new tuple of tier rates raised by the given percentage."""
    return tuple(rate * (1 + percent / 100) for rate in rates)


def flag_spikes():
    """Return the ids of meters whose total exceeds SPIKE_LIMIT."""
    return [meter_id for meter_id, units in meters.items()
            if units > SPIKE_LIMIT]


def load_meter_data(file="meters.json"):
    """Replace meter data with the contents of a JSON file ({} if unusable)."""
    try:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        data = {}
    meters.clear()
    meters.update(data)


def save_meter_data(file="meters.json"):
    """Write the meter data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(meters, f)


def main():
    """Run the demo."""
    history = []
    record_reading("M-01", 120, history)
    record_reading("M-02", 640, history)
    record_reading("M-03", 0, history)
    try:
        record_reading("M-04", -50, history)
    except ValueError as err:
        print("Rejected reading for M-04:", err)
    print("Readings stored so far:", len(history))
    rates = raise_rates(DEFAULT_RATES, 10)
    print(f"Bill M-01: {compute_bill('M-01', rates):.2f}")
    print(f"Bill M-03: {compute_bill('M-03', rates):.2f}")
    print("Spikes:", flag_spikes())
    prompt = "Extra units for M-01 (Enter for 0): "
    adjustment = input(prompt) or "0"
    try:
        record_reading("M-01", float(adjustment), history)
    except ValueError as err:
        print("Invalid input, ignoring:", err)
    save_meter_data()
    load_meter_data()
    print(f"Bill M-01 after reload: {compute_bill('M-01', rates):.2f}")


if __name__ == "__main__":
    main()
