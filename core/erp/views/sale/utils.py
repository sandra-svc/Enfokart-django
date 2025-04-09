# core/erp/views/sale/utils.py
from babel.core import Locale
from babel.numbers import format_currency

def safe_format_currency(value):
    try:
        # Creamos el locale explícitamente para que no dependa del sistema
        locale = Locale.parse('es_CO')
        return format_currency(value, 'COP', locale=locale)
    except Exception as e:
        return f"${value:,.2f}".replace(",", ".").replace(".", ",", 1)  # fallback





