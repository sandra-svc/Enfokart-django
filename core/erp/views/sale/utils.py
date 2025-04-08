import json
from decimal import Decimal
from babel.numbers import format_currency

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)



def safe_format_currency(value):
    try:
        # Asegura que sea decimal
        if not isinstance(value, (Decimal, float, int)):
            value = Decimal(str(value))

        # Formatea con separador latino (punto para miles, coma para decimales)
        val = f"{value:,.2f}"
        val = val.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"${val}"
    except Exception as e:
        return f"${value}"


