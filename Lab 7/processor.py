import math

MENU_PRICES = {
    "LAT": 4.50,
    "CAP": 4.00,
    "ESP": 3.00,
    "AME": 3.50,
    "MOC": 5.00,  # fixed: was "MOc", which could never match an upper-cased prefix
}


def lookup_drink_code(code_string):
    """Return the base price for a drink code, or None if the input is
    not a string or the code is not on the menu."""
    if not isinstance(code_string, str):
        return None
    code_prefix = code_string.strip().upper()[:3]
    return MENU_PRICES.get(code_prefix)


def calculate_average_shot_cost(pricing_csv):
    """Return the average of a comma-separated list of prices, or None if the
    input is not a string, is empty, or contains a non-numeric / non-finite
    / negative value."""
    if not isinstance(pricing_csv, str) or not pricing_csv.strip():
        return None
    prices = []
    for part in pricing_csv.split(','):
        try:
            value = float(part)
        except (ValueError, OverflowError):
            return None
        if not math.isfinite(value) or value < 0:  # rejects nan, inf, negatives
            return None
        prices.append(value)
    try:
        average = sum(prices) / len(prices)  # prices is never empty here
    except OverflowError:
        return None
    return average if math.isfinite(average) else None


def parse_order_modifiers(order_spec):
    """Parse 'key:value;key:value' into a dict. Malformed items (no colon,
    empty key) are skipped. Non-string input gives an empty dict."""
    modifier_dict = {}
    if not isinstance(order_spec, str):
        return modifier_dict
    for item in order_spec.split(';'):
        if ':' not in item:
            continue
        key, value = item.split(':', 1)  # value may itself contain ':'
        key = key.strip()
        if not key:
            continue
        modifier_dict[key] = value.strip()
    return modifier_dict


def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    price = lookup_drink_code(drink_input)
    if price is None:
        print("Invalid or unknown drink code.")
    else:
        print("Base Price: $", price)

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    avg_price = calculate_average_shot_cost(shots_input)
    if avg_price is None:
        print("Invalid shot price list.")
    else:
        print("Average Shot Price: $", avg_price)

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    mods = parse_order_modifiers(spec_input)
    print("Parsed Modifiers:", mods)


if __name__ == "__main__":
    main()
