import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    """
    Clase auxiliar para convertir objetos Decimal de DynamoDB 
    a string o float/int para que JSON no falle.
    """
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Verificamos si es entero o flotante
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def ok(body, status=200):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            # Headers necesarios para evitar errores de CORS en el navegador
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH"
        },
        "body": json.dumps(body, cls=DecimalEncoder)
    }

def error(msg, status=400):
    # Reutilizamos la estructura de éxito pero con mensaje de error
    return ok({"error": msg}, status)
