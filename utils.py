def to_float(value: str, default: float | None = None) -> float | None:
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

VOLTAGE_HIGH = 4.2
VOLTAGE_LOW = 3.0

