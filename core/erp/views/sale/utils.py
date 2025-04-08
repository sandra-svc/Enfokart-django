# core/erp/views/sale/utils.py

def safe_format_currency(value):
    try:
        value = float(value)
        return '${:,.2f}'.format(value).replace(',', 'X').replace('.', ',').replace('X', '.')
    except Exception:
        return '$0,00'



