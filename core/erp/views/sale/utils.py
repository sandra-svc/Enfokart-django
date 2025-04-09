# core/erp/views/sale/utils.py
def safe_format_currency(value):
    """
    Formatea valores monetarios sin depender del locale del sistema.
    Formato colombiano: $1.000.000,00
    """
    try:
        # Convertir a float primero para validar
        num = float(value)
        
        # Manejar valores negativos
        sign = '-' if num < 0 else ''
        num = abs(num)
        
        # Separar parte entera y decimal
        int_part = int(num)
        decimal_part = int(round((num - int_part) * 100))
        
        # Formatear parte entera con puntos
        int_str = f"{int_part:,}".replace(",", ".")
        
        # Formatear parte decimal con coma
        decimal_str = f"{decimal_part:02d}"
        
        return f"{sign}${int_str},{decimal_str}"
    except (ValueError, TypeError):
        # Fallback para valores no numéricos
        return f"${value}"




