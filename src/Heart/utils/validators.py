"""Server-side input validation for prediction form fields."""

from src.Heart.constants import VALIDATION_RULES


class ValidationError(Exception):
    def __init__(self, errors: dict):
        self.errors = errors
        super().__init__("Validation failed")


def validate_patient_input(form_data: dict) -> dict:
    """Validate and coerce form input; return cleaned patient dict."""
    errors = {}
    cleaned = {}

    for field, rules in VALIDATION_RULES.items():
        raw = form_data.get(field)
        if raw is None or str(raw).strip() == "":
            errors[field] = f"{field.replace('_', ' ').title()} is required."
            continue

        try:
            if rules["type"] is int:
                value = int(raw)
            else:
                value = float(raw)
        except (TypeError, ValueError):
            errors[field] = f"Invalid value for {field.replace('_', ' ')}."
            continue

        if "allowed" in rules and value not in rules["allowed"]:
            errors[field] = f"{field.replace('_', ' ').title()} must be one of {rules['allowed']}."
        elif value < rules["min"] or value > rules["max"]:
            errors[field] = (
                f"{field.replace('_', ' ').title()} must be between "
                f"{rules['min']} and {rules['max']}."
            )
        else:
            cleaned[field] = value

    if errors:
        raise ValidationError(errors)

    return cleaned
