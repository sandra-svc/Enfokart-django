import json
from decimal import Decimal
from babel.numbers import format_currency

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)

# Formateo seguro
def safe_format_currency(value, currency='USD', loc='es_CO'):
    try:
        return format_currency(value, currency, locale=loc).replace("US$", "$")
    except:
        # Fallback: Formato manual con separador latino
        val = f"{value:,.2f}"
        val = val.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"${val}"

