# core/erp/views/sale/utils.py
def safe_format_currency(value):
    try:
        value = float(value)
        formatted = f"${value:,.2f}"
        # Convierte a formato colombiano: puntos como miles, coma como decimal
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return f"${value}"




