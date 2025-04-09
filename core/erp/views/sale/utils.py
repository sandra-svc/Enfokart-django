# core/erp/views/sale/utils.py
from babel.numbers import format_currency

def safe_format_currency(value):
    try:
        return format_currency(value, 'COP', locale='es_CO')
    except Exception as e:
        return f"${value:,.2f}".replace(",", ".").replace(".", ",", 1)  # fallback manual




