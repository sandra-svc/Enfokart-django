import json
from decimal import Decimal
from babel.numbers import format_currency

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)

def safe_format_currency(value, currency='USD'):
    for loc in ['es_CO', 'es_ES', 'en_US']:
        try:
            if not isinstance(value, (Decimal, float, int)):
                value = Decimal(str(value))
            return format_currency(value, currency, locale=loc).replace("US$", "$")
        except:
            continue

    # Fallback si ningún locale sirve
    val = f"{value:,.2f}"
    val = val.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"${val}"

