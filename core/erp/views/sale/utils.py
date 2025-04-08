import json
from decimal import Decimal
from babel.numbers import format_currency

# Codificador para Decimal en JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)

# Formateo seguro de moneda, con fallback si falla Babel
def safe_format_currency(value, currency='USD', loc='es_CO'):
    try:
        return format_currency(value, currency, locale=loc).replace("US$", "$")
    except Exception:
        # Fallback simple, convierte a string con formato latino
        return f"${value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
